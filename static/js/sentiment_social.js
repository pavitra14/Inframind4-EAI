var data = "";
var timer = "";
var timer_running = false;
var loader = '<img src="/static/imgs/ajax-loader2.gif" width="10%" alt="Processing">';
var output_area = $("#output_area");
var output_timer = $("#output_timer");

var h=0;
var m=0;
var s=0;

function genPieChart()
{
    values = data.values;
    colors = data.colors;
    labels = data.labels;
    overall = data.overall;
    var pieData = {
        "type": "doughnut",
        "data": {
          "labels": labels,
          "datasets" : [{
              "label": "Overall Analysis - " + overall,
              "data" : values,
              "backgroundColor": colors
          }]
        },
        options: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    fontColor: 'white'
                }
            }
        }
    };
    console.log(pieData);
    new Chart(document.getElementById("SentimentChart"), pieData);
    $("#SentimentChart").show();
}

function sendAjax(tweet_url)
{
    return $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/ajax/sentiment_social",
        data: {
            tweet_url: tweet_url
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

function doTweetAnalysis(tweet_url)
{
    startTimer();
    output_area.html("Tweet under processing..." + loader);
    $.when(sendAjax(tweet_url)).done(function(){
        output = data.data.replace(/(?:\r\n|\r|\n)/g, '<br>');
        alert('Processing Done!')
        output_area.html(output);
        stopTimer();
        genPieChart();

    });
}
$(function () {
    var t = setInterval(tick, 1000);

    $("form#video_form").on("submit", function(e){
        var tweet_url = $("#tweet_url").val();
        doTweetAnalysis(tweet_url);
        e.preventDefault();
        UIkit.modal("#search").hide();
    });
});