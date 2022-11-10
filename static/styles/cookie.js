
var fn = document.getElementById('cookie-consent')

fn.onclick = function() {
    document.cookie = "cookie_consent=true";
    document.getElementById('cookie-consent-container').hidden = true
}