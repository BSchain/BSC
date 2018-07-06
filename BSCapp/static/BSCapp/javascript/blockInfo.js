function interpreterBlock(obj) {
    block_height = obj.value;
    $.ajax("/ChainInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "height": block_height,
        }
    }).done(function (data) {
        if (data.statCode != 0) {
            alert(data.message)
            return false
        }
        else {

            // alert('index: '+ data.block.index+
            // 'timestamp: ' + data.block.timestamp+
            // ' prev_hash: ' + data.block.prev_hash +
            // ' transactions: ' + data.block.transactions)
            // alert(data.message)
            // alert(data.block)
            // alert(data.txNumber)
            // alert(data.timestamp)
            block_json = JSON.parse(data.block)
            var div = document.createElement("div")
            div.id = 'new_add_info'
            for (var i=0;i<data.txNumber;i++)
            {
                str1 = ''
                if(i=0){
                    str1 = "<span> 交易数量: "+ data.txNumber +" <span> </span>"
                }
                str2 = ''
                str2 += "<span> 交易时间: " + block_json.transactions[i].timestamp+ "</span>" +
                "<span> 交易动作: "+ block_json.transactions[i].action+"</span>" +
                "<span> 数据出售方: " + block_json.transactions[i].seller+ "</span>" +
                "<span> 数据购买方: " + block_json.transactions[i].buyer+ "</span>" +
                "<span> 数据id: " + block_json.transactions[i].data_uuid+ "</span>" +
                "<span> 数据标价: " + block_json.transactions[i].credit+ "</span>"+"<br>";
            }
            div.innerHTML += str1 + str2
            document.getElementById("one_block_detail").appendChild(div)
        }
    })
    return;
}
function showBlockDetail(obj) {
    block_height = obj.value;
    $.ajax("/ChainInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "height": block_height,
        }
    }).done(function (data) {
        if (data.statCode != 0) {
            alert(data.message)
            return false
        }
        else {
            // alert('index: '+ data.block.index+
            // 'timestamp: ' + data.block.timestamp+
            // ' prev_hash: ' + data.block.prev_hash +
            // ' transactions: ' + data.block.transactions)
            // alert(data.message)
            alert(data.block)
        }
    })
    return;
}

function adminShowBlockDetail(obj) {
    block_height = obj.value;
    $.ajax("/AdminChainInfo/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "height": block_height,
        }
    }).done(function (data) {
        if (data.statCode != 0) {
            alert(data.message)
            return false
        }
        else {
            alert(data.block)
        }
    })
    return;
}

function indexShowBlockDetail(obj) {
    block_height = obj.value;
    $.ajax("/Index/", {
        dataType: 'json',
        type: 'POST',
        data: {
            "height": block_height,
        }
    }).done(function (data) {
        if (data.statCode != 0) {
            alert(data.message)
            return false
        }
        else {
            alert(data.block)
        }
    })
    return;
}