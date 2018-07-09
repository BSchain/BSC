
function popWindow(block) {
    tx_id = block['tx_id']
    posId = "block"+tx_id
    item = document.getElementById(posId)
    str_html = '<div id="myModal'+tx_id+'" class="modal" style="display: block; " >' +
        '          <div class="modal-content" style="width: available"> ' +
        '            <div class="modal-header" > ' +
        '               <span id="close'+ tx_id +'" class="close" onclick="hideWindow('+tx_id+')">&times;</span>' +
        '                <h4>操作'+tx_id+'详细信息</h4>' +
        '                <div class="modal-body pre-scrollable">' +
        '                   <div class="panel-body">' +
        '                   <p align="left"> 查看会议 </p> ' +
        '                       <table class="table table-striped table-bordered table-condensed table-hover">' +
        '                           <thead >' +
        '                               <tr>' +
        '                                   <th align="center"> 论文名称 </th>' +
        '                                   <th align="center"> 论文作者 </th>' +
        '                                   <th align="center"> 会议名称 </th>' +
        '                                   <th align="center"> 关 键 字 </th>' +
        '                                   <th align="center"> 论文摘要 </th>' +
        '                               </tr>' +
        '                           </thead>' +
        '                           <tbody>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                                   <td align="left">该系统bababbababa......</td>' +
        '                               </tr>' +
        '                           </tbody>' +
        '                       </table>' +
        '                   <p align="left"> 查看期刊 </p> ' +
        '                       <table class="table table-striped table-bordered">' +
        '                           <thead>' +
        '                               <tr>' +
        '                                   <th align="center"> 文章名称 </th>' +
        '                                   <th align="center"> 文章作者 </th>' +
        '                                   <th align="center"> 期刊名称 </th>' +
        '                                   <th align="center"> 关 键 字 </th>' +
        '                                   <th align="center"> 文章摘要 </th>' +
        '                               </tr>' +
        '                           </thead>' +
        '                           <tbody>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                                   <td align="left">该系统bababbababa......</td>' +
        '                               </tr>' +
        '                           </tbody>' +
        '                       </table>' +
        '                   <p align="left"> 查看专利 </p> ' +
        '                       <table class="table table-striped table-bordered">' +
        '                           <thead>' +
        '                               <tr>' +
        '                                   <th align="center"> 专利名称 </th>' +
        '                                   <th align="center"> 专利号 </th>' +
        '                                   <th align="center"> 专利申请人 </th>' +
        '                                   <th align="center"> 专利关键字 </th>' +
        '                                   <th align="center"> 专利作者 </th>' +
        '                               </tr>' +
        '                           </thead>' +
        '                           <tbody>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                                   <td align="left">该系统bababbababa......</td>' +
        '                               </tr>' +
        '                           </tbody>' +
        '                       </table>' +
        '                   <p align="left"> 其他操作 </p> ' +
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
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                               <tr>' +
        '                                   <td align="left">基于区块链的科技资源确权系统的设计与实现</td>' +
        '                                   <td align="left">郑鹏飞</td>' +
        '                                   <td align="left">北航软件学院本科答辩</td>' +
        '                                   <td align="left">区块链 数据确权 共识机制</td>' +
        '                               </tr>' +
        '                           </tbody>' +
        '                       </table>' +
        '                   </div>' +
        '                </div>' +
        '           </div>' +
        '         </div>' +
        '       </div>'
    item.innerHTML = str_html

}

function hideWindow(tx_id) {
    modal = document.getElementById('myModal'+ tx_id)
    modal.style.display = "none";

}
