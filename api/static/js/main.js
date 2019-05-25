const generateResults = (data) => {
    const div = $('<div id="results"></div>');

    div.append(`<h3>Showing results for <em>"${data.query}"</em></h3>`);

    data.results.forEach(element => {
        div.append(`<div class="result_item">
                        <a class="result_element" href="#${element}" id="${element}">
                            ${element.toUpperCase()}
                        </a>
                    </div>`)
    });
    return div;
}

const showSearchResults = (data) => {
    
    const resultsHTML = generateResults(data);
    
    $("#content").html(resultsHTML);
    $("a.result_element").on("click", detailHandler);
    
}

const searchHandler = () => {
    
    
    $("#content").html('<h3 id="results">Fetching results ...</h3>')
    
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
        searchHandler();
    }
    
}

const generateInformationSection = (title, property_name, data) => {
    
    const informationSection = $(`<div class="information_section">
                                    <div class="section_title">
                                        ${title}
                                    </div>
                                  </div>`)
    
    const informationListing = $(`<div class="information_listing"></div>`)
    data[property_name].forEach(element => {
        let informationItem;

        switch (property_name) {
            case "mentioned_by":
            case "mentions":
            case "similar_entities":
                informationItem = $(`<span class="information_item">
                    <a class="result_element result_entry" href="#${element}" id="${element}">
                        ${element.toUpperCase()}
                    </a>
                   </span>`)
                informationListing.append(informationItem)
                break;
            case "keywords":
                informationItem = $(`<span class="information_item">
                                            ${element.toUpperCase()}
                                    </span>`)
                informationListing.append(informationItem)
            default:
                break;
        }

        
        
    })
    
    informationSection.append(informationListing)
    return informationSection;
}

const generateQuoteSection = (quotes) => {

    const quoteSection = $(`<div class="quote_section">
                                <div class="section_title">
                                    Quotes
                                </div>
                            </div>`)

    const quoteListing = $(`<div class="quote_listing"></div>`)

    quotes.forEach(element => {
        const listingContent = $(`<div class="listing_content"></div>`)
        listingContent.append(element.quote)
        listingContent.append(`<span class="source">
                                    <a class="source" href="${element.url}" target="_blank">
                                        source
                                    </a>
                               </span>`)
        quoteListing.append(listingContent)
    })
    quoteSection.append(quoteListing)
    return quoteSection
}

const showDetail = (data) => {

    const div = $('<div class="talker"></div>')
    const quoteSection = generateQuoteSection(data.quotes)
    const keywordsSection = generateInformationSection("Keywords", "keywords", data)
    const similarEntitiesSection = generateInformationSection("Similar Entities", "similar_entities", data)
    const mentionsSection = generateInformationSection("Mentions", "mentions", data)
    const mentionedBySection = generateInformationSection("Mentioned By", "mentioned_by", data)
    
    div.append($(`<div class="talker_name">${data.entity.toUpperCase()}</div>`))
    div.append(quoteSection)
    div.append(keywordsSection)
    div.append(similarEntitiesSection)
    div.append(mentionsSection)
    div.append(mentionedBySection)
    $("#content").html(div)
    $("a.result_element").on("click", detailHandler);
}

const detailHandler = (event) => {

    $("#content").html('<h3 id="results">Fetching results ...</h3>')
    const detailPayload = {entity: event.target.id}
    $.ajax('/detail/', {
        data: JSON.stringify(detailPayload),
        contentType: 'application/json',
        type: 'POST'})
        .done(showDetail)
}

$("#search").on("click", searchHandler);
$("#query").on("keypress", enterHandler);
