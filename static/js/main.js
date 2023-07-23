window.addEventListener('scroll', function () {
    var header = document.querySelector('header');


    if (window.scrollY > 100) {
        header.style.backgroundColor = '#93b2eb';
    } else {
        header.style.backgroundColor = '#eff4fd';
    }
});
