$(document).ready(function(){

//$("#popup").dialog({autoOpen:false});
function giphy(keyword) {
    var part1 = "http://api.giphy.com/v1/gifs/search?q="
    var part2 = "&api_key=dc6zaTOxFJmzC"

    var keyword = keyword

    var apicall = part1+keyword+part2
    var src = ""

    $.getJSON(apicall, function(data) {
        console.log(data);
        src = data['data']['0']['url']
    });
    $("#giphyimg").attr("src", 'http://media.'+src.substring(7)+'/giphy.gif')
}
});


