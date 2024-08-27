const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");
const session_id = document.getElementById("session_id").innerText;
let isChatDisable = false;  // a variable which switched when ai presented the ticket
let inrPerUsd = 83;
const updateExchangeRate = async () => {
  try {
    const res = await fetch('https://open.er-api.com/v6/latest/USD');
    const data = await res.json();
    inrPerUsd = data.rates.INR;
    console.log(`Updated INR per USD: ${inrPerUsd}`);
  } catch (err) {
    console.error("Error while fetching INR per USD value \nError: ", err);
  }
};

updateExchangeRate();


const autoScroll = (scrollTop, clientHeight, scrollHeight) => {
  if (scrollTop + clientHeight <= scrollHeight) {
    console.log("down")
    const latestChatDiv = main.lastChild;
    // main.scrollTop = latestChatDiv.offsetTop;
    main.scrollTo({
      top: latestChatDiv.offsetTop,
      behavior: 'smooth'
    });
    return 1;
  }
  return 0;
}
const chatFetch = async (url, options) => {
  const scrollTop = main.scrollTop;
  const clientHeight = main.clientHeight;
  const scrollHeight = main.scrollHeight;
  console.log(form[1].value)

  if (isChatDisable) {
    if (confirm("This session has ended. Would you like to start a new session?")) {
      window.location.reload();
    }
    return;
  }

  const chatDiv = document.createElement('div');
  chatDiv.classList.add("chat-div");
  main.appendChild(chatDiv);

  const userPrompt = form[1].value.trim();
  chatDiv.innerHTML = `
    <div class="notranslate user_input" translate="no">
      <p name="prompt" class="user_prompt"><span class="userSpanPrompt" translate="no">${userPrompt}</span></p>
    </div>`;

  form[1].value = "";

  autoScroll(scrollTop, clientHeight, scrollHeight);
  try {
    let backendResponse = await fetch(url, options);
    backendResponse = await backendResponse.json();
    console.log(backendResponse);

    const aiResponse = backendResponse.response[0];

    if (backendResponse.confirm) {
      isChatDisable = true;
      const ticketDiv = document.createElement('div');
      ticketDiv.classList.add("tickets-div");
      main.appendChild(ticketDiv);

      let user = 0;
      let totalPrice = 0;
      for (const ticketId in backendResponse.ticketDetails) {
        const userInfo = aiResponse.users[user].user_info;
        ticketDiv.innerHTML += `<br>
 <div class="ticket created-by-anniedotexe">
        <div class="left">
        <div class="image">
            <p class="admit-one">
                <span>${userInfo.ticket_type}</span>
            </p>
            <div class="ticket-number">
                <p>${user + 1}</p>
            </div>
            <div class="ticket" class="bottom-left" style="position: absolute;background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px;">
            <p>Price: ${backendResponse.ticketDetails[ticketId]} INR</p>
          </div>
        </div>
        <div class="ticket-info">
            <p class="date">
                <span>${userInfo.day}</span>
                <span class="june-29">${userInfo.month}</span>
                <span>${userInfo.year}</span>
            </p>
            <div class="show-name" style="display: flex; flex-direction: column;">
                <h1>${userInfo.name}</h1>
                <div>
                    <span>student: </span>
                    <span>${userInfo.student}</span>
                </div>
                <div>
                    <span>indian</span>
                    <span>${userInfo.indian}</span>
                </div>
                <div>
                    <span>age</span>
                    <span>${userInfo.age}</span>
                </div>
            </div>
            <div class="time">
                <p>10:00 AM <span>TO</span> 5 PM</p>
            </div>
        </div>
    </div>
    <div class="right">
        <p class="admit-one">
        </p>
        <div class="right-info-container">
            <div class="show-name">
                <h1>Albert Hall</h1>
            </div>
            <div class="time">
                <p>${userInfo.name}</p>
                <p>10:00 AM <span>TO</span> 5 PM</p>
            </div>
            <div class="barcode">
                <img src="https://external-preview.redd.it/cg8k976AV52mDvDb5jDVJABPrSZ3tpi1aXhPjgcDTbw.png?auto=webp&s=1c205ba303c1fa0370b813ea83b9e1bddb7215eb" alt="QR code">
            </div>
            <p class="ticket-number">
                #20030220
            </p>
        </div>
    </div>
</div> 
         <br> `;
        user++;
        totalPrice += backendResponse.ticketDetails[ticketId];
      }

      ticketDiv.innerHTML += `<p class='total-price'>Total Price: <b>${totalPrice} INR</b></p>`;
      ticketDiv.innerHTML += `<div id="paynow-btn"></div>`;

      totalPrice = parseFloat((totalPrice / inrPerUsd).toFixed(2));
      console.log(`Total price in USD: ${totalPrice}`);

      paypal.Buttons({
        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{
              amount: {
                currency_code: "USD",
                value: totalPrice
              }
            }]
          });
        },
        onApprove: async function(data, actions) {
          console.log("Payment approved");
          const tickets = Object.keys(backendResponse.ticketDetails);
          console.log(tickets);
          try {
            const res = await fetch("/makepaymentsuccess", {
              method: "POST",
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': `${form[0].value}`
              },
              body: JSON.stringify({ tickets }),
            });
            const result = await res.json();
            console.info("Payment success data: ", result);
            alert("Payment was successfull")
          } catch (err) {
            console.error("Error processing payment: ", err);
          }
        },
        onCancel: function(data, actions) {
          console.info("Payment cancelled");
        },
        onError: function(err) {
          console.error("Payment error: ", err);
          alert("Error while payment\n Error :", err)
        },
        style: {
          layout: 'vertical',
          color: 'blue',
          shape: 'rect',
          label: 'paypal',
          align: 'center',
        },
        message: {
          amount: totalPrice,
          align: 'center',
          color: 'black',
          position: 'top',
        }
      }).render('#paynow-btn');
    } else {
      chatDiv.innerHTML += `
        <div class="chat response">
<button class="text-to-speech" onclick="speak(this)">
<svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1em" height="1em" viewBox="0 0 64 64" enable-background="new 0 0 64 64" xml:space="preserve">
<g>
	<path fill="#231F20" d="M59.998,28.001h-7.999c-2.211,0-4,1.789-4,4s1.789,4,4,4h7.999c2.211,0,4-1.789,4-4   S62.209,28.001,59.998,28.001z"/>
	<path fill="#231F20" d="M49.71,19.466l6.929-4c1.914-1.105,2.57-3.551,1.461-5.465c-1.102-1.914-3.547-2.57-5.46-1.465l-6.93,4   c-1.914,1.105-2.57,3.551-1.461,5.464C45.351,19.915,47.796,20.571,49.71,19.466z"/>
	<path fill="#231F20" d="M56.639,48.535l-6.929-3.999c-1.914-1.105-4.355-0.449-5.461,1.464c-1.105,1.914-0.453,4.359,1.461,5.465   l6.93,4c1.913,1.105,4.358,0.449,5.464-1.465S58.553,49.641,56.639,48.535z"/>
	<path fill="#231F20" d="M37.53,0.307c-1.492-0.625-3.211-0.277-4.359,0.867L18.343,16.001H4c-2.211,0-4,1.789-4,4v24   C0,46.211,1.789,48,4,48h14.343l14.828,14.828C33.937,63.594,34.96,64,35.999,64c0.516,0,1.035-0.098,1.531-0.305   c1.496-0.617,2.469-2.078,2.469-3.695V4.001C39.999,2.384,39.026,0.924,37.53,0.307z"/>
</g>
</svg>
</button>
          <label for="response"> Bot </label>
          <p name="response" class="ai_response">${aiResponse.your_response_back_to_user}</p>
        </div>`;
    }
    autoScroll(scrollTop, clientHeight, scrollHeight);
  } catch (error) {
    console.error("Error during chatFetch: ", error);
    chatDiv.innerHTML += `<p class="error">There was an error processing your request. Please try again later.</p>`;
    chatDiv.classList.add("chat-div");
    main.appendChild(chatDiv);
  }
};

