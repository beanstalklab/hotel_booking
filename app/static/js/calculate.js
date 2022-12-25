var sum = 0;
function service() {
    var service1 = document.querySelector("input[id=service1]");
    var service2 = document.querySelector("input[id=service2]");
    var service3 = document.querySelector("input[id=service3]");
    var service4 = document.querySelector("input[id=service4]");
    var service5 = document.querySelector("input[id=service5]");
    var service6 = document.querySelector("input[id=service6]");


    service1.addEventListener('change', function () {
        if (this.checked) {
            sum += 100
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 100
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });

    service2.addEventListener('change', function () {
        if (this.checked) {
            sum += 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });

    service3.addEventListener('change', function () {
        if (this.checked) {
            sum += 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });

    service4.addEventListener('change', function () {
        if (this.checked) {
            sum += 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });

    service5.addEventListener('change', function () {
        if (this.checked) {
            sum += 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });

    service6.addEventListener('change', function () {
        if (this.checked) {
            sum += 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        } else {
            sum -= 200
            document.getElementById("calc-service").innerHTML = sum + "$";
        }
    });
}

service()

function clear() {
    document.getElementById("calc-service").innerText = '';
}


function calc() {
    const starDay = document.getElementById('start-date').value;
    const endDay = document.getElementById('end-date').value;

    const price = document.getElementById('price').innerText;

    const days = numOfDays(starDay, endDay)

    document.getElementById("calc-room").innerHTML = days * price + "đ";
    document.getElementById("calc-all").innerHTML = days * price + "đ";
    document.getElementById("calc-all").innerHTML = days * price + sum;

}


function numOfDays(starDay, endDay) {
    let start = new Date(starDay);
    let end = new Date(endDay);

    let millisBetween = Number(start.getTime() - end.getTime());

    let days = millisBetween / (1000 * 3600 * 24);

    return Math.round(Math.abs(days));
}



