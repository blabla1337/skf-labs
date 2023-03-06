const userInfo = document.getElementById("user-info");
const username = document.getElementById("username").dataset.username;
(async () => {
  const response = await fetch(`/users/${username}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.status === 200) {
    const data = await response.json();
    if (data) {
      const { name, lastname, address, phone, email } = data;
      userInfo.innerHTML = `
        <h3>Welcome, ${name} ${lastname}</h3>

        <p class="address"><span class="profile-item">Address: </span><span>${address}</span></p>
        <p class="phone"><span class="profile-item">Phone: </span><span>${phone}</span></p>
        <p class="email"><span class="profile-item">Email: </span><span>${email}</span></p>
      `;
    }
  } else {
    const data = await response.json();
    userInfo.innerText = data.error;
  }
})();
