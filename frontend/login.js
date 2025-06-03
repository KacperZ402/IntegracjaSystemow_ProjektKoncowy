async function login(event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`
  });

  const data = await response.json();
  if (response.ok) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", username);
    window.location.href = "/";
  } else {
    document.getElementById("error").textContent = "❌ Błędna nazwa użytkownika lub hasło.";
  }
}
