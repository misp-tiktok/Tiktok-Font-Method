document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // For demo purposes only: send login data to a server to handle authentication
    fetch('https://your-server.com/login', {  // Replace with your server's endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.sessionId) {
            // Display the session ID and allow copying
            document.getElementById('sessionId').value = data.sessionId;
            document.getElementById('status').textContent = 'Session ID retrieved. You can now copy it.';
        } else {
            document.getElementById('status').textContent = 'Failed to retrieve Session ID.';
        }
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Error occurred. Please try again.';
        console.error('Error:', error);
    });
});

// Function to copy text to clipboard
document.getElementById('copyBtn').addEventListener('click', () => {
    const sessionIdText = document.getElementById('sessionId').value;
    navigator.clipboard.writeText(sessionIdText).then(() => {
        document.getElementById('status').textContent = 'Session ID copied!';
    }, (err) => {
        document.getElementById('status').textContent = 'Failed to copy Session ID.';
        console.error('Could not copy text: ', err);
    });
});
