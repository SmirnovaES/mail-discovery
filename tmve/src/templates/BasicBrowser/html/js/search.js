function handleKeyPress(event){
    var key = event.keyCode || event.which;
    if (key == 13) {
        doSearch();
    }
}

function doSearch() {
    var query = document.getElementsByName("search")[0].value;
    if (query == "") {
        return;
    }
    alert("searching for " + document.getElementsByName("search")[0].value + "...");
}
