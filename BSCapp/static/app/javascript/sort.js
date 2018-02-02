function sortTime(obj){
    $.ajax("/BuyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "type":'time'
        }
      }).done(function(data){
          window.location.replace("/BuyableData/");
      })
    return;
}
