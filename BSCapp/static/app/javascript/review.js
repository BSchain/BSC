function reviewAcknowledge(obj) {
    $.ajax("/AdminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": "1",
        }
      }).done(function(data){
          window.location.replace("/AdminDataInfo/");
      })
    return;
}

function reviewReject(obj) {
    $.ajax("/AdminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": "2",
        }
      }).done(function(data){
          window.location.replace("/AdminDataInfo/");
      })
    return;
}
