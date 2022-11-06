document.onreadystatechange = function() {
    window.onload = (e) => {
        if (document.readyState !== "complete") {
            document.getElementById('#loading').hidden = false
        }
    }
}

document.onreadystatechange = function() {
    var fn = function () {
        document.cookie = "cookie_consent=true";
        document.getElementById('cookie-consent-container').hidden = true;
    };
    document.getElementById('cookie-consent').onclick = fn;
}


document.onreadystatechange = function() {
    //cache your selector
    setTimeout(function() {
        document.querySelector("#cookie-consent-container").hidden = false
    }, 5000);
}