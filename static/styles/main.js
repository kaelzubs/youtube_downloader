
document.onreadystatechange = function() {
    window.onload = (e) => {
        document.querySelector("#loading").style.visibility = "hidden"
        if (document.readyState !== "complete") {
            document.querySelector("#loading").style.visibility = "visible";
        } else {
            document.querySelector("#loading").style.visibility = "hidden"
        }
    }
}

function loading() {
    document.querySelector('#loading').style.visibility = 'visible'
    window.location.href='/'
}
