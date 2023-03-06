const url = decodeURI(location.href);
const userposition = url.indexOf("name=");

if (userposition != -1) {
  const user = url.substring(userposition + 5);
  document.getElementById("welcome").innerHTML =
    user + ", please confirm your password";
}
