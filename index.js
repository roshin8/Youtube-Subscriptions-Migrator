var fs = require('fs'),
    childProc = require('child_process'),
    xml2js = require('xml2js');

var parser = new xml2js.Parser();
fs.readFile(__dirname + '/subscription_manager.xml', function (err, data) {
    parser.parseString(data, function (err, result) {
        var nodes = result.opml.body[0].outline[0].outline;

        nodes.forEach(function (node, index) {
            var url = node['$'].xmlUrl;
            url = url.substring(url.indexOf('=') + 1, url.length);
            var channel = 'https://www.youtube.com/channel/' + url;
            // https://www.youtube.com/subscription_center?add_user=

            if (index == 1) { // Safe Break only remove this when you are ready!
                childProc.exec('google-chrome ' + channel);
            }
        });
    });
});