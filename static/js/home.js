// small fade-in effect for cards
window.onload = () => {
    const cards = document.querySelectorAll(".card");

    cards.forEach((card, i) => {
        card.style.opacity = 0;
        setTimeout(() => {
            card.style.transition = "0.5s";
            card.style.opacity = 1;
        }, i * 200);
    });
};
// Shop status
const openingHour = 9;  // 9 AM
const closingHour = 18; // 6 PM
function checkShopTime() {
    const now = new Date();
    const hours = now.getHours();
    const shopDiv = document.getElementById("shop-status");

    if(hours >= openingHour && hours < closingHour){
        shopDiv.textContent = `🟢 Shop is OPEN | Opening Hours: 09:00 - 18:00`;
        shopDiv.style.color = "green";
    } else {
        shopDiv.textContent = `🔴 Shop is CLOSED | Opening Hours: 09:00 - 18:00`;
        shopDiv.style.color = "red";
    }
}
setInterval(checkShopTime, 60000);
checkShopTime();

// Logout function
function logout(){
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
}
