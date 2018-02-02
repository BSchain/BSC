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
              window.location.replace("/Order/");
          }
      })
    return;
}

function downloadData(obj) {
    data_id = obj.value;
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
              var file = document.getElementById(obj.value);
              file.innerHTML = "<a hidden='hidden' id='download' href='" + obj.name + "' download='" + obj.id + "'>下载</a>";
              var download = document.getElementById("download")
              download.click()
          }
      })
    return;
}
