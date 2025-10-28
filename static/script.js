
// Register
if (document.getElementById('registerForm')) {
  document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    alert(data.message || data.error);
    if (res.ok) window.location.href = '/';
  });
}

// Login
if (document.getElementById('loginForm')) {
  document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    alert(data.error || 'Logged in!');
    if (res.ok) {
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      window.location.href = '/dashboard';
    }
  });
}

// Dashboard logic
if (window.location.pathname === '/dashboard') {
  const token = localStorage.getItem('token');
  if (!token) window.location.href = '/';
  document.getElementById('logoutBtn').onclick = function() {
    localStorage.clear();
    window.location.href = '/';
  };
  fetch('/api/users', {
    headers: { 'Authorization': token }
  }).then(res => res.json()).then(data => {
    const ul = data.users||[]
    const userList = document.getElementById('userList');
    userList.innerHTML = ul.map(u=>`<div>${u.name} (${u.email}) <button onclick="deleteUser('${u.id}')">Delete</button></div>`).join('')
    window.deleteUser = function(id) {
      fetch(`/api/users/${id}`, {
        method: 'DELETE', headers:{'Authorization':token}
      }).then(r=>r.json()).then(d=>{alert(d.message);location.reload()})
    }
  })
}
