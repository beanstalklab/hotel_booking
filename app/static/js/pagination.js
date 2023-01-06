function changePage() {
    const currentPage = document.querySelectorAll('.pagination li');
    console.log(currentPage);

    for (let i = 0; i < currentPage.length; i++) {
        currentPage[i].addEventListener('click', () => {
            $('.acti').addClass('activate');
        })
    }
}
changePage()