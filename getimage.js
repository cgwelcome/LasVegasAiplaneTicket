var page = require('webpage').create();
var args = require('system').args

page.onError = function() {};

if (args.length != 2) {
    console.log("Invalid syntax");
    phantom.exit(1);
}

var website = args[1];
page.open(website, function() {
    window.setTimeout(function() {
        page.render('/dev/stdout', {format: 'png'});
        phantom.exit();
    }, 100)
});

