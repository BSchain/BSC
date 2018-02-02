function sortBase(obj){
    $.ajax("/BuyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "sort_name": obj
        }
      }).done(function(data){
          window.location.replace("/BuyableData/");
      })
    return;
}


