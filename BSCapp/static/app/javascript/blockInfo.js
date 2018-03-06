function showBlockDetail(obj) {
    block_height = obj.value;
    $.ajax("/ChainInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "height": block_height,
            "op":'show'
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              alert(data.message)
              // download transaction in the view.py file
              var file = document.getElementById(obj.value);
              file.innerHTML = "<a hidden='hidden' id='download' href='" + obj.name + "' download='" + obj.id + "'>下载</a>";
          }
      })
    return;
}