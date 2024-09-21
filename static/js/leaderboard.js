document.addEventListener('DOMContentLoaded', function() {
    fetch('/leaderboard')
        .then(response => response.json())
        .then(data => {
            const leaderboard = document.getElementById("leaderboard");
            leaderboard.innerHTML = ""; // Clear existing content
            data.forEach(user => {
                const li = document.createElement("li");
                li.textContent = `${user.name}: ${user.points} points`; // Constructing HTML element
                leaderboard.appendChild(li); // Adding the constructed element to the DOM
            });
        })
        .catch(error => console.error('Error fetching leaderboard:', error));
});
