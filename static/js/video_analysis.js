var data = "";
var timer = "";
var timer_running = false;
var loader = '<img src="/static/imgs/ajax-loader2.gif" width="10%" alt="Processing">';
var output_area = $("#output_area");
var output_timer = $("#output_timer");

var h=0;
var m=0;
var s=0;

function sendAjax(video_url)
{
    return $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/ajax/video_analysis",
        data: {
            video_url: video_url
        },
        success: function (response) {
            data = response;
        },
        error: function (err)
        {
            console.error(err);
        }
    });
}

function tick()
{
    if(!timer_running)
    {
        return;
    }
    h= parseInt(h);
    m= parseInt(m);
    s= parseInt(s);
    s++;
    if(s>=60){
        m++;
        s=0;
    }
    if(m>=60)
    {
        h++;
        m=0;
    }

    h = (h <10)?'0'+h:h;
    m = (m <10)?'0'+m:m;
    s = (s <10)?'0'+s:s;
    timer = h+':'+m+':'+s;
    output_timer.html(timer);
}
function startTimer()
{
    timer_running = true;
}

function stopTimer()
{
    timer_running = false;
}

function doVideoAnalysis(video_url)
{
    startTimer();
    output_area.html("Video under processing, please check back in some time for results, we'll alert you when it's done." + loader);
    $.when(sendAjax(video_url)).done(function(){
        output = data.replace(/(?:\r\n|\r|\n)/g, '<br>');
        alert('Video Processing Done!')
        output_area.html(output);
        stopTimer();
    });
}
$(function () {
    var t = setInterval(tick, 1000);

    $("form#video_form").on("submit", function(e){
        var video_url = $("#video_url").val();
        doVideoAnalysis(video_url);
        e.preventDefault();
        UIkit.modal("#search").hide();
    });
});