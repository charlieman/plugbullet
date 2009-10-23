
function printWidget(args) {
    document.getElementById('plugbullet_widget').innerHTML = args;
    document.getElementById('plugbullet_widget').innerHTML = output;
    style = document.createElement('link');
    style.href='/media/widget.css';
    style.rel = 'stylesheet';
    style.type = 'text/css';
    document.getElementsByTagName('head')[0].appendChild(style);
}

