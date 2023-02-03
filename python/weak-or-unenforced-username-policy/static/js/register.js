const form = document.getElementById("register-form");
const error = document.getElementById("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;

  const lastname = document.getElementById("lastname").value;
  const password = document.getElementById("password").value;
  const address = document.getElementById("address").value;
  const phone = document.getElementById("phone").value;
  const email = document.getElementById("email").value;

  const response = await fetch("/register/", {
    method: "POST",
    body: JSON.stringify({
      password,
      name,
      lastname,
      address,
      phone,
      email,
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
