// var fn = function () {
//     document.cookie = "cookie_consent=true";
//     if (document.cookie == true) {
//         document.getElementById('cookie-consent-container').hidden = true;
//     }  
// };
// document.getElementById('cookie-consent').onclick = fn;


const fn = document.getElementById('cookie-consent');

if (fn) {
    fn.onclick = () => {
        document.cookie = 'cookie_consent=true';
        document.getElementById('cookie-consent-container').hidden = true
    }
}

