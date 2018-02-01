
function EditInfo(){
    var btn = document.getElementById("edit");
    if (btn.innerHTML == "编辑")
    {
        $("#edit").replaceWith("<div class='row'> <div class='col-md-6'> <button id='edit' class='btn btn-primary btn-lg btn-block' onclick='EditInfo()'>保存</button> </div> <div class='col-md-6'> <button id='cancel' class='btn btn-primary btn-lg btn-block' onclick='cancelEdit()'>取消</button> </div> </div>");
        var name = document.getElementById("nametext");
        var value = name.innerHTML;
        name.innerHTML = "<input name='name' id='name' value="+value+">";
        var phone = document.getElementById("phonetext");
        var value = phone.innerHTML;
        phone.innerHTML = "<input name='phone' id='phone' value="+value+">";
        var idcard = document.getElementById("idcardtext");
        var value = idcard.innerHTML;
        idcard.innerHTML = "<input name='idcard' id='idcard' value="+value+">";
        var company = document.getElementById("companytext");
        var value = company.innerHTML;
        company.innerHTML = "<input name='company' id='company' value="+value+">";
        var title = document.getElementById("titletext");
        var value = title.innerHTML;
        title.innerHTML = "<input name='title' id='title' value="+value+">";
        var addr = document.getElementById("addrtext");
        var value = addr.innerHTML;
        addr.innerHTML = "<input name='addr' id='addr' value="+value+">";
    }
    else {
        $.ajax({
          dataType: 'json',
          type: 'POST',
          data: {
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

function cancelEdit()
{
    indexURL = "/userInfo/"
    window.location.replace(indexURL);
}
