document.getElementById('evenClick').addEventListener("click", activeButton);

function activeButton() {
    document.getElementById("pageActive").className += "active";
}

var change = document.getElementById("pageActive");
var activePage = change.getElementsByClassName("numPage");
for (var i = 0; i < activePage.length; i++) {
    activePage[i].addEventListener("click", function () {
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}