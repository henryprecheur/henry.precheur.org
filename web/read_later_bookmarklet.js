function check_username(user_input) {
    var label_required = $('label#required');

    if (!user_input.val()) {
        if (!label_required.length) {
            var req = $('<label id="required" for="user" ' +
                    'style="color: red; float: left"> ' +
                    '&#8592; Required</label>');
            req.insertAfter(user_input);
        }
        user_input.focus();
        return false;
    } else {
        label_required.remove();
    }
    return true;
}

function generate() {
    var user_input = $('input#user');

    if (!check_username(user_input)) {
        return false;
    }

    var tags = $('#tags').val();

    var url = 'javascript:' +
        'var a=encodeURIComponent;' +
        'location.href="http://delicious.com/save?' +
        'user=' + encodeURIComponent(user_input.val()) +
        '&url="+a(location.href)+"&title="+a(document.title)+"&' +
        (tags ? 'tags=' + encodeURIComponent(tags) : '') +
        '&share=no&jump=yes&notes="+a(window.getSelection());';
    $('#bm-link').attr('href', url).text('Read later');
    $('#bm-comment').html(" &#8592; Drag this link into your bookmark toolbar");
    return false;
}
