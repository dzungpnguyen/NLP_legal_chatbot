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
            chatbox.innerHTML += message + '<br>';
            conversations[selectedConversation].messages.push(message);
            input.value = '';
            // Ici, vous pouvez ajouter le code pour envoyer le message à votre chatbot et afficher la réponse
        }