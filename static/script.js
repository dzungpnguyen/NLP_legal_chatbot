var conversations = []; // Stocke les conversations

        function createConversation() {
            var newConversation = { messages: [] };
            conversations.push(newConversation);
            var option = document.createElement('option');
            option.value = conversations.length - 1;
            option.text = 'Conversation ' + conversations.length;
            document.getElementById('conversationSelect').add(option);
        }

        function loadConversation(index) {
            var chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = '';
            conversations[index].messages.forEach(function(message) {
                chatbox.innerHTML += message + '<br>';
            });
        }

        function sendMessage() {
            var input = document.getElementById('userInput');
            var chatbox = document.getElementById('chatbox');
            var selectedConversation = document.getElementById('conversationSelect').value;
            var message = 'User: ' + input.value;
            console.log(message);
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
                console.log(typeof data)
                var botMessage = 'Bot: ' + data.response;
                chatbox.innerHTML += message + '<br>';
                chatbox.innerHTML += botMessage + '<br>';
                conversations[selectedConversation].messages.push(message);
                conversations[selectedConversation].messages.push(botMessage);
            })
            .catch((error) => {
                console.log('Error:', error);
                console.error('Error:', error);
            });
            
            
        }