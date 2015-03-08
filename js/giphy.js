var pizza = "PIZZAAAAAAA"

var part1 = "http://api.giphy.com/v1/gifs/search?q="
var part2 = "&api_key=dc6zaTOxFJmzC"


var swear = "fuck"

var apicall = part1+swear+part2


$.getJSON(apicall, function(data) {
    console.log(data);
var img = $( '<img id="image">');
});
