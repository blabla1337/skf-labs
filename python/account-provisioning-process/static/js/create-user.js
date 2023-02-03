const form = document.getElementById("create-user");
const info = document.getElementById("info");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  const response = await fetch("/create-user/", {
    method: "POST",
    body: JSON.stringify({ username, password, role }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();

  if (response.status !== 200) {
    info.innerText = `Error creating user`;
  } else {
    info.innerText = "User created successfully";
  }
});
