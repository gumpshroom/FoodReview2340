clicked = false
anime({
        targets: 'article',
        opacity: 1,
        duration: 1000,
        easing: 'cubicBezier(.5, .05, .1, .3)'
    });
document.getElementById(('search')).addEventListener('click', function() {
    console.log("expand search")
    anime({
        targets: 'div#search',
        backgroundColor: '#FFF',
        duration: 500,
        width: '60%',
    });
    clicked = true
})
document.onclick = function(e) {
    console.log(e.target.id)
    if (e.target.id !== 'search' && e.target.id !== 'searchInput' && clicked) {
        anime({
            targets: 'div#search',
            backgroundColor: '#FFF',
            duration: 500,
            width: '40%',
        });
    }

}