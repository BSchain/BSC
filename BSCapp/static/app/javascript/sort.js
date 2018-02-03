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

function adminDataSortBase(obj){
    $.ajax("/AdminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "sort_name": obj
        }
      }).done(function(data){
          window.location.replace("/AdminDataInfo/");
      })
    return;
}


function notifyDataSortBase(obj){
    $.ajax("/Notify/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "sort_name": obj
        }
      }).done(function(data){
          window.location.replace("/Notify/");
      })
    return;
}

function myDataSortBase(obj){
    $.ajax("/MyData/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "sort_name": obj
        }
      }).done(function(data){
          window.location.replace("/MyData/");
      })
    return;
}