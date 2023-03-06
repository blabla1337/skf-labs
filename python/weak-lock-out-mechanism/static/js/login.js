const form = document.getElementById("login-form");
const error = document.getElementById("error");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const captcha = document.getElementById("captcha").value;

  const response = await fetch("/login/", {
    method: "POST",
    body: JSON.stringify({ username, password, captcha }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.status === 200) {
    window.location.href = "/";
  } else {
    const data = await response.json();
    const { number1, number2, operator } = await getCaptcha();
    const captchaEl = document.getElementsByClassName("captcha")[0];
    captchaEl.getElementsByClassName("n1")[0].innerText = number1;
    captchaEl.getElementsByClassName("n2")[0].innerText = number2;
    captchaEl.getElementsByClassName("op")[0].innerText = operator;
    error.innerText = data.error;
  }
});

/**
 *
 * @returns {Promise<{number1: string, number2: string, operator: string }>}
 */
async function getCaptcha() {
  const response = await fetch("/captcha/");
  // {"number1": number1, "number2": number2, "operator": operator}
  return await response.json();
}
