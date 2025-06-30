const orderTableBody = document.getElementById("orderTableBody");

let currentOrderPage = 1;
const orderPageSize = 2;
let currentOrderSearch = '';

const ORDER_API_URL = "/adminpanel/api/orders/";


  function fetchOrders() {
         const url = `${ORDER_API_URL}?search=${encodeURIComponent(currentOrderSearch)}&page=${currentOrderPage}&page_size=${orderPageSize}`;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        orderTableBody.innerHTML = "";
        console.log(data)
         console.log(data.results)
        data.results.forEach(order => {
          orderTableBody.innerHTML += `
            <tr>
              <td>${order.id}</td>
<td>${order.user}</td>
<td>${order.full_name}</td>
<td>${order.phone}</td>
<td>${order.address}</td>
<td>${order.payment_method}</td>
  <td>
        <select onchange="updateOrderStatus(${order.id}, this.value)">
          ${['PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED'].map(status => `
            <option value="${status}" ${order.status === status ? 'selected' : ''}>${status}</option>
          `).join('')}
        </select>
      </td><td>₹${order.total_amount}</td>
<td>${new Date(order.order_date).toLocaleString()}</td>

              <td>
            <a  onclick="viewOrder(${order.id})" class="btn btn-sm btn-outline-info" title="View Order">
  <i class="fas fa-eye"></i>
</a>



  <button onclick="deleteOrder(${order.id})" class="btn btn-sm" title="Delete Order" style="border: none; background: none;">
    <i class="fas fa-trash-alt" style="color: red; font-size: 16px;"></i>
  </button>
         </td>
            </tr>
          `;
        });
        document.getElementById('pageInfo').textContent = `Page ${currentOrderPage}`;
      document.getElementById('nextBtn').disabled = !data.next;
      document.getElementById('prevBtn').disabled = !data.previous;
      });
  }

  document.getElementById('nextBtn').addEventListener('click', () => {
  currentOrderPage ++;
  fetchOrders();
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentOrderPage > 1) {
    currentOrderPage--;
    fetchOrders();
  }
});
document.getElementById('searchOrderInput').addEventListener('input', function () {
  currentOrderSearch = this.value;
  currentOrderPage = 1; // Reset to first page
  fetchOrders();
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function viewOrder(orderId) {
  // Construct the URL dynamically
  const url = `/adminpanel/orders/${orderId}/`;

  // Redirect to that URL
  window.location.href = url;
}
function updateOrderStatus(orderId, newStatus) {
  fetch(`/adminpanel/api/orders/${orderId}/update_status/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({ status: newStatus })
  })
  .then(res => {
    if (!res.ok) throw new Error("Failed to update status");
    return res.json();
  })
  .then(data => {
    alert("Order status updated successfully.");
    fetchOrders();
  })
  .catch(err => {
    alert("Error updating status");
    console.error(err);
  });
}

// Helper function to get CSRF token
function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function deleteOrder(orderId) {
  if (confirm("Are you sure you want to delete this order?")) {
    fetch(`/adminpanel/orders/${orderId}/delete/`, {
    method: "DELETE",
    headers: {
      'X-CSRFToken': getCSRFToken(),  // ✅ Very important!
    }
    })
    .then(res => {
      if (res) {
       fetchOrders();
      } else {
        alert('Failed to delete order.');
      }
    });
  }
}


  fetchOrders();