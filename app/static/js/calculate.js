var sum = 0;
function service() {
    var service1 = document.querySelector("input[id=service1]");
    var service2 = document.querySelector("input[id=service2]");
    var service3 = document.querySelector("input[id=service3]");





    service1.addEventListener('change', function () {
        if (this.checked) {
            sum += 500000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        } else {
            sum -= 500000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        }
        let calc_service = document.getElementById("calc-service").innerHTML;
        document.getElementById("calc-service").innerHTML = calc_service.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');
    });

    service2.addEventListener('change', function () {
        if (this.checked) {
            sum += 200000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        } else {
            sum -= 200000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        }
        let calc_service = document.getElementById("calc-service").innerHTML;
        document.getElementById("calc-service").innerHTML = calc_service.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');
    });

    service3.addEventListener('change', function () {
        if (this.checked) {
            sum += 1000000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        } else {
            sum -= 1000000
            document.getElementById("calc-service").innerHTML = sum + " VNĐ";
        }
        let calc_service = document.getElementById("calc-service").innerHTML;
        document.getElementById("calc-service").innerHTML = calc_service.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');
    });

}

service()

function clear() {
    document.getElementById("calc-service").innerText = '';
}


function calc() {
    const starDay = document.getElementById('start-date').value;
    const endDay = document.getElementById('end-date').value;

    const price = document.getElementById('price').innerHTML.replaceAll(' ', '');
    console.log(price);

    const days = numOfDays(starDay, endDay)

    document.getElementById("days").innerHTML = days + " đêm";
    document.getElementById("calc-room").innerHTML = days * price + " VNĐ";
    document.getElementById("calc-all").innerHTML = days * price + sum + " VNĐ";


    let calc_room = document.getElementById("calc-room").innerHTML;


    let calc_all = document.getElementById("calc-all").innerHTML;

    document.getElementById("calc-room").innerHTML = calc_room.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');
    document.getElementById("calc-all").innerHTML = calc_all.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');

}


function numOfDays(starDay, endDay) {
    let start = new Date(starDay);
    let end = new Date(endDay);

    let millisBetween = Number(start.getTime() - end.getTime());

    let days = millisBetween / (1000 * 3600 * 24);
    document.getElementById("days").innerHTML = days;
    return Math.round(Math.abs(days));
}


