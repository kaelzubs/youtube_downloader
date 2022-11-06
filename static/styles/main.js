document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.getElementById('#loading').style.visibility = 'visible'
        } else {
            document.getElementById('#loading').style.visibility = 'hidden'
        }
    }
}


var fn = function () {
    document.cookie = "cookie_consent=true";
    document.getElementById('cookie-consent-container').hidden = true;
};
document.getElementById('cookie-consent').onclick = fn;


//cache your selector
setTimeout(function() {
    document.querySelector("#cookie-consent-container").style.visibility = 'visible'
}, 5000);