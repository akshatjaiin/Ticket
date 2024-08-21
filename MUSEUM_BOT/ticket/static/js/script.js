const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");
// ticketViewer.parentElement.classList.add("disappear");
async function fetchTicket(ticketId) {
  try {
    const response = await fetch(`/api/ticket/${ticketId}/`); // Adjust the URL as needed
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const ticket = await response.json();
    displayTicket(ticket);
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const url = "/ticket/";
  const options = {
    method: "POST",
    body: formData
  };
  const chatFetch = async (url, options) => {
    // a div where prompt and res gonna store 
    const chatDiv = document.createElement('div');
    chatDiv.classList.add("chat-div");

    // adding the div to the html 
    main.appendChild(chatDiv);

    // appending the prompt to the chat-div
    chatDiv.innerHTML += `
<div class="chat user_input">
<label for="prompt"> You </label>
<p name="prompt">${form[1].value}</p>
</div>`

    // clearning the prompt input 
    form[1].value = "";

    // send the prompt to the backend 
    let res = await fetch(url, options);
    res = await res.json();
    console.log(res);


    // parse the stringify output of ai 
    const response = JSON.parse(res.response)[0];
    if (response.confirm) {
      console.log(response.users)
      const ticketDiv = document.createElement('div');
      ticketDiv.classList.add("tickets-div")
        const ticket_id = response.users[user].user_info;
        ticketDiv.innerHTML += fetchTicket(1);
      }
      chatDiv.appendChild(ticketDiv);
      chatDiv.innerHTML += '<button class="pay-btn">Pay now</button>'
      return;
    }



    // append the user res to the html
    chatDiv.innerHTML += `
    <div class="chat response" >
<label for="response"> Bot </label>
<p name="response">${response.your_response_back_to_user}</p>
</div >
    `

    return;
  }
  chatFetch(url, options);
})