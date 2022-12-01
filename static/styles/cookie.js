const fn = document.getElementById('cookie-consent');


window.addEventListener('DOMContentLoaded', (event) => {
    if (fn) {
        fn.onclick = () => {
            document.cookie = 'cookie_consent=true';
            document.getElementById('cookie-consent-container').hidden = true
        }
    }
});