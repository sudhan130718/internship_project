const BRAND_API_URL = "/adminpanel/api/brands/";
const brandTableBody = document.getElementById("brandTableBody");
const addBrandForm = document.getElementById("addBrandForm");

let currentbrandPage = 1;
let currentbrandSearch = "";

function loadBrands() {
  let url = `${BRAND_API_URL}?page=${currentbrandPage}&page_size=5`;
  if (currentbrandSearch) {
    url += `&search=${currentbrandSearch}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      brandTableBody.innerHTML = "";
      data.results.forEach(brand => {
        brandTableBody.innerHTML += `
          <tr>
            <td>${brand.logo ? `<img src="${brand.logo}" height="40">` : "N/A"}</td>
            <td>${brand.name}</td>
            <td>${brand.description}</td>
            <td>
              <button onclick="editBrand(${brand.id}, '${brand.name}', '${brand.description}')">Edit</button>
              <button onclick="deleteBrand(${brand.id})">Delete</button>
            </td>
          </tr>`;
      });

      document.getElementById('pageInfo').textContent = `Page ${currentbrandPage}`;
      document.getElementById('nextBtn').disabled = !data.next;
      document.getElementById('prevBtn').disabled = !data.previous;
    });
}
function getCSRFToken() {
  let cookieValue = null;
  const name = "csrftoken";
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

addBrandForm.addEventListener("submit", function (e) {

  e.preventDefault();


  const formData = new FormData();
  formData.append('name', document.getElementById('name').value);
  formData.append('description', document.getElementById('description').value);

   const logoInput = document.getElementById('logo');
  if (logoInput.files.length > 0) {
    formData.append('logo', logoInput.files[0]);
  }
  const id = document.getElementById('brandId').value;
  const isEdit = !!id;

  const url = isEdit ? `${BRAND_API_URL}${id}/` : BRAND_API_URL;
  const method = isEdit ? 'PUT' : 'POST';

  fetch(url, {
    method,
    body: formData,
       headers: {
      'X-CSRFToken': getCSRFToken(),  
    }
  })
  
  
.then(res => {
    if (!res.ok) {
      return res.json().then(err => { throw err });
    }
    return res.json();
  })
  .then(() => {
     addBrandForm.reset();
    document.getElementById('brandId').value = '';
    document.getElementById('submitBtn').textContent = 'Add Brand';

    loadBrands();
  })
  .catch(err => console.error("Error:", err));
});


function editBrand(id, name, description) {
  document.querySelector('[name="name"]').value = name;
  document.querySelector('[name="description"]').value = description;
  document.getElementById('brandId').value = id;
  document.getElementById('submitBtn').textContent = 'Update Brand';
}

function deleteBrand(id) {
  if (confirm("Are you sure you want to delete this brand?")) {
    fetch(`${BRAND_API_URL}${id}/`, { method: "DELETE", headers: {
      'X-CSRFToken': getCSRFToken(),  
    } })
      .then(() => loadBrands());
  }
}

document.getElementById('nextBtn').addEventListener('click', () => {
  currentbrandPage++;
  loadBrands();
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentbrandPage > 1) {
    currentbrandPage--;
    loadBrands();
  }
});

const searchInput = document.getElementById('searchInput');
if (searchInput) {
  searchInput.addEventListener('input', function () {
    currentbrandSearch = this.value;
    currentbrandPage = 1;
    loadBrands();
  });
}
loadBrands();
