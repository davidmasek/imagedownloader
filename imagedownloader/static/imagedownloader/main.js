$(document).ready(function(){
    var form = $('#main-form');
    var down_form = $('#down-form');
    // var urlIn = form.find('#url-in');

    var bar = $('#bar'); // progress bar
    var results = $('#results');
    var download = $('#download');
    var downloadBtn = $('#download-btn');
    var urls_div = $('#urls-div');

    // var all_urls = [];

    downloadBtn.click(function (event) {
        down_form.submit();
    });

    // function download_all (urls) {
    //     if (urls.length == 0) {
    //         return;
    //     };

    //     $.ajax({
    //         type: 'post',
    //         url: 'down',
    //         data: $('#down-form').serialize() + '&' + $.param(urls),
    //         success: function (data) {
    //             console.log(data);
    //         },
    //         error: function(data) {
    //             server_error();
    //             console.log(data);
    //         }
    //     });
    // }

    form.submit(function (event) {
        event.preventDefault();

        download.attr('class', 'row well');
        results.text('');
        bar_searching();

        $.ajax({
            type: 'post',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data) {
                // all_urls = data['urls'];
                preview_all(data['urls']);
            },
            error: function(data) {
                if(data['status'] === 400) {
                    invalid_url();
                } else {
                    server_error();
                }
            }
        });
        return false;
    });

    function preview_all (urls) {
        if (urls.length == 0) {
            bar_no_images();
            return;
        }

        urls_div.html('');

        start_preview(urls, 0);
    }

    function start_preview(urls, current) {
        preview(urls, current);

        current += 1;
        bar_working(urls.length, current);

        if (current < urls.length) {
            setTimeout(start_preview, 0, urls, current);
        }
    }

    function preview (urls, current) {
        var src = urls[current];
        var img = $('<a href="#" class="thumbnail"> \
                        <img src="' + src + '"> \
                    </a>');

        urls_div.append('<input type="hidden" \
            name="url[]" value="'+src+'"> ');


        results.append(img);
    }

    function bar_no_images (argument) {
        var text = 'No downloadable images found.';
        set_bar(100, 100, 'warning', 100, text);
    }

    function bar_searching() {
        var text = 'Searching...';
        set_bar(100, 50, 'info', 50, text);
    }

    function invalid_url () {
        var text = 'Invalid url.';
        set_bar(100, 100, 'danger', 100, text);
    }

    function server_error() {
        var text = 'Server error. Please try again later.';
        set_bar(100, 100, 'danger', 100, text);
    }

    function bar_complete() {
        set_bar(100, 100, 'success', 100, 'Complete.');
    }

    function bar_working(max, current) {
        var width = current / max * 100;
        var text = 'Preview: ' + current + '/' + max;
        set_bar(max, current, 'success', width, text);
    }

    function bar_downloading() {
        var text = 'Preparing download...';
        set_bar(100, 100, 'success', 100, text);
    }

    function set_bar (max, current, style, width, text) {
        bar.attr({
            'class': 'progress-bar progress-bar-'+style,
            'aria-valuenow': current,
            'aria-valuemin': 0,
            'aria-valuemax': max,
            'style': 'width: '+width+'%',
        });
        bar.text(text);
    }
});