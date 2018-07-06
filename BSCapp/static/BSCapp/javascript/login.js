function Func_validate() {
  pwd = $("#password").val()
  $.ajax({
    url: '/Login/',
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "password": pwd,
    }
  }).done(function(data) {
    if(data.statCode != 0) {
      alert(data.errormessage)
      return(false)
    } else {
     $.cookie('username', data.username, {path: '/'})
     $.cookie('password', md5(pwd), {path: '/'})
     if (data.isAdmin == 0) {
       indexURL = "/UserInfo/"
     } else {
       indexURL = "/AdminDataInfo/"
     }
     window.location.replace(indexURL);
     return(true)
    }
  })
}
