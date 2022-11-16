document.addEventListener('DOMContentLoaded', function() {
    let pasteButton = document.getElementsByTagName('button')[0];
    pasteButton.addEventListener('click', function () {
        navigator.clipboard
        .readText()
        .then(cliptext => (document.getElementById('clipboard-paste').innerText = cliptext), err => console.log(err));
    });
});