// Afficher les messages du chat avec l'heure
function displayMessage(message, sender, time) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    const messageParagraph = document.createElement('p');
    // Ajouter le message et l'heure avec un retour à la ligne entre eux
    messageParagraph.textContent = `${message}\n${time}`;
    contentDiv.appendChild(messageParagraph);
    messageDiv.appendChild(contentDiv);

    if (sender === 'user') {
        messageDiv.classList.add('user-message');
    } else {
        messageDiv.classList.add('bot-message');
    }

    document.getElementById('chat-container').appendChild(messageDiv);
    document.getElementById('chat-container').scrollTop = document.getElementById('chat-container').scrollHeight;
}

  
  function sendMessage() {
    const userMessage = document.getElementById('userMessage').value;
    const userTime = new Date().toLocaleTimeString();
    displayMessage(userMessage, 'user', userTime);
  
    // Vérifier s'il y a déjà un indicateur de chargement dans le chat
    const existingLoadingIndicator = document.querySelector('.loading-indicator');
    if (!existingLoadingIndicator) {
        // Ajouter un nouvel indicateur de chargement seulement s'il n'existe pas déjà
        const loadingIndicator = document.createElement('p');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.textContent = 'Sending...';
        document.getElementById('chat-container').appendChild(loadingIndicator);
    }
  
    // Envoyer une requête à l'API
    fetch('/send_message', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: userMessage }),
    })
    .then((response) => response.json())
    .then((data) => {
        const botResponse = data.response;
        const time = data.time;
        const botTime = new Date().toLocaleTimeString();
        displayMessage(botResponse, 'bot', botTime);
    })
    .catch((error) => {
        console.error('An error occurs:', error);
        const errorMessage = error.message || "Network error. Please retry.";
        displayMessage(errorMessage, 'bot');
    })
    .finally(() => {
        // Cacher l'indicateur de chargement une fois la réponse reçue ou en cas d'erreur
        const loadingIndicator = document.querySelector('.loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    });
    
    document.getElementById('userMessage').value = '';
  }
  
  
  
//   function handleEnterKey(event) {
//     if (event.key === 'Enter') {
//         event.preventDefault();
//         sendMessage();
//     }
// }
  
    //document.getElementById('userMessage').addEventListener('keypress', handleEnterKey);

    document.getElementById('sendButton').addEventListener('click', function() {
        sendMessage();
        //document.getElementById('userMessage').removeEventListener('keypress', handleEnterKey);
    });
  document.body.addEventListener('scroll', function (e) {
    e.preventDefault();
  });
  