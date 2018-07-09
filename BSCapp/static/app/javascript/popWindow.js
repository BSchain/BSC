function getModal(height){
    return document.getElementById('myModal'+ height)
}

function popWindow(block) {
    height = block['height']
    posId = "block"+height
    item = document.getElementById(posId)
    str_html = '<div id="myModal'+height+'" class="modal" style="display: block; width: content-box; " >' +
        '          <div class="modal-content" style="width: available"> ' +
        '            <div class="modal-header" > ' +
        '               <span id="close'+ height +'" class="close" onclick="hideWindow('+height+')">&times;</span>' +
        '                <h4>操作'+height+'详细信息</h4>' +
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

function hideWindow(height) {
    modal = getModal(height)
    modal.style.display = "none";

}
