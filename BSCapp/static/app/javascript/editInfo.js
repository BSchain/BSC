
function EditInfo(){
    var btn = document.getElementById("edit");
    if (btn.innerHTML == "编辑")
    {
        btn.innerHTML = "保存";
        var name = document.getElementById("nametext");
        var value = name.innerHTML;
        name.innerHTML = "<input name='name' class='form-control' id='name' value="+value+">";
    }
    else {
        $.ajax({
          dataType: 'json',
          type: 'POST',
          data: {
            "email": $("#email").val(),
            "realname": $("#name").val(),
            "phone": $("#phone").val(),
            "idcard": $("#idcard").val(),
            "company": $("#company").val(),
            "title": $("#title").val(),
            "addr": $("#addr").val(),
          }
        }).done(function(data) {
          if (data.statCode != 0) {
              alert(data.errormessage)
          } else {
              btn.innerHTML = "编辑";
              var value = document.getElementById("name").value;
              var name = document.getElementById("nametext");
              name.innerHTML = value;
              indexURL = "/userInfo/"
              window.location.replace(indexURL);
          }
        })
    }
}
