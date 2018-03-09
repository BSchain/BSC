function orderDownloadData(obj) {
    dataid = obj.value;
    $.ajax("/Order/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "data_id": dataid,
            "op":'download'
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              // alert(data.message)
              var file = document.getElementById(obj.value);
              file.innerHTML = "<a hidden='hidden' id='download' href='" + obj.name + "' download='" + obj.id + "'>下载</a>";
              var download = document.getElementById("download")
              download.click()
          }
      })
    return;
}