
document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.querySelector("#loading").style.visibility = "visible";
        }
    }
}

function loading() {
    document.querySelector('#loading').style.visibility = 'visible'
    window.location.href='/'
}
