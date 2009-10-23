
function printWidget(args) {
    var output = "<h3>Eventos para este mes</h3><ul>";
    for (var x=0; x<args.length; x++) {
        output += "<li><a href='"+ args[x].fields.url +"'>"+args[x].fields.body+"</a></li>";
    }
    output += "</ul><a href='http://www.linux.org.pe/eventos/' class='more'>m&aacute;s eventos</a>";
    document.getElementById('plugbullet_widget').innerHTML = output;
    style = document.createElement('link');
    style.href='/media/widget.css';
    style.rel = 'stylesheet';
    style.type = 'text/css';
    document.getElementsByTagName('head')[0].appendChild(style);
}

