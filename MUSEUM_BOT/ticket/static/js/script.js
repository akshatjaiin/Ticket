const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");

// a function to chat with ai  on backend
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
  let backendResponse = await fetch(url, options);
  backendResponse = await backendResponse.json();
  console.log(backendResponse);

  // parse the stringify output of ai 
  const aiResponse = JSON.parse(backendResponse.response)[0];

  // if user confirm the ticket
  if (backendResponse.confirm) {
    const ticketDiv = document.createElement('div');
    ticketDiv.classList.add("tickets-div");
    main.appendChild(ticketDiv);
    let user = 0;
    let totalPrice = 0;
    for (ticketId in backendResponse.ticketDetails) {
      const userInfo = aiResponse.users[user].user_info;
      ticketDiv.innerHTML += ` 
        <div class= "ticket" >
          <h1>Ticket ${user + 1}</h1>
          <p>Name: ${userInfo.name}</p> 
          <p>Age: ${userInfo.age}</p> 
          <p>Indian: ${userInfo.indian}</p>
          <p>Student: ${userInfo.student}</p>
          <p>Ticket_type: ${userInfo.ticket_type}</p>
          <p>Date: ${userInfo.day}-${userInfo.month}-${userInfo.year} </p>
          <p>Price: ${backendResponse.ticketDetails[ticketId]}</p>
        </div > `
      user++;
      totalPrice += backendResponse.ticketDetails[ticketId];
    }
    ticketDiv.innerHTML += `<p class='total-price'>TotalPrice: <b>${totalPrice}</b></p>`;
  } else {
    // append the user res to the html
    chatDiv.innerHTML += `
      <div class="chat response" >
<label for="response"> Bot </label>
<p name="response">${aiResponse.your_response_back_to_user}</p>
</div > `
  }
  return;
}

// ticketViewer.parentElement.classList.add("disappear");
async function fetchTicket(ticketId) {
  try {
    const response = await fetch(`/ticket/ticket/${ticketId}/`); // Adjust the URL as needed
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    console.log(response)
    return response.url;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    return "";
  }
}

function chat(e) {
  e.preventDefault(); // so that the page not reload multiple time on chat
  const formData = new FormData(form);
  const url = "/ticket/";
  const options = {
    method: "POST",
    body: formData
  };
  chatFetch(url, options);
}

// a eventlistener designed 
form.addEventListener("submit", chat);


//  for setting popuo
const settingDiv = document.getElementById("setting-div")
const settingBtn = document.getElementById("setting-btn")


//  for opening setting popup
settingBtn.addEventListener("click", () => {
  settingDiv.classList.remove("disappear")
})
// for closeing setting popup
document.getElementById("close-setting")
  .addEventListener("click", () => {
    settingDiv.classList.add("disappear")
  })
