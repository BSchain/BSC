function buyData(obj) {
    data_id = obj.value
    $.ajax("/BuyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "data_id": data_id,
            "op":'buy'
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              alert(data.message)
              window.location.replace("/order/");
          }
      })
    return;
}

function downloadData(obj) {
    data_id = obj.value
    $.ajax("/BuyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "data_id": data_id,
            "op":'download'
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              alert(data.message)
              window.location.replace("/Order/");
          }
      })
    return;
}