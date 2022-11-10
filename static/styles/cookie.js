
var fn = document.getElementById('cookie-consent')

fn.onclick = function click() {
    document.cookie = "cookie_consent=true";
    document.getElementById('cookie-consent-container').style.visibility = 'hidden';
}