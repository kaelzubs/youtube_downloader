document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.getElementById('#loading').style.visibility = 'visible'
        }
    }
}