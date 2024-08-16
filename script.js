document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submitButton').addEventListener('click', () => {
        const sessionId = document.getElementById('sessionId').value;
        const deviceId = document.getElementById('deviceId').value;
        const iid = document.getElementById('iid').value;
        const lastUsername = document.getElementById('lastUsername').value;
        const newUsername = document.getElementById('newUsername').value;

        fetch('/change_username', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                device_id: deviceId,
                iid: iid,
                last_username: lastUsername,
                new_username: newUsername
            }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = data.result;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'An error occurred. Please try again.';
        });
    });
});
