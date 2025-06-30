// ✅ Updated JavaScript for handling all Product fields
const PRODUCT_API_URL = "/adminpanel/api/products/";
const productTableBody = document.getElementById("productTableBody");
const addProductForm = document.getElementById("addProductForm");

let currentproductPage = 1;
let currentproductSearch = "";

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

function loadProducts() {
  let url = `${PRODUCT_API_URL}?page=${currentproductPage}&page_size=5`;
  if (currentproductSearch) {
    url += `&search=${currentproductSearch}`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      productTableBody.innerHTML = "";
      data.results.forEach(product => {
        const isLowStock = product.total_stock < product.stock_threshold;

        productTableBody.innerHTML += `
          <tr>
            <td>${product.image ? `<img src="${product.image}" height="40">` : "N/A"}</td>
            <td>${product.name}</td>
            <td>${product.category}</td>
            <td>${product.brand}</td>
            <td>${product.mrp}</td>
            <td>${product.selling_price}</td>
            <td>
              ${product.total_stock}
              ${isLowStock ? `<span class="low-stock-badge">Low Stock</span>` : ""}
            </td>
            <td>${product.stock_threshold}</td>
            <td>
              <button onclick="editProduct(${product.id}, '${product.name.replace(/'/g, "\\'")}', ${product.category}, ${product.brand}, '${product.mrp}', '${product.selling_price}', '${product.slug.replace(/'/g, "\\'")}', '${product.sku}', ${product.return_available}, ${product.instock}, '${product.ages}', ${product.is_free_delivery}, '${product.delivery_charge}',  ${product.is_wholesale}, ${product.min_wholesale_quantity}, '${product.wholesale_price}', '${product.key_features}', '${product.description}', ${product.total_stock}, ${product.stock_threshold})">Edit</button>
              <button onclick="deleteProduct(${product.id})">Delete</button>
            </td>
          </tr>`;
      });

      document.getElementById('pageInfo').textContent = `Page ${currentproductPage}`;
      document.getElementById('nextBtn').disabled = !data.next;
      document.getElementById('prevBtn').disabled = !data.previous;
    });
}


document.getElementById('nextBtn').addEventListener('click', () => {
  currentproductPage++;
  loadProducts();
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentproductPage > 1) {
    currentproductPage--;
    loadProducts();
  }
});

document.getElementById('searchProductInput').addEventListener('input', function () {
  currentproductSearch = this.value;
  currentproductPage = 1;
  loadProducts();
});

document.addEventListener("DOMContentLoaded", function () {
  if (addProductForm) {
    addProductForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData();
      formData.append("name", document.getElementById("name").value);
      formData.append("category", document.getElementById("category").value);
      formData.append("brand", document.getElementById("brand").value);
      formData.append("mrp", document.getElementById("mrp").value);
      formData.append("selling_price", document.getElementById("selling_price").value);
      formData.append("sku", document.getElementById("sku").value);
      formData.append("slug", document.getElementById("slug").value);
      formData.append("instock", document.getElementById("instock").checked ? "true" : "false");
      formData.append("return_available", document.getElementById("return_available").checked ? "true" : "false");
      formData.append("ages", document.getElementById("ages").value);
      formData.append("is_free_delivery", document.getElementById("is_free_delivery").checked ? "true" : "false");
      formData.append("delivery_charge", document.getElementById("delivery_charge").value);
      formData.append("is_wholesale", document.getElementById("is_wholesale").checked ? "true" : "false");
      formData.append("min_wholesale_quantity", document.getElementById("min_wholesale_quantity").value);
      formData.append("wholesale_price", document.getElementById("wholesale_price").value);
      formData.append("key_features", document.getElementById("key_features").value);
      formData.append("description", document.getElementById("description").value);
      formData.append("total_stock", document.getElementById("total_stock").value);
      formData.append("stock_threshold", document.getElementById("stock_threshold").value);

      const imageInput = document.getElementById("image");
      if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]);
      }

      const id = document.getElementById("productId").value;
      const isEdit = !!id;
      const url = isEdit ? `${PRODUCT_API_URL}${id}/` : PRODUCT_API_URL;
      const method = isEdit ? "PUT" : "POST";

      fetch(url, {
        method: method,
        body: formData,
        headers: {
          "X-CSRFToken": getCSRFToken()
        }
      })
        .then(res => res.json())
        .then(() => {
           var newProduct = document.getElementById("name").value;
          if(method == "POST"){
          alert(newProduct + " saved successfully.");
        }else{
                    alert(newProduct + " updated successfully.");

        }
          addProductForm.reset();
          document.getElementById("productId").value = "";
          document.getElementById("submitBtn").textContent = "Add Product";
          loadProducts();
        })
        .catch(err => console.error("Error:", err));
    });
  }
});

function editProduct(id, name, category, brand, mrp, selling_price, slug, sku, return_available, instock, ages, is_free_delivery, delivery_charge, is_wholesale, min_wholesale_quantity, wholesale_price, key_features, description, total_stock, stock_threshold) {

  document.getElementById("productId").value = id;
  document.getElementById("name").value = name;
  document.getElementById("category").value = category;
  document.getElementById("brand").value = brand;
  document.getElementById("mrp").value = mrp;
  document.getElementById("selling_price").value = selling_price;
  document.getElementById("slug").value = slug;
  document.getElementById("sku").value = sku;
  document.getElementById("return_available").checked = return_available;
  document.getElementById("instock").checked = instock;
  document.getElementById("ages").value = ages;
  document.getElementById("is_free_delivery").checked = is_free_delivery;
  document.getElementById("delivery_charge").value = delivery_charge;
  document.getElementById("is_wholesale").checked = is_wholesale;
 
  document.getElementById("min_wholesale_quantity").value = min_wholesale_quantity;
  document.getElementById("wholesale_price").value = wholesale_price;
  document.getElementById("key_features").value = key_features;
  document.getElementById("description").value = description;
  document.getElementById("total_stock").value = total_stock;
  document.getElementById("stock_threshold").value = stock_threshold;
  document.getElementById("submitBtn").textContent = "Update Product";
}

function deleteProduct(id) {
  if (confirm("Are you sure you want to delete this product?")) {
    fetch(`${PRODUCT_API_URL}${id}/`, {
      method: "DELETE",
      headers: { "X-CSRFToken": getCSRFToken() }
    })
      .then(() => loadProducts());
  }
}

loadProducts();
