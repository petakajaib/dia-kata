
const showSearchResults = (data) => {
    console.log(data)
}

const searchHandler = () => {
    
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