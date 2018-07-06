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


function indexFindPwd() {
  $.ajax({
    dataType: 'json',
    type: 'POST',
    data: {
      "username": $("#username").val(),
      "email": $("#email").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.message)
        // 是否刷新输入
      // indexURL = "/findPwd/"
      // window.location.replace(indexURL);
        return False
    } else {
      alert(data.message)
      indexURL = "/Index/"
      window.location.replace(indexURL);
    }
  })
}

function userModifyPwd() {
  $.ajax({
    dataType: 'json',
    type: 'POST',
    data: {
      "old_password": $("#old_password").val(),
      "new_password": $("#new_password").val(),
      "new_repassword": $("#new_repassword").val(),
    }
  }).done(function(data) {
    if (data.statCode != 0) {
      alert(data.message)
        // 是否刷新输入
      // indexURL = "/findPwd/"
      // window.location.replace(indexURL);
        return False
    } else {
      alert(data.message)
      indexURL = "/Login/"
      window.location.replace(indexURL);
    }
  })
}