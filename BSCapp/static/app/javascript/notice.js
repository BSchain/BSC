function read_notice(obj) {
    $.ajax("/Notify/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": '1',
        }
      }).done(function(data){
          window.location.replace("/Notify/");
      })
    return;
}

function unread_notice(obj) {
    $.ajax("/Notify/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": '2',
        }
      }).done(function(data){
          window.location.replace("/Notify/");
      })
    return;
}