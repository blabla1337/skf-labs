const form = document.getElementById("register-form");
const error = document.getElementById("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/register/", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.status === 200) {
    window.location.href = "/login";
  } else {
    const data = await response.json();
    error.innerText = data.error;
  }
});
