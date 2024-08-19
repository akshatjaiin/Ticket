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
            <ul>
                <li>
                     <div class="user_input">${data.user_input}</div>
                </li>
                <li>
                    <div class="response">${res}</div>
               </li>
            </ul>`
    })
    .catch((error) => {

      console.error(error);

    });
})
