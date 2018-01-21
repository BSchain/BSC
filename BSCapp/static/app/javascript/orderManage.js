function operate(obj) {
  $.ajax("/distributorOrderManage/", {
    dataType: 'json',
    type: 'POST',
    data: {
      "info": obj.name,
    }
  }).done(function(data){
      window.location.replace("/distributorOrderManage/");
  })
}
