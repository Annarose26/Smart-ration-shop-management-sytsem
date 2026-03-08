// Check login
const user = JSON.parse(localStorage.getItem("loggedInUser"));
if(!user){
    window.location.href = "login.html";
}

// Logout
function logout(){
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
}

// Live Date & Time
function updateDateTime(){
    const now = new Date();
    document.getElementById("datetime").textContent =
        now.toLocaleDateString() + " | " + now.toLocaleTimeString();
}
setInterval(updateDateTime, 1000);
updateDateTime();

// Shop Status
const openingHour = 9;
const closingHour = 18;

function checkShopTime(){
    const hour = new Date().getHours();
    const status = document.getElementById("shop-status");

    if(hour >= openingHour && hour < closingHour){
        status.textContent = "🟢 Shop is OPEN (9AM–6PM)";
        status.style.color = "green";
    } else {
        status.textContent = "🔴 Shop is CLOSED (9AM–6PM)";
        status.style.color = "red";
    }
}
checkShopTime();
