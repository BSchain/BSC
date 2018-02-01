function buyData(obj) {
    $.ajax("/buyableData/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
            "price":obj.price,
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