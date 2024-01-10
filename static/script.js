var conversations = []; // Stocke les conversations

        function createConversation() {
            var newConversation = { messages: [] };
            conversations.push(newConversation);
            var option = document.createElement('option');
            option.value = conversations.length - 1;
            option.text = 'Conversation ' + conversations.length;
            document.getElementById('conversationSelect').add(option);
            document.getElementById('conversationSelect').value = conversations.length - 1;
            loadConversation(conversations.length - 1);
        }

        function loadConversation(index) {
            var chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = '';
            conversations[index].messages.forEach(function(message) {
                chatbox.innerHTML += message + '<br>';
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            var input = document.getElementById('userInput');
            var message = input.value
            var chatbox = document.getElementById('chatbox');
            var selectedConversation = document.getElementById('conversationSelect').value;
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: message
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                message = '<p class="user-message">😎: ' + message + '</p>';
                console.log(message)
                var botMessage = '<p class="bot-message">🤖: ' + data.response + '</p>';
                chatbox.innerHTML += message;
                chatbox.innerHTML += botMessage
                conversations[selectedConversation].messages.push(message);
                conversations[selectedConversation].messages.push(botMessage);
            })
            .catch((error) => {
                console.log('Error:', error);
                console.error('Error:', error);
            });
            document.getElementById('userInput').value = '';
            
        }