// var fn = function () {
//     document.cookie = "cookie_consent=true";
//     if (document.cookie == true) {
//         document.getElementById('cookie-consent-container').hidden = true;
//     }  
// };
// document.getElementById('cookie-consent').onclick = fn;


const fn = document.getElementById('cookie-consent');

fn.click = () => {
    document.cookie = 'cookie_consent=true'
    if(document.cookie) {
        document.getElementById('cookie-consent-container').hidden = true
    }
}