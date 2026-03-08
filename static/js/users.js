let cart = [];
let totalAmount = 0;


function selectItem(name, qty, price, image){

    let exists = cart.find(item => item.name === name);

    if(exists){
        alert("Item already selected");
        return;
    }

    let total = qty * price;

    cart.push({
        name: name,
        qty: qty,
        total: total,
        image: image
    });

    updateCart();
}

function removeItem(name){
    cart = cart.filter(item => item.name !== name);
    updateCart();
}

function updateCart(){

    let body = document.getElementById("cartBody");
    body.innerHTML = "";

    totalAmount = 0;

    cart.forEach(item => {

        let row = `
        <tr>
            <td><img src="${item.image}" class="item-img"></td>
            <td>${item.name}</td>
            <td>${item.qty}</td>
            <td>₹${item.total}</td>
            <td><button onclick="removeItem('${item.name}')">Remove</button></td>
        </tr>
        `;

        body.innerHTML += row;
        totalAmount += item.total;
    });

    document.getElementById("total").innerText = totalAmount;
}

function openPopup(){
    if(cart.length === 0){
        alert("Select items first!");
        return;
    }

    document.getElementById("popup").style.display="flex";
}