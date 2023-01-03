
let nodeList = document.querySelectorAll(".fomat-money"); 

for (let i = 0; i < nodeList.length; i++) {
    nodeList[i].innerHTML = nodeList[i].innerHTML.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ');
}
