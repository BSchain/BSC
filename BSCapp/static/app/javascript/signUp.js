function SignUp_validate() {
  pwd = $("#password").val()
  $.ajax({
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "email": $("#email").val(),
      "password": pwd,
      "repassword": $("#repassword").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.errormessage)
    } else {
      $.cookie('username', data.username, {path: '/'})
      $.cookie('password', md5(pwd), {path: '/'})
      indexURL = "/Login/"
      window.location.replace(indexURL);
    }
  })
}
