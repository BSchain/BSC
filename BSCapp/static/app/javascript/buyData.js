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
              // download transaction in the view.py file
              // alert(data.message)
              var file = document.getElementById(obj.value);
              // obj_address = data.address
              // obj_ = data.name
              // file.innerHTML = "<a hidden='hidden' id='download' href='" + obj.name + "' download='" + obj.id + "'>下载</a>";
              // alert(data.data_address)
              // alert(data.data_name)
              file.innerHTML = "<a hidden='hidden' id='download' href='" + data.data_address + " ' download='" + data.data_name + "'>下载</a>";
              var download = document.getElementById("download")
              download.click()
              // alert('下载成功')
              location.replace(location)
          }
      })
    return;
}
