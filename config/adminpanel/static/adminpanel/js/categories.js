



const categoryTableBody = document.querySelector("#categoryTable tbody");
const addCategoryForm = document.querySelector("#addCategoryForm");
let currentPage = 1;
const pageSize = 5;
let currentSearch = '';


const CATEGORY_API_URL = "/adminpanel/api/categories/";
// const API_URL = `/adminpanel/api/categories/?search=${encodeURIComponent(currentSearch)}&page=${currentPage}&page_size=${itemsPerPage}`;

function loadCategories() {
     const url = `${CATEGORY_API_URL}?search=${encodeURIComponent(currentSearch)}&page=${currentPage}&page_size=${pageSize}`;
   fetch(url)
    .then(res => res.json())
    .then(data => {
      categoryTableBody.innerHTML = "";

      // Loop through 'results' array
      data.results.forEach(category => {
        categoryTableBody.innerHTML += `
          <tr>
            <td>${category.image ? `<img src="${category.image}" height="40">` : "N/A"}</td>
            <td>${category.name}</td>
            <td>${category.slug}</td>
            <td>
              <button onclick="editCategory(${category.id}, '${category.name}', '${category.slug}', '${category.image}',)">Edit</button>
              <button onclick="deleteCategory(${category.id})">Delete</button>
            </td>
          </tr>
        `;
      });

      // Pagination Info
      document.getElementById('pageInfo').textContent = `Page ${currentPage}`;

      // Enable/Disable pagination buttons
      document.getElementById('nextBtn').disabled = !data.next;
      document.getElementById('prevBtn').disabled = !data.previous;
    });
}




document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById('searchInput');
 if (searchInput) {
document.getElementById('searchInput').addEventListener('input', function () {
  currentSearch = this.value;
  currentPage = 1; 
  loadCategories();
});
}
});
// ⏭ Next Page
document.getElementById('nextBtn').addEventListener('click', () => {
  currentPage++;
  loadCategories();
});

// ⏮ Previous Page
document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentPage > 1) {
    currentPage--;
    loadCategories();
  }
});



function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

addCategoryForm.addEventListener('submit', function (e) {
  e.preventDefault();

  const id = document.getElementById('categoryId').value;
  const isEdit = !!id;

  const formData = new FormData();
  formData.append('name', document.getElementById('name').value);
  formData.append('slug', document.getElementById('slug').value);

  const imageInput = document.getElementById('image');
  if (imageInput.files.length > 0) {
    formData.append('image', imageInput.files[0]);  // Only add if user selects image
  }

  const url = isEdit ? `${CATEGORY_API_URL}${id}/` : CATEGORY_API_URL;
  const method = isEdit ? 'PUT' : 'POST';

  fetch(url, {
    method: method,
    body: formData,
    headers: {
      'X-CSRFToken': getCSRFToken(),  // ✅ Very important!
    }
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => { throw err });
    }
    return res.json();
  })
  .then(() => {
    addCategoryForm.reset();
    document.getElementById('categoryId').value = '';
    document.getElementById('submitBtn').textContent = 'Add Category';
    loadCategories();
  })
  .catch(err => console.error("Error:", err));
});


// Fill form to edit
function editCategory(id, name, slug) {

  document.getElementById('categoryId').value = id;
  document.getElementById('name').value = name;
  document.getElementById('slug').value = slug;
  document.getElementById('image').value = ''; // Reset image input

  document.getElementById('submitBtn').textContent = 'Update Category';
}

function deleteCategory(id) {
  if (!confirm("Are you sure you want to delete this category?")) return;

  fetch(`${CATEGORY_API_URL}${id}/`, {
    method: "DELETE",
    headers: {
      'X-CSRFToken': getCSRFToken(),  // ✅ Very important!
    }
  }).then(() => loadCategories());
}



// Initial load
loadCategories();
