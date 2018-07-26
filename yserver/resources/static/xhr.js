var timeout;
var stats_element = "#stats";
var url = "http://192.168.1.42:7099/stats";
var ms = 1000*60*1;

function loop () {
    $.ajax(url, {
        dataType: 'json',
        cache: false,
        success: function (data, s, xhr) {
            text_stats("Up: " + data.up + " Down: " + data.down + " Ratio: " + data.ratio);
            timeout = setTimeout(loop, ms);
        },
        error: function (xhr, s, t) { 
            if (xhr.status == 404) {
                /* 404: Retry soon, I guess */
                throw "404 :( " + xhr.status
                timeout = setTimeout(loop, ms);
            } else {
                $("#favicon").attr("href","err.png");
                throw "Unknown AJAX Error (status " + xhr.status + ")";
                timeout = setTimeout(loop, ms);
            }
        }
    });
}

function error(what) {
    $(stats_element).text("An error occured :-(.\r\n" +
                     "Reloading may help; no promises." +
                     what);
    $("#favicon").attr("href","err.png");

    return false;
}


function text_stats(thetext) { 
    $(stats_element).text(thetext);
}

$(document).ready(function () {
    window.onerror = error;

    /* Start */
    loop();
});

