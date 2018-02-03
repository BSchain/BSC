function searchData(obj) {
    var searchBase = $("#searchBase").val();
    var searchField = $("#searchField").val();
    $.ajax({
        dataType: 'json',
        type: 'POST',
        data: {
        "searchBase": searchBase,
        "searchField": searchField,
        }
    }).done(function(data){
        alert("GET IT!")
        $('#mainTable').html(data);
    })
    return;
}