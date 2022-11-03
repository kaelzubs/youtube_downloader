document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.querySelector('#loading').style.visibility = 'visible'
        }
    }
    document.querySelector('#loading').remove()
}
