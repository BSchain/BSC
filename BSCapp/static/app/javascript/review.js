function reviewAcknowledge(obj) {
    $.ajax("/adminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": "1",
        }
      }).done(function(data){
          window.location.replace("/adminDataInfo/");
      })
    return;
}

function reviewReject(obj) {
    $.ajax("/adminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": "2",
        }
      }).done(function(data){
          window.location.replace("/adminDataInfo/");
      })
    return;
}