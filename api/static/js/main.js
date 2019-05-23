const generateHTML = (data) => {
    const div = $('<div id="results"></div>');

    div.append(`<h3>Showing results for <em>"${data.query}"</em></h3>`);

    data.results.forEach(element => {
        div.append(`<div class="result_item"><a id="${element}" href="#${element}">${element.toUpperCase()}</a></div>`)
    });

    return div;
}

const showSearchResults = (data) => {
    
    const resultsHTML = generateHTML(data);
    
    $("#content").html(resultsHTML);

}

const searchHandler = () => {
    
    
    $("#content").html('<div id="results">Fetching results ...</div>')
    
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