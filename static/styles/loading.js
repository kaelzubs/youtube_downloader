document.onreadystatechange = function() {
    window.onload = () => {
        if (document.readyState == "complete") {
            if (document.querySelector('.loading_css')) {
                document.querySelector('.loading_css').style.visibility = 'hidden';
            }
            
        }
    }
}