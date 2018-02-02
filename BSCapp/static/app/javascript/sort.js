function buySortBase(obj){
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

function orderSortBase(obj){
    $.ajax("/Order/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "sort_name": obj
        }
      }).done(function(data){
          window.location.replace("/Order/");
      })
    return;
}

