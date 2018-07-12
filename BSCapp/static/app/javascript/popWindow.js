
function popWindow(block) {
    tx_id = block['tx_id']
    posId = "block"+tx_id
    item = document.getElementById(posId)

    conference_html = ''
    if(block['conference_data_id_list'] != ''){
        conference_data_id_list = block['conference_data_id_list'].split(',')

        len_conference = conference_data_id_list.length
        conference_body_html = ''
        for( i=0; i < len_conference; i++){
            item_conference_id = conference_data_id_list[i]
            conference_body_html += '<tr>' +
                                    // '    <td align="left">'+block[item_conference_id]['article_id']+'</td>' +
                                    '    <td align="left">'+block[item_conference_id]['article_name']+'</td>' +
                                    '    <td align="left">'+block[item_conference_id]['article_authors']+'</td>' +
                                    '    <td align="left">'+block[item_conference_id]['conference_name']+'</td>' +
                                    '    <td align="left">'+block[item_conference_id]['keywords']+'</td>' +
                                    '    <td align="left">'+block[item_conference_id]['abstract']+'</td>' +
                                    '</tr>'
        }
        conference_html += '<h5 align="left"> 操作类型: 查看会议资源 </h5> ' +
        '                       <table class="table table-striped table-bordered table-condensed table-hover">' +
        '                           <thead >' +
        '                               <tr>' +
        // '                                   <th align="center"> 文章ID </th>' +
        '                                   <th align="center"> 论文名称 </th>' +
        '                                   <th align="center"> 论文作者 </th>' +
        '                                   <th align="center"> 会议名称 </th>' +
        '                                   <th align="center"> 关 键 字 </th>' +
        '                                   <th align="center"> 论文摘要 </th>' +
        '                               </tr>' +
        '                           </thead>' +
        '                           <tbody>' +
                                        conference_body_html +
        '                           </tbody>' +
        '                       </table>'
    }

    journal_html = ''
    if(block['journal_data_id_list'] != ''){
        journal_data_id_list = block['journal_data_id_list'].split(',')
        len_journal = journal_data_id_list.length
        journal_body_html = ''
        for( i=0; i < len_journal; i++){
            item_journal_id = journal_data_id_list[i]
            journal_body_html += '<tr>' +
                                 // '    <td align="left">'+block[item_journal_id]['article_id']+'</td>' +
                                 '    <td align="left">'+block[item_journal_id]['article_name']+'</td>' +
                                 '    <td align="left">'+block[item_journal_id]['article_authors']+'</td>' +
                                 '    <td align="left">'+block[item_journal_id]['journal_name']+'</td>' +
                                 '    <td align="left">'+block[item_journal_id]['keywords']+'</td>' +
                                 '    <td align="left">'+block[item_journal_id]['abstract']+'</td>' +
                                 '</tr>'
        }

        journal_html += '<h5 align="left"> 操作类型: 查看期刊资源 </h5> ' +
        '                     <table class="table table-striped table-bordered">' +
        '                         <thead>' +
        '                             <tr>' +
        // '                                 <th align="center"> 文章ID </th>' +
        '                                 <th align="center"> 文章名称 </th>' +
        '                                 <th align="center"> 文章作者 </th>' +
        '                                 <th align="center"> 期刊名称 </th>' +
        '                                 <th align="center"> 关 键 字 </th>' +
        '                                 <th align="center"> 文章摘要 </th>' +
        '                             </tr>' +
        '                         </thead>' +
        '                         <tbody>' +
                                    journal_body_html +
        '                         </tbody>' +
        '                     </table>'
    }

    patent_html = ''
    if(block['patent_data_id_list'] != ''){
        patent_data_id_list = block['patent_data_id_list'].split(',')
        len_patent = patent_data_id_list.length
        patent_body_html = ''
        for( i=0; i < len_patent; i++){
            item_patent_id = patent_data_id_list[i]
            patent_body_html += '<tr>' +
                                // '    <td align="left">'+block[item_patent_id]['patent_id']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_name']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_openId']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_applicant']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_authors']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_keywords']+'</td>' +
                                '    <td align="left">'+block[item_patent_id]['patent_province']+'</td>' +
                                '</tr>'
        }
        patent_html += '<h5 align="left"> 操作类型: 查看专利资源 </h5> ' +
    '                       <table class="table table-striped table-bordered">' +
    '                           <thead>' +
    '                               <tr>' +
    // '                                   <th align="center"> 专利ID </th>' +
    '                                   <th align="center"> 专利名称 </th>' +
    '                                   <th align="center"> 专利号 </th>' +
    '                                   <th align="center"> 专利申请人 </th>' +
    '                                   <th align="center"> 专利作者 </th>' +
    '                                   <th align="center"> 专利关键字 </th>' +
    '                                   <th align="center"> 所属省份 </th>' +
    '                               </tr>' +
    '                           </thead>' +
    '                           <tbody>' +
                                    patent_body_html +
    '                           </tbody>' +
    '                       </table>'
    }

    science_data_html = ''
    if(block['science_data_id_list'] != ''){
        operation_str = ''
        if(block['action'] == 'upload'){
            operation_str ='上传数据'
        }
        else if(block['action'] == 'review_pass'){
            operation_str ='审核数据通过'
        }
        else if(block['action'] == 'review_reject'){
            operation_str ='审核数据不通过'
        }
        else if(block['action'] == 'download'){
            operation_str ='下载数据'
        }
        science_data_html += '<h5 align="left">操作类型:'+operation_str+' </h5> ' +
        '                       <table class="table table-striped table-bordered">' +
        '                           <thead>' +
        '                               <tr>' +
        '                                   <th align="center"> 数据名称 </th>' +
        '                                   <th align="center"> 数据简介 </th>' +
        '                                   <th align="center"> 数据来源 </th>' +
        '                                   <th align="center"> 数据大小 </th>' +
        '                               </tr>' +
        '                           </thead>' +
        '                           <tbody>' +
        '                               <tr>' +
        '                                   <td align="left">'+block['science_data_name']+'</td>' +
        '                                   <td align="left">'+block['science_data_info']+'</td>' +
        '                                   <td align="left">'+block['science_data_source']+'</td>' +
        '                                   <td align="left">'+block['science_data_size']+'</td>' +
        '                               </tr>' +
        '                           </tbody>' +
        '                       </table>'
    }
    str_html = '<div id="myModal'+tx_id+'" class="modal" style="display: block; " >' +
        '          <div class="modal-content" style="width: available"> ' +
        '            <div class="modal-header"  >' +
        '               <button type="button" onclick="hideWindow(\'' + tx_id+  '\')" data-dismiss="modal" id="close'+ tx_id +'" class="close">&times; </button>' +
        '                <h4>操作详情</h4>' +
        '                <div class="modal-body pre-scrollable">' +
        '                   <div class="panel-body">' +
        '                    <h5 align="left"> 用户名: '+block['user_id']+' </h5> ' +
        '                    <h5 align="left"> 操作时间: '+block['timestamp']+' </h5> '
    if(block['conference_data_id_list'] != ''){
        str_html+=conference_html
    }
    if(block['journal_data_id_list'] != ''){
        str_html+=journal_html
    }
    if(block['patent_data_id_list'] != ''){
        str_html+=patent_html
    }
    if(block['science_data_id_list'] != ''){
        str_html+=science_data_html
    }
    str_html += '                   </div>' +
                '                </div>' +
                '           </div>' +
                '         </div>' +
                '       </div>';

    item.innerHTML = str_html

}

function hideWindow(tx_id) {
    posId = "myModal"+tx_id
    item = document.getElementById(posId)
    item.style.display = "none"

}
