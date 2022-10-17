document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.querySelector('#loading').style.visibility = 'visible'
        } else {
            document.querySelector('#loading').remove()
        }
    }
}

document.querySelector('body').getAttribute('spellcheck', false)