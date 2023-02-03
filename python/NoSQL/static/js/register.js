const form = document.getElementById("register-form");
const error = document.getElementById("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/register/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.status === 200) {
    window.location.href = "/login";
  } else {
    const data = await response.json();
    let errorMessage = "Error registering user";
    if (data.error) {
      errorMessage = data.error;
    }
    error.innerText = errorMessage;
  }
});
