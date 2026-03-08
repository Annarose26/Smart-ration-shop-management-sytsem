const reports = [
    {
        title: "Biometric Machine Not Working",
        description: "Fingerprint scanner is not detecting properly.",
        name: "Rajesh Kumar",
        card: "APL12345"
    },
    {
        title: "Kerosene Not Supplied",
        description: "Kerosene not available for last 5 days.",
        name: "Anitha P",
        card: "BPL56789"
    },
    {
        title: "Poor Quality Rice",
        description: "Rice contains stones and dust.",
        name: "Suresh Nair",
        card: "AAY88990"
    },
    {
        title: "Long Waiting Time",
        description: "Waiting more than 2 hours for distribution.",
        name: "Meera Das",
        card: "OTH12390"
    },
    {
        title: "Incorrect Quantity Provided",
        description: "Sugar quantity is less than fixed quota.",
        name: "Abdul Rahman",
        card: "BPL11223"
    }
];

function loadReports(){

    let container = document.getElementById("reportContainer");
    container.innerHTML = "";

    reports.forEach(report => {

        let now = new Date();
        let date = now.toLocaleDateString();
        let time = now.toLocaleTimeString();

        let box = `
        <div class="report-box">
            <h3>${report.title}</h3>
            <p>${report.description}</p>
            <div class="details">
                <span><b>Name:</b> ${report.name}</span>
                <span><b>Card No:</b> ${report.card}</span>
                <span><b>Date:</b> ${date}</span>
                <span><b>Time:</b> ${time}</span>
            </div>
        </div>
        `;

        container.innerHTML += box;
    });
}

window.onload = loadReports;
