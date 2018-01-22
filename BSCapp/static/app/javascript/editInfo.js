
function EditInfo(){
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
        indexURL = "/userInfo/"
        window.location.replace(indexURL);
      }
    })
}
