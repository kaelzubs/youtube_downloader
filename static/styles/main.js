
document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            $('#loading').show()
        } else {
            $('#loading').remove()
        }
    }
}
