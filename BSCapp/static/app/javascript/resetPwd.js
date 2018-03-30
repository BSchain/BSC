function indexResetPwd() {
  pwd = $("#password").val()
  $.ajax({
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "password": pwd,
      "repassword": $("#repassword").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.message)
        return False
    } else {
      alert(data.message)
      indexURL = "/Login/"
      window.location.replace(indexURL);
    }
  })
}
