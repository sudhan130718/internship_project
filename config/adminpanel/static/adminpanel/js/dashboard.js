document.addEventListener("DOMContentLoaded", () => {
  fetch('/adminpanel/api/dashboard/')
    .then(res => res.json())
    .then(data => {
      document.getElementById('total-orders').textContent = data.total_orders;
      document.getElementById('total-users').textContent = data.total_users;
      document.getElementById('total-products').textContent = data.total_products;
      document.getElementById('total-categories').textContent = data.total_categories;
      document.getElementById('total-brands').textContent = data.total_brands;
      document.getElementById('recent-orders').innerHTML = data.recent_orders.map(order => (
        `<p>#${order.id} - ${order.full_name} - ₹${order.total_amount} - ${order.status}</p>`
      )).join('');
    })
    .catch(err => {
      document.getElementById('recent-orders').textContent = 'Error loading data';
      console.error(err);
    });
});
