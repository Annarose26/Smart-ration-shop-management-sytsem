function signup(){

    const username =
        document.getElementById("signup-username").value;

    const password =
        document.getElementById("signup-password").value;

    fetch("/signup",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            username:username,
            password:password

        })

    })
    .then(res=>res.json())
    .then(data=>{

        if(data.status=="success"){

            alert("Signup successful");
            window.location.href="/login";

        }else{

            alert(data.message);

        }

    });

}
