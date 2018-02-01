function buyData(obj) {
    data_id = obj.value
    $.ajax("/buyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "data_id": data_id,
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.error)
              return false
          }
          window.location.replace("/order/");
      })
    return;
}