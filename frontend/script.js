// script.js

// Handle Registration Form Submission
document.getElementById('registration-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const payload = { email, password };

  fetch("http://127.0.0.1:8000/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('registration-output').textContent = "Registered! User ID: " + data.id;
    console.log("Registration success:", data);
  })
  .catch(err => {
    document.getElementById('registration-output').textContent = "Error: " + err.message;
    console.error("Registration error:", err);
  });
});

// Handle Login Form Submission
document.getElementById('login-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const payload = { email, password };

  fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('login-output').textContent = "Logged in! Token: " + data.access_token;
    console.log("Login success:", data);
    // Optionally, store the JWT token in localStorage for later use
    localStorage.setItem("jwt", data.access_token);
  })
  .catch(err => {
    document.getElementById('login-output').textContent = "Error: " + err.message;
    console.error("Login error:", err);
  });
});
