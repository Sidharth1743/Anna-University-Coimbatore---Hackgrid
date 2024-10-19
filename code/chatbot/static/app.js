document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);

        const messageContent = document.createElement('p');
        messageContent.textContent = content;

        messageDiv.appendChild(messageContent);
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;  // Auto-scroll to the latest message
    }

    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        appendMessage('user', userMessage);

        // Clear input field
        userInput.value = '';

        // Send user input to the backend
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();

            // Append assistant response to the chat history
            appendMessage('assistant', data.reply);
        } catch (error) {
            appendMessage('assistant', 'Sorry, something went wrong.');
        }
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }

    // Attach event listener to the input field
    userInput.addEventListener('keypress', handleKeyPress);

    // Attach event listener to the send button
    document.querySelector('button').addEventListener('click', sendMessage);
});