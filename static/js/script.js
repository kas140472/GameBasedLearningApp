let users = [
    { name: "User1", points: 50 },
    { name: "User2", points: 30 }
];

document.getElementById('completeModuleBtn').addEventListener('click', () => {
    const userIndex = Math.floor(Math.random() * users.length);
    users[userIndex].points += 10;

    updateLeaderboard();
});

function updateLeaderboard() {
    const leaderboard = document.getElementById("leaderboard");
    leaderboard.innerHTML = "";
    users.forEach(user => {
        const li = document.createElement("li");
        li.textContent = `${user.name}: ${user.points} points`;
        leaderboard.appendChild(li);
    });
}