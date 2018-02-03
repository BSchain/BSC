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
            alert("已经上传过相同文件");
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
