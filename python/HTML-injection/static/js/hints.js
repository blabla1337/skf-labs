// Using code from: https://xss-game.appspot.com

var userOpenedAlert = false;

function setInnerText(element, value) {
  if (element.innerText) {
    element.innerText = value;
  } else {
    element.textContent = value;
  }
}


function logXHR(path) {
  window.location.toString().match(/level(\d+)/);
  var lNum = RegExp.$1 || "0";

  var oReq = new XMLHttpRequest();
  oReq.open("GET", '/feedback/level' + lNum + path, true);
  oReq.send();
}


function showHint() {
  var firstHiddenHint = document.querySelector('#hints li[data-hidden]');
  if (!firstHiddenHint)
    return;

  firstHiddenHint.style.display = "block";
  firstHiddenHint.removeAttribute('data-hidden');
  window.scroll(0, document.body.clientHeight);

  var hintNumEl = document.getElementById('hint-num');
  var hintNum = parseInt(hintNumEl.innerHTML, 10) + 1;
  setInnerText(hintNumEl, hintNum);

  logXHR('/hint/' + hintNum)
}
