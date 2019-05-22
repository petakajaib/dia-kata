
const showSearchResults = (data) => {
    console.log(data)
}

const searchHandler = (elem) => {
    
    const query = $("#query").val();
    const searchPayload = { query: query };
    $.post("/search/", searchPayload)
        .done(showSearchResults);
}

$("#search").on("click", searchHandler);