// Function to get cookies by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        document.getElementById('status').textContent = 'Session ID copied!';
    }, (err) => {
        document.getElementById('status').textContent = 'Failed to copy Session ID.';
        console.error('Could not copy text: ', err);
    });
}

// Fetch the session ID from cookies
document.addEventListener('DOMContentLoaded', () => {
    const sessionId = getCookie('sessionid'); // Replace with the correct cookie name
    if (sessionId) {
        document.getElementById('sessionId').value = sessionId;
    } else {
        document.getElementById('sessionId').value = 'Session ID not found. Please log in and refresh.';
    }

    document.getElementById('copyBtn').addEventListener('click', () => {
        const sessionIdText = document.getElementById('sessionId').value;
        copyToClipboard(sessionIdText);
    });
});
