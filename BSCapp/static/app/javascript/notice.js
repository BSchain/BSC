function read_notice(obj) {
    $.ajax("/Notify/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": 'read',
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
          "op": 'unread',
        }
      }).done(function(data){
          window.location.replace("/Notify/");
      })
    return;
}

function delete_notice(obj) {
    $.ajax("/Notify/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": 'delete',
        }
      }).done(function(data){
          window.location.replace("/Notify/");
      })
    return;
}
