function showSection(id) {
    let sections = document.querySelectorAll(".section");
    sections.forEach(section => {
        section.style.display = "none";
    });

    let activeSection = document.getElementById(id);
    if (activeSection) {
        activeSection.style.display = "block";
    }
}

function toggleSidebar(){
    document.querySelector(".sidebar").classList.toggle("collapsed");
}

function logout(){
    window.location.href="login.html";
}

/* PIE CHART - STOCK STATUS */
new Chart(document.getElementById("stockChart"),{
    type:'pie',
    data:{
        labels:['Available','Low Stock','Out of Stock'],
        datasets:[{
            data:[60,25,15],
            backgroundColor:['#16a34a','#f59e0b','#dc2626']
        }]
    }
});

/* BAR CHART - BOOKING */
new Chart(document.getElementById("bookingChart"),{
    type:'bar',
    data:{
        labels:['APL','BPL','Other'],
        datasets:[{
            label:'Bookings',
            data:[30,40,12],
            backgroundColor:['#3b82f6','#8b5cf6','#6b7280']
        }]
    }
});

/* LINE CHART - CUSTOMER GROWTH */
new Chart(document.getElementById("customerChart"),{
    type:'line',
    data:{
        labels:['Jan','Feb','Mar','Apr','May','Jun'],
        datasets:[{
            label:'Customers',
            data:[20,35,50,65,90,120],
            borderColor:'#3b82f6',
            fill:false
        }]
    }
});
/* LOAD BOOKINGS INTO TABLE */
function loadBookings(){

    let bookings = JSON.parse(localStorage.getItem("bookings")) || [];
    let table = document.querySelector("#bookingTable tbody");
    table.innerHTML = "";

    bookings.forEach(b=>{
        let row = `
            <tr>
                <td>${b.cardNumber}</td>
                <td>${b.cardType}</td>
                <td>${b.date}</td>
                <td>${b.time}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

/* SHOW SECTION */
function showSection(id){

    document.querySelectorAll(".section").forEach(sec=>{
        sec.style.display="none";
    });

    document.getElementById(id).style.display="block";

    if(id === "booking"){
        loadBookings();
    }
}

/* SAVE NOTICE */
function saveNotice(){
    let notice = document.getElementById("noticeText").value;
    localStorage.setItem("notice", notice);
    document.getElementById("displayNotice").innerText = notice;
}

/* LOAD NOTICE ON PAGE LOAD */
window.onload = function(){
    let notice = localStorage.getItem("notice");
    if(notice){
        document.getElementById("displayNotice").innerText = notice;
    }
}
function addMember(event){
    event.preventDefault();

    let name = document.getElementById("memberName").value;
    let card = document.getElementById("memberCard").value;
    let type = document.getElementById("memberType").value;
    let mobile = document.getElementById("memberMobile").value;

    let member = { name, card, type, mobile };

    let members = JSON.parse(localStorage.getItem("members")) || [];
    members.push(member);

    localStorage.setItem("members", JSON.stringify(members));

    loadMembers();

    document.getElementById("memberForm").reset();
}

function loadMembers(){
    let members = JSON.parse(localStorage.getItem("members")) || [];
    let table = document.querySelector("#memberTable tbody");

    table.innerHTML = "";

    members.forEach(m=>{
        let row = `
        <tr>
            <td>${m.name}</td>
            <td>${m.card}</td>
            <td>${m.type}</td>
            <td>${m.mobile}</td>
        </tr>
        `;
        table.innerHTML += row;
    });
}

window.onload = function(){
    loadMembers();
};
