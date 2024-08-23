const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");

let isChatDisable = false;
let inrPerUsd = 80;

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

const makePaymentSuccess = async (tickets) => {
  // You can implement payment success logic here
};

const chatFetch = async (url, options) => {
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
    <div class="user_input">
      <label for="prompt"> You </label>
      <p name="prompt" class="user_prompt">${userPrompt}</p>
    </div>`;

  form[1].value = "";

  try {
    let backendResponse = await fetch(url, options);
    backendResponse = await backendResponse.json();
    console.log(backendResponse);

    const aiResponse = JSON.parse(backendResponse.response)[0];

    if (backendResponse.confirm) {
      isChatDisable = true;
      const ticketDiv = document.createElement('div');
      ticketDiv.classList.add("tickets-div");
      main.appendChild(ticketDiv);

      let user = 0;
      let totalPrice = 0;

      for (const ticketId in backendResponse.ticketDetails) {
        const userInfo = aiResponse.users[user].user_info;
        ticketDiv.innerHTML += ` 
          <div class="ticket">
            <h1>Ticket ${user + 1}</h1>
            <p>Name: ${userInfo.name}</p> 
            <p>Age: ${userInfo.age}</p> 
            <p>Indian: ${userInfo.indian}</p>
            <p>Student: ${userInfo.student}</p>
            <p>Ticket_type: ${userInfo.ticket_type}</p>
            <p>Date: ${userInfo.day}-${userInfo.month}-${userInfo.year}</p>
            <p>Price: ${backendResponse.ticketDetails[ticketId]} INR</p>
          </div>`;
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
          try {
            const res = await fetch("/makepaymentsuccess/", {
              method: "POST",
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ tickets: Object.keys(backendResponse.ticketDetails) }),
            });
            const result = await res.json();
            console.info("Payment success data: ", result);
          } catch (err) {
            console.error("Error processing payment: ", err);
          }
        },
        onCancel: function(data, actions) {
          console.info("Payment cancelled");
        },
        onError: function(err) {
          console.error("Payment error: ", err);
        },
        style: {
          layout: 'vertical',
          color: 'blue',
          shape: 'rect',
          label: 'paypal'
        }
      }).render('#paynow-btn');
    } else {
      chatDiv.innerHTML += `
        <div class="chat response">
          <label for="response"> Bot </label>
          <p name="response" class="ai_response">${aiResponse.your_response_back_to_user}</p>
        </div>`;
    }
  } catch (error) {
    console.error("Error during chatFetch: ", error);
    chatDiv.innerHTML += `<p class="error">There was an error processing your request. Please try again later.</p>`;
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
  const url = "/ticket/";
  const options = {
    method: "POST",
    body: formData
  };
  chatFetch(url, options);
}

form.addEventListener("submit", chat);

const settingDiv = document.getElementById("setting-div");
const settingBtn = document.getElementById("setting-btn");

settingBtn.addEventListener("click", () => {
  settingDiv.classList.remove("disappear");
});

document.getElementById("close-setting").addEventListener("click", () => {
  settingDiv.classList.add("disappear");
});
