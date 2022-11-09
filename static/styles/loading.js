document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState == "complete") {
            document.querySelector('.loading_css').style.visibility = 'hidden';
        }
    }
}