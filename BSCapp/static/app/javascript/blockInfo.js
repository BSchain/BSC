var m1 = new MyModal.modal(function() {
				alert("你点击了确定");
			});

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
            m1.show()
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