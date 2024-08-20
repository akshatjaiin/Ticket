const form = document.getElementById("form-chat");
const main = document.getElementById("main");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const url = "/ticket/";
  const options = {
    method: "POST",
    body: formData
  };
  fetch(url, options)
    .then((response) => response.json())

    .then((data) => {
      const res = JSON.parse(data.response)[0].your_response_back_to_user;
      console.info(data.response);
      main.innerHTML += ` 
<div class="chat-div">
<div class="chat user_input">
<label for="prompt"> You </label>
<p name="prompt">${data.user_input}</p>
</div>
<div class="chat response">

<label for="response"> Bot </label>
<p name="response">${res}</p>
</div>
`
    })
    .catch((error) => {

      console.error(error);

    });
})
