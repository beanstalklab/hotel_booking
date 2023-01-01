textarea = document.querySelector("#body-text");
title = document.querySelector("#title");
textarea.addEventListener('input', autoResize, false);
title.addEventListener('input', autoResize, false);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}