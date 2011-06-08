var random_background = (function() {
    var _images = [
    '4120/4778132344_2acfac5e56_b.jpg',
    '4073/4778132490_ff3d47c118_b.jpg',
    '2398/2289721254_a6d5cc2eb6_b.jpg',
    '28/55514402_a520e49f3b_b.jpg',
    '21/31090286_4f658e6c4a_o.jpg',
    '1415/5110569837_1e235f1a6f_b.jpg',
    '5163/5310825607_652a5c9c61_b.jpg',
    '2418/1988668999_6bc9f462ff_b.jpg',
    '2163/2038844404_a56d84b1e7_b.jpg',
    ];

    function random() {
        var d = new Date();
        // Change the picture every 30 seconds.
        var ticks = (d.getMinutes() * 60 + d.getSeconds()) / 30;

        return Math.floor(ticks % _images.length);

    }

    return function(element) {
        var url = ('http://static.flickr.com/' +
                   _images[random()]);
        console.debug(url);

        element.css({
                'background': 'url(' + url + ') no-repeat center center fixed',
                '-webkit-background-size': 'cover',
                '-moz-background-size': 'cover',
                '-ms-background-size': 'cover',
                '-o-background-size': 'cover',
                'background-size': 'cover',
            });
    }
})();
