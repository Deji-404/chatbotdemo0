document.addEventListener('DOMContentLoaded', async function() {
    /**
    const chatlog = document.getElementById('chatlog');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get user input
        const userMessage = userInput.value;

        // Clear the input field
        userInput.value = '';

        // Add the user message to the chat log
        chatlog.innerHTML += '<p class="user-message">' + userMessage + '</p>';

        data = 'user_input=' + encodeURIComponent(userMessage);

        $.post('/chatbot/', 
            data,
            function(data, status) {
                // Add the bot response to the chat log
                chatlog.innerHTML += '<p class="bot-message">' + data.bot_response + '</p>';
                // Scroll to the bottom of the chat log
                chatlog.scrollTop = chatlog.scrollHeight;
            }
        )
        */
        /**
        // Send the user message to the server and get the response
        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'user_input=' + encodeURIComponent(userMessage)
        })
        .then(response => response.json())
        .then(data => {
            // Add the bot response to the chat log
            chatlog.innerHTML += '<p class="bot-message">' + data.bot_response + '</p>';
            // Scroll to the bottom of the chat log
            chatlog.scrollTop = chatlog.scrollHeight;
        });
        
    });
    */

    const get_history = async () => {

        $.ajax({
            url: 'get-history/',
            type: "GET",
            dataType: "json",
            success: (data) => {
                console.log(data)  
              chats = data.get_history;
              chats.forEach((item) => {
                
                populateHistory(item)
              })
            },
            error: (error) => {
              console.log(error);
            }
          });
          
    }

    console.log("here")
    await get_history();
});

const populateHistory = (item) => {
    const chatDiv = $("#chatDiv");
    
    let convo = `
        <li class="list-group-item d-flex justify-content-between align-items-start p-2 mb-3">
            <div class="ms-2 me-auto">
                <div class="fw-bold"><i class="bi bi-person-circle"></i></div>
                ${item.messageInput}
            </div>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-start p-2 mb-3 text-bg-secondary">
            <div class="ms-2 me-auto">
                <div class="fw-bold">Bot <i class="bi bi-robot"></i></div>
                ${item.bot_response}
            </div>
        </li>
    `
    chatDiv.append(convo)
     
}

const populateMessage = (item) => {
    const chatDiv = $("#chatDiv");
    
    let convo = `
        <li class="list-group-item d-flex justify-content-between align-items-start p-2 mb-3">
            <div class="ms-2 me-auto">
                <div class="fw-bold"><i class="bi bi-person-circle"></i></div>
                ${item}
            </div>
        </li>
        `
    chatDiv.append(convo)
}

const populateResponse = (item) => {
    const chatDiv = $("#chatDiv");
    
    let convo = `
        <li class="list-group-item d-flex justify-content-between align-items-start p-2 mb-3 text-bg-secondary">
            <div class="ms-2 me-auto">
                <div class="fw-bold">Bot <i class="bi bi-robot"></i></div>
                ${item}
            </div>
        </li>
        `
    chatDiv.append(convo)
}


const sendMessage = async () => {
    //this.elementFromPoint.preventDefault();
    messageInput = $("#exampleFormControlTextarea1");
    message = messageInput.val();
    messageInput.val('')
    populateMessage(message);

    data = 'user_input=' + encodeURIComponent(message);

    $.ajax({
        url: 'send-message/',
        type: "POST",
        dataType: "json",
        data,
        success: (data) => {
            bot_response = data.bot_response;
            console.log(bot_response);
            populateResponse(bot_response)
        },
        error: (error) => {
          console.log(error);
        }
    });
}
