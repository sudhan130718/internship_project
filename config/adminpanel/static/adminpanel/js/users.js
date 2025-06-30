const userTableBody = document.getElementById("userTableBody");

let currentUserPage = 1;
const userPageSize = 5;
let currentUserSearch = '';

const USER_API_URL = "/adminpanel/api/users/";


  function fetchUsers() {
         const url = `${USER_API_URL}?search=${encodeURIComponent(currentUserSearch)}&page=${currentUserPage}&page_size=${userPageSize}`;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        userTableBody.innerHTML = "";
        console.log(data)
         console.log(data.results)
        data.results.forEach(user => {
          userTableBody.innerHTML += `
            <tr>
              <td>${user.id}</td>
              <td>${user.username}</td>
              <td>${user.email || '-'}</td>
              <td>${user.first_name || '-'}</td>
              <td>${user.last_name || '-'}</td>
              <td>${user.is_staff ? 'Admin' : 'User'}</td>
              <td>
                <button  onclick="editUser(${user.id}, '${user.username}', '${user.email}', '${user.first_name}', '${user.password}')" style="display: none;">Edit</button>
                <button onclick="deleteUser(${user.id})">Delete</button>
              </td>
            </tr>
          `;
        });
        document.getElementById('pageInfo').textContent = `Page ${currentUserPage}`;
      document.getElementById('nextBtn').disabled = !data.next;
      document.getElementById('prevBtn').disabled = !data.previous;
      });
  }

  document.getElementById('nextBtn').addEventListener('click', () => {
  currentUserPage ++;
  fetchUsers();
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (currentUserPage > 1) {
    currentUserPage--;
    fetchUsers();
  }
});
document.getElementById('searchUserInput').addEventListener('input', function () {
  currentUserSearch = this.value;
  currentUserPage = 1; // Reset to first page
  fetchUsers();
});



document.addEventListener("DOMContentLoaded", function () {
  const USER_API_URL = "/adminpanel/api/users/";

  // ✅ CSRF Token helper
  function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  }

  const addUserForm = document.querySelector("#addUserForm");  // 🔁 FIXED ID name

  addUserForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const id = document.getElementById('userId').value;
    const isEdit = !!id;

    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('first_name', document.getElementById('first_name').value);
    formData.append('last_name', document.getElementById('last_name').value);
    
    // 🛑 Only send password if creating (not editing)
    if (!isEdit) {
      const password = document.getElementById('password').value;
      const confirmPassword = document.getElementById('confirmpassword').value;
      if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
      }
      formData.append('password', password);
    }

    const url = isEdit ? `${USER_API_URL}${id}/` : USER_API_URL;
    const method = isEdit ? 'PUT' : 'POST';

    fetch(url, {
      method: method,
      body: formData,
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    })
    .then(res => {
      if (!res.ok) {
        return res.json().then(err => { throw err });
      }
      return res.json();
    })
    .then(() => {
      addUserForm.reset();
      document.getElementById('userId').value = '';
      document.getElementById('submitBtn').textContent = 'Add User';
      fetchUsers();
    })
    .catch(err => {
      console.error("Error:", err);
      alert("Something went wrong. See console for details.");
    });
  });
});


  // Fill form to edit
function editUser(id, username, email,first_name) {

  document.getElementById('userId').value = id;
  document.getElementById('username').value = username;
  document.getElementById('email').value = email;
    document.getElementById('first_name').value = first_name;
  document.getElementById('password').value = password;


  document.getElementById('submitBtn').textContent = 'Update User';
}
 

function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return;

  fetch(`${USER_API_URL}${id}/`, {
    method: "DELETE",
    headers: {
      'X-CSRFToken': getCSRFToken(),  // ✅ Very important!
    }
  }).then(() => fetchUsers());
}


  fetchUsers();

