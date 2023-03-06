const comments = document.getElementById("comments");
const form = document.getElementById("comment-form");
const username = document.getElementById("username").dataset.username;

comments.innerHTML = "Loading...";
comments.addEventListener("click", (e) => {
  if (e.target.id === "comment__edit") {
    const comment = e.target.parentElement;
    const commentText = comment.querySelector(".comment__text");
    const id = comment.dataset.id;

    const newCommentText = prompt("Edit comment:", commentText.innerText);
    if (newCommentText) {
      fetch("/comments/", {
        method: "PUT",
        body: JSON.stringify({
          id,
          text: newCommentText,
        }),

        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => {
        response.json().then((data) => {
          if (response.status === 200) {
            commentText.innerText = newCommentText;
          }
        });
      });
    }
  }
});

function loadComments() {
  fetch("/comments/").then((response) => {
    response.json().then((data) => {
      comments.innerHTML = "";

      const commentsList = data.comments;
      commentsList.forEach((comment) => {
        comments.innerHTML += `<div class="comment" data-id=${comment._id}>
          <div class="comment__author">${comment.author}: </div>
          <div class="comment__text">${comment.text}</div>
          ${
            username === comment.author
              ? `<div id="comment__edit">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z"/>
          </svg>
        </div>`
              : ""
          }
          
        </div>`;
      });
    });
  });
}

if (form) {
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const text = formData.get("text");

    fetch("/comments/", {
      method: "POST",
      body: JSON.stringify({ text }),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      response.json().then((data) => {
        form.reset();
        loadComments();
      });
    });
  });
}

loadComments();
