const form = document.getElementById("form-chat");
const main = document.getElementById("main");
const ticketViewer = document.getElementById("tickets");
// ticketViewer.parentElement.classList.add("disappear");

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
      for (user = 0; user < response.users.length; user++) {
        const userInfo = response.users[user].user_info;
        ticketDiv.innerHTML += ` 
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>tic</title>
    <style>
            @import url("https://fonts.googleapis.com/css2?family=Staatliches&display=swap");
    @import url("https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap");

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body,
    html {
        height: 100vh;
        display: grid;
        font-family: "Staatliches", cursive;
        background: #d83565;
        color: black;
        font-size: 14px;
        letter-spacing: 0.1em;
    }

    .ticket {
        margin: auto;
        display: flex;
        background: white;
        box-shadow: rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px;
    }

    .left {
        display: flex;
    }

    .image {
        height: 250px;
        width: 250px;
        background-image: url("https://media.pitchfork.com/photos/60db53e71dfc7ddc9f5086f9/1:1/w_1656,h_1656,c_limit/Olivia-Rodrigo-Sour-Prom.jpg");
        background-size: contain;
        opacity: 0.85;
    }

    .admit-one {
        position: absolute;
        color: darkgray;
        height: 250px;
        padding: 0 10px;
        letter-spacing: 0.15em;
        display: flex;
        text-align: center;
        justify-content: space-around;
        writing-mode: vertical-rl;
        transform: rotate(-180deg);
    }

    .admit-one span:nth-child(2) {
        color: white;
        font-weight: 700;
    }

    .left .ticket-number {
        height: 250px;
        width: 250px;
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
        padding: 5px;
    }

    .ticket-info {
        padding: 10px 30px;
        display: flex;
        flex-direction: column;
        text-align: center;
        justify-content: space-between;
        align-items: center;
    }

    .date {
        border-top: 1px solid gray;
        border-bottom: 1px solid gray;
        padding: 5px 0;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: space-around;
    }

    .date span {
        width: 100px;
    }

    .date span:first-child {
        text-align: left;
    }

    .date span:last-child {
        text-align: right;
    }

    .date .june-29 {
        color: #d83565;
        font-size: 20px;
    }

    .show-name {
        font-size: 32px;
        font-family: "Nanum Pen Script", cursive;
        color: #d83565;
    }

    .show-name h1 {
        font-size: 48px;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #4a437e;
    }

    .time {
        padding: 10px 0;
        color: #4a437e;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 10px;
        font-weight: 700;
    }

    .time span {
        font-weight: 400;
        color: gray;
    }

    .left .time {
        font-size: 16px;
    }


    .location {
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        padding-top: 8px;
        border-top: 1px solid gray;
    }

    .location .separator {
        font-size: 20px;
    }

    .right {
        width: 180px;
        border-left: 1px dashed #404040;
    }

    .right .admit-one {
        color: darkgray;
    }

    .right .admit-one span:nth-child(2) {
        color: gray;
    }

    .right .right-info-container {
        height: 250px;
        padding: 10px 10px 10px 35px;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
    }

    .right .show-name h1 {
        font-size: 18px;
    }

    .barcode {
        height: 100px;
    }

    .barcode img {
        height: 100%;
    }

    .right .ticket-number {
        color: gray;
}

    </style>
</head>
<body>

<div class="ticket created-by-anniedotexe">
	<div class="left">
		<div class="image">
			<p class="admit-one">
				
				<span>{{ticket_type}}</span>
				
			</p>
			<div class="ticket-number">
				<p>
					{{ticket_id}}
				</p>
			</div>
		</div>
		<div class="ticket-info">
			<p class="date">
				<span>${userInfo.day}</span>--
				<span class="june-29">${userInfo.month}</span>
				<span>${userInfo.year}</span>
			</p>
			<div class="show-name" style="display: flex; flex-direction: column;">
				<h1>{{name}}</h1>
                <div>
                    <span>student: </span>
                    <span>{{student}}</span>
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
			<span>${userInfo.ticket_type}</span>
			<span>${userInfo.ticket_type}</span>
			<span>${userInfo.ticket_type}</span>
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
	
</body>
</html>
          <div className = "ticket" >
      <h1>Ticket ${user + 1}</h1>
      <p>Name: ${userInfo.name}</p> 
      <p>Age: ${userInfo.age}</p> 
      <p>Indian: ${userInfo.indian}</p>
      <p>Student: ${userInfo.student}</p>
      <p>Ticket_type: ${userInfo.ticket_type}</p>
      <p>Date: ${userInfo.day}-${userInfo.month}-${userInfo.year} </p>
      </div > `

        // ticketViewer.parentElement.classList.remove("disappear");
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
