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
