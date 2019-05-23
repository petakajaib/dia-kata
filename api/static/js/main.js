
const titleize = (sentence)=> {
    if(!sentence.split) return sentence;
    var _titleizeWord = function(string) {
            return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
        },
        result = [];
    sentence.split(" ").forEach(function(w) {
        result.push(_titleizeWord(w));
    });
    return result.join(" ");
}

const generateHTML = (data) => {
    const div = $('<div id="results"></div>');

    div.append(`<h3>Showing results for ${data.query}</h3>`);

    data.results.forEach(element => {
        div.append(`<div class="result_item"><a id="${element}" href="#${element}">${titleize(element)}</a></div>`)
    });

    return div;
}

const showSearchResults = (data) => {
    
    const resultsHTML = generateHTML(data);
    
    $("#content").html(resultsHTML);

}

const searchHandler = () => {
    
    
    $("#content").html("waiting...")
    
    const query = $("#query").val();
    const searchPayload = { query: query };

    $.ajax('/search/', {
        data : JSON.stringify(searchPayload),
        contentType : 'application/json',
        type : 'POST'})
        .done(showSearchResults)
}

const enterHandler = (event) => {
    const keycode = (event.keyCode ? event.keyCode : event.which);

    if(keycode == '13'){
        searchHandler()
    }
    
}

$("#search").on("click", searchHandler);
$("#query").on("keypress", enterHandler)