async function fetchTicket(ticketId) {
  try {
    const response = await fetch(`/ticket/ticket/${ticketId}/`);
    if (!response.ok) throw new Error('Network response was not ok');
    console.log(response);
    return response.url;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    return "";
  }
}

function chat(e) {
  e.preventDefault(); // so that the page not reload multiple time on chat
  if (!form[1].value) return;
  const formData = new FormData(form);
  const url = "/";
  const options = {
    method: "POST",
    body: formData
  };
  chatFetch(url, options);
}
form.addEventListener("submit", chat);
(() => {
  const formData = new FormData(form);
  formData.delete("user_input")
  formData.append("user_input", `[Hi, i m your new ${document.getElementById("user").innerText}.I don't want to book a ticket for anyone now,
                          I just want to know about you.My preferred language is  ${document.getElementById("language-sys").innerText}. 
                          .I hate cringy face emojis.
                          .Clients love consise results.
                          Please only use my preferred language, even if I use another language to talk with you.
                          I hate when someone asks more than one detail / question in at a time to my clients.
                          Just ask One by one no need to rush. 
                          Dont forget to ask the age of my clients for whom you gonna book the tickets.
                          I just want to know what you can do in a concise way.
                          client might reprompt you with same prompt again and again.
                          just remind me if I do that and use different reminders each time.Todays Date is ${Date()}] Dont book the ticket before this. Date should be greater than or equal to current date.`);
  const url = "/";
  const options = {
    method: "POST",
    body: formData
  };
  fetch(url, options)
    .then(res => res.json())
    .then((data) => {
      console.log(data)
      const aiResponse = data.response[0];
      const chatDiv = document.createElement('div');
      main.appendChild(chatDiv)

      chatDiv.innerHTML += `
        <div class="chat response">
<button class="text-to-speech" onclick="speak(this)">
<svg version="1.0" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1em" height="1em" viewBox="0 0 64 64" enable-background="new 0 0 64 64" xml:space="preserve">
<g>
	<path fill="#231F20" d="M59.998,28.001h-7.999c-2.211,0-4,1.789-4,4s1.789,4,4,4h7.999c2.211,0,4-1.789,4-4   S62.209,28.001,59.998,28.001z"/>
	<path fill="#231F20" d="M49.71,19.466l6.929-4c1.914-1.105,2.57-3.551,1.461-5.465c-1.102-1.914-3.547-2.57-5.46-1.465l-6.93,4   c-1.914,1.105-2.57,3.551-1.461,5.464C45.351,19.915,47.796,20.571,49.71,19.466z"/>
	<path fill="#231F20" d="M56.639,48.535l-6.929-3.999c-1.914-1.105-4.355-0.449-5.461,1.464c-1.105,1.914-0.453,4.359,1.461,5.465   l6.93,4c1.913,1.105,4.358,0.449,5.464-1.465S58.553,49.641,56.639,48.535z"/>
	<path fill="#231F20" d="M37.53,0.307c-1.492-0.625-3.211-0.277-4.359,0.867L18.343,16.001H4c-2.211,0-4,1.789-4,4v24   C0,46.211,1.789,48,4,48h14.343l14.828,14.828C33.937,63.594,34.96,64,35.999,64c0.516,0,1.035-0.098,1.531-0.305   c1.496-0.617,2.469-2.078,2.469-3.695V4.001C39.999,2.384,39.026,0.924,37.53,0.307z"/>
</g>
</svg>
</button>
          <label for="response"> Bot </label>
          <p name="response" class="ai_response">${aiResponse.your_response_back_to_user}</p>
        </div>`;
    });

})()
