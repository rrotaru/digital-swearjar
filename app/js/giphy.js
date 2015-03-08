function giphy(keyword) {
    var part1 = "http://api.giphy.com/v1/gifs/search?q="
    var part2 = "&api_key=dc6zaTOxFJmzC"

    var keyword = keyword

    var apicall = part1+keyword+part2
    var src = ""

    $.getJSON(apicall, function(data) {
        console.log(data);
        src = data['data'][Math.floor(Math.random() * data['data'].length)]['embed_url']
    });
    setTimeout(function() {
    $("#giphyimg").attr("src", 'http://media.giphy.com/media/'+src.substring(23)+'/giphy.gif')
    }, 1000);
}
