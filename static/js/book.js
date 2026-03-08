function submitForm(){

    const number = document.getElementById("cardNo").value;
    const type = document.getElementById("cardType").value;

    if(number === "1234" && type === "APL"){
        window.location.href = "/user1";
    }

    else if(number === "123" && type === "BPL"){
        window.location.href = "/user2";
    }

    else if(number === "12345" && type === "BPL"){
        window.location.href = "/user3";
    }

    else{
        alert("Invalid card details");
    }
}

function goHome(){
    window.location.href = "/home";
}
