
const showSearchResults = (data) => {
    console.log(data)
}

const searchHandler = (elem) => {
    
    const query = $("#query").val();
    const searchPayload = { query: query };
    $.ajax(url, {
        data : JSON.stringify(query),
        contentType : 'application/json',
        type : 'POST'})
        .done(showSearchResults)
}

$("#search").on("click", searchHandler);