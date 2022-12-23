function setSlide(number){
    clearSelected();
    currentSlide(number);
    document.querySelectorAll('.demo')[number-1].style.borderBottom = "6px solid purple";
 }
 function clearSelected(){
    Array.from(document.querySelectorAll('.demo')).forEach(item=>item.style.borderBottom="");
 }
 document.querySelector(".prev-img").addEventListener("click", () => {
    changeSlides(-1);
 });
 document.querySelector(".next-img").addEventListener("click", () => {
    changeSlides(1);
 });
 var slideIndex = 1;
 showSlides(slideIndex);
 function changeSlides(n) {
    showSlides((slideIndex += n));
 }
 function currentSlide(n) {
    showSlides((slideIndex = n));
 }
 function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {
       slideIndex = 1;
    }
    if (n < 1) {
       slideIndex = slides.length;
    }
    Array.from(slides).forEach(item => (item.style.display = "none"));
    slides[slideIndex - 1].style.display = "block";
 }