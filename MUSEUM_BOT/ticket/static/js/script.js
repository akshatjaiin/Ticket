const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");

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

const makePaymentSuccess = async (tickets) => {
  // You can implement payment success logic here
};

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
      <p name="prompt" class="user_prompt"><span class="userSpanPrompt" >${userPrompt}</span></p>
    </div>`;

  form[1].value = "";

  // try {
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
      ticketDiv.innerHTML += `<br> <div class="ticket created-by-anniedotexe">
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
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [{
            amount: {
              currency_code: "USD",
              value: totalPrice
            }
          }]
        });
      },
      onApprove: async function (data, actions) {
        console.log("Payment approved");
        const tickets = Object.keys(backendResponse.ticketDetails);
        console.log(tickets);
        try {
          const res = await fetch("/ticket/makepaymentsuccess", {
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
      onCancel: function (data, actions) {
        console.info("Payment cancelled");
      },
      onError: function (err) {
        console.error("Payment error: ", err);
        alert("Error while payment\n Error :", err)
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
  autoScroll(scrollTop, clientHeight, scrollHeight);
  // } catch (error) {
  //   console.error("Error during chatFetch: ", error);
  //   chatDiv.innerHTML += `<p class="error">There was an error processing your request. Please try again later.</p>`;
  // }
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
