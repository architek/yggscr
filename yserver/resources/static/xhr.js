var timeout;
var stats_element = "#stats_txt";
var url = "/stats";
var ms = 1000*60*15;
var modp = 0;

jQuery.fn.fade_inout = function(speed) {
    $(this).fadeIn('slow', function(){
        $(this).fadeOut(speed,function(){
            $(this).remove();
        })
    });
}

var off=0;
function disp_msg_fade(msg) {
    var msgModal = '<div id="mod-cont">'+msg+'</div>';
    $('#modal').append(msgModal);
    $('#mod-cont').fade_inout(2500);
}
function prog_fade(msg, ndelay) {
    setTimeout(function() {
        disp_msg_fade(msg);
    }, off);
    off = off + ndelay;
}

function loop () {

    $.ajax(url, {
        dataType: 'json',
        cache: false,
        success: function (data, s, xhr) {
            update_stats_text(data);
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

function update_stats_text(data) {
    var date = new Date();
    var time = date.getHours().toString().padStart(2,"0") + ":" + date.getMinutes().toString().padStart(2,"0")+ ":" + date.getSeconds().toString().padStart(2,"0");
    var progs = ["-", "\\","|","/"];
    var prog = progs[modp++%progs.length];
    $(stats_element).text(prog+" Up(MB):"+data.up+" Down(MB):"+data.down+" Ratio:"+data.ratio+ " Mean Up Speed (KBps):"+data.m_up+" Mean Down Speed (KBps):"+data.m_down+" @ "+time);
}

function error(what) {
    $(stats_element).text("An error occured :-(.\r\n" +
                     "Reloading may help; no promises." +
                     what);
    $("#favicon").attr("href","err.png");

    return false;
}

function text_stats(thetext) { 
}

$(document).ready(function () {
    window.onerror = error;

    /* Start */
    tpl_disp_message();
    loop();
});
$(window).focus(function() {
    $("#favicon").attr("href","");
});
