function reviewAcknowledge(obj) {
    $.ajax("/AdminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
          "id": obj.id,
          "op": "pass",
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
          "op": "reject",
        }
      }).done(function(data){
          window.location.replace("/AdminDataInfo/");
      })
    return;
}


function reviewDataAllPass() {
    $.ajax("/AdminDataInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "func":'reviewAllPass'
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              alert(data.message)
              window.location.replace("/AdminDataInfo/");
          }
      })
    return;
}