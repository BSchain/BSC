var incomeUser = 1

function checkUpload() {
    var form_data = new FormData();
    var file_info = $("#file")[0].files[0];
    form_data.append('file', file_info);
    form_data.append('data_name', $('#data_name').val());
    form_data.append('data_info', $('#data_info').val());
    form_data.append('data_source', $('#data_source').val());
    form_data.append('data_price', $('#data_price').val());
    form_data.append('data_type', $('#data_type').val());
    form_data.append('data_tag', $('#data_tag').val());
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
            " <input name =\"data_income1\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_income1\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ration1\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_ration1\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
            " </div>"
        }
        else{
            div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
            " <input name =\"data_income1\" style=\"background: lightblue\" class=\"form-control\" id=\"data_income1\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ration1\" style=\"background: lightblue\" class=\"form-control\" id=\"data_ration1\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
            " </div>"
        }
        // div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
        //     "\t\t\t\t\t\t\t\t\t\t\t\t\t<input name =\"data_income1\" style=\"background: "+ style+ " class=\"form-control\" id=\"data_income"+incomeUser+"\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
        //     "                                                    <input name =\"data_ration1\" class=\"form-control\" id=\"data_ration1\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
        //     "\t\t\t\t\t\t\t\t\t\t\t\t</div>"

        var income_userId = "income_user"+(incomeUser-1)
        document.getElementById(income_userId).appendChild(div)
    }
    else{
        incomeUser +=1
        var div = document.createElement("div")
        div.innerHTML = "<div class=\"form-group\" id=\"income_user"+incomeUser +"\">\n" +
            " <input name =\"data_income1\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_income1\" value=\"\" placeholder=\"数据收益人"+incomeUser+"用户名\">\n" +
            " <input name =\"data_ration1\" style=\"background: cornsilk\" class=\"form-control\" id=\"data_ration1\" value=\"\" placeholder=\"收益比重"+incomeUser+" 范围(0~100)\">\n" +
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