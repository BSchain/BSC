var incomeUser = 1

function checkUpload() {
    var form_data = new FormData();
    var file_info = $("#file")[0].files[0];
    form_data.append('file', file_info);
    form_data.append('data_name', $('#data_name').val());
    form_data.append('data_info', $('#data_info').val());
    form_data.append('data_source', $('#data_source').val());
    form_data.append('data_price', $('#data_price').val());
    form_data.append('data_ration0', $('#data_ration0').val());
    form_data.append('data_type', $('#data_type').val());
    form_data.append('data_tag', $('#data_tag').val());
    var temp = incomeUser
    while(temp > 0){
        form_data.append('data_income_user'+temp, document.getElementById("data_income_user"+temp).value);
        form_data.append('data_ratio'+temp, document.getElementById("data_ratio"+temp).value);
        temp -=1
    }
    form_data.append('data_user_number',incomeUser)

    $.ajax({
        url: '/Upload/',
        dataType: 'json',
        type: 'POST',
        data: form_data,
        processData: false,  // tell jquery not to process the data
        contentType: false, // tell jquery not to set contentType
    }).done(function(data) {
        if (data.statCode != 0)
        {
            alert(data.message);
        } else {
            alert("上传成功");
            indexURL = "/MyData/";
            window.location.replace(indexURL);
        }
    })
}

function checkRecharge() {
    alert("充值成功");
}

function addNewIncomeUser(){
    if(incomeUser >= 5){
        alert('最多5个其他收益者')
    }
    else if(incomeUser > 0){
        incomeUser +=1
        var div = document.createElement("div")
        if (incomeUser%2 !=0){
            div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
            " <input name =\"data_income_user"+incomeUser+"\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_income_user"+incomeUser+"\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ratio"+incomeUser+"\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_ratio"+incomeUser+"\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
            " </div>"
        }
        else{
            div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
            " <input name =\"data_income_user"+incomeUser+"\" style=\"background: lightblue\" class=\"form-control\" id=\"data_income_user"+incomeUser+"\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ratio"+incomeUser+"\" style=\"background: lightblue\" class=\"form-control\" id=\"data_ratio"+incomeUser+"\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
            " </div>"
        }
        var income_userId = "income_user"+(incomeUser-1)
        document.getElementById(income_userId).appendChild(div)
    }
    else{
        incomeUser +=1
        var div = document.createElement("div")
        div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
            " <input name =\"data_income_user"+incomeUser+"\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_income_user"+incomeUser+"\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ratio"+incomeUser+"\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_ratio"+incomeUser+"\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
            " </div>"
        document.getElementById("income_div").appendChild(div)
    }
}

function deleteNewIncomeUser(){
    if(incomeUser > 0){
        document.getElementById("income_user"+incomeUser).remove()
        incomeUser -=1
    }
    else{
        alert('无法删除，没有其他收益者！')
    }
}

function rechagreAccount(obj) {
    account = document.getElementById("account").value
    reaccount = document.getElementById("reaccount").value
    amount = document.getElementById("amount").value
    $.ajax("/Recharge/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "account":account,
            "reaccount":reaccount,
            "amount": amount
        }
      }).done(function(data){
          if (data.statCode !=0){
              alert(data.message)
              return false
          }
          else{
              alert(data.message)
              window.location.replace("/UserInfo/");
          }
      })
    return;
}
