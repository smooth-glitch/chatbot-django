document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatMessagesContainer = document.getElementById('chat-messages');

    sendButton.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleUserInput();
        }
    });

    async function handleUserInput() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        addMessage(userMessage, 'user-message');
        userInput.value = '';

        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ message: userMessage })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addMessage(data.response, 'bot-message');
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            addMessage('Sorry, there was an error processing your request.', 'bot-message');
        }
    }

    function addMessage(message, className) {
        const messageElement = document.createElement('div');
        messageElement.className = className;
        messageElement.textContent = message;

        if (className === 'user-message') {
            messageElement.style.textAlign = 'right';
            messageElement.style.backgroundColor = '#00d0ff';
            messageElement.style.color = '#0e1a2b';
        } else {
            messageElement.style.textAlign = 'left';
            messageElement.style.backgroundColor = '#00ff8f';
            messageElement.style.color = '#0e1a2b';
        }

        messageElement.style.borderRadius = '15px';
        messageElement.style.padding = '10px';
        messageElement.style.marginTop = '10px';
        messageElement.style.width = 'fit-content';
        messageElement.style.maxWidth = '60%';
        messageElement.style.animation = 'fadeIn 0.5s ease-in-out';

        chatMessagesContainer.appendChild(messageElement);
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }

    function toggleFAQ(element) {
        element.classList.toggle('active');
        const answer = element.nextElementSibling;
        if (answer.style.maxHeight) {
            answer.style.maxHeight = null;
        } else {
            answer.style.maxHeight = answer.scrollHeight + "px";
        }
    }

    function getCSRFToken() {
        let cookieValue = null;
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 'csrftoken'.length + 1) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                break;
            }
        }
        return cookieValue;
    }

    // FAQ Toggle Functionality
    document.querySelectorAll('.faq-question').forEach(item => {
        item.addEventListener('click', () => {
            const answer = item.nextElementSibling;
            answer.classList.toggle('active');
            answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
        });
    });
});
