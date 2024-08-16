document.getElementById("changeUsernameForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const sessionId = document.getElementById("sessionId").value;
    const newUsername = document.getElementById("newUsername").value;

    fetch("/change-username", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sessionId, newUsername })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").textContent = data.message;
    })
    .catch(error => {
        document.getElementById("result").textContent = "An error occurred.";
        console.error("Error:", error);
    });
});
