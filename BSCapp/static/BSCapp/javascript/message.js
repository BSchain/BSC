
function checkUpload() {
    var form_data = new FormData();
    var file_info = $("#file")[0].files[0];
    form_data.append('file', file_info);
    form_data.append('data_name', $('#data_name').val());
    form_data.append('data_info', $('#data_info').val());
    form_data.append('data_type', $('#data_type').val());
    form_data.append('data_source', $('#data_source').val());
    form_data.append('first_title', $('#first_title').val());
    form_data.append('second_title', $('#second_title').val());

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

scienceMapList = ['国家高新技术企业','高校院所','科研机构','入选QS世界大学500强', '北京地区上市公司','北京地区科技型上市企业','新三板挂牌企业','新三板创新层','独角兽企业','国家重点实现验室',
                    '国家工程技术研究中心','北京重点实验室','北京工程技术研究中心','北京企业研发机构','高等学校高精尖创新中心','国家级科技企业孵化器','国家级大学科技园','国家级众创空间','北京创业投资及股权投资机构','企业融资',
                    '企业并购','两院院士','北京科技新星','首都科技领军人才','全球高被引科学家','开放实验室','科研仪器设备','北京科技计划课题','北京自然基金项目','PCT国际专利申请量',
                    '全球500强企业总部','国际科技合作基地（国家）','国际科技合作基地（北京）','全市科普基地','社区科普体验厅','中小学科学探究实验室'];


leadingPredictionList = ['电子信息','生物医药','新能源','新能源汽车','节能环保','新材料','智能制造'];

keyAreaAnalysisList = ['无人机', '物联网','虚拟现实','增强现实','智能驾驶','智能机器人','区块链','5G','人工智能','智能农业','第三代半导体','大数据分析','量子通信','固态锂电池','石墨烯'];


innovationActivitiesList = ['上市企业','新三板挂牌企业','独角兽企业','初创企业','潜力企业','企业全景信息','企业创新能力评价','企业创新活动跟踪','高技术企业产业分析','众创空间生态发展情况'];

achievementTransformationList = ['科技计划项目', '技术交易', '专利运营', '高价值运营'];

regionalSynergyList = ['园区共建', '产来辐射', '创新合同', '津京冀宏观数据'];

technologyPolicyList = ['北京政策', '国外政策', '政策解读'];

urbanManagementList = ['三城一区', '遥感影像', '资源现状', '动态监测'];


function generateOption(obj, list){
    for(i=0; i < list.length; i++)
        {
            item_option = '<option value="'+list[i]+'">'+list[i]+'</option>';
            obj.append(item_option);
        }
    return obj;
}

lastFirstTitle = ''
function changeSecondTitle(obj) {
    first_title_val = $('#first_title').val();
    second_title_obj = $('#second_title');
    if(lastFirstTitle != first_title_val){
        second_title_obj.empty();
        lastFirstTitle = first_title_val
        if(first_title_val == '科技资源地图')
        {
            second_title_obj = generateOption(second_title_obj,scienceMapList );
        }
        else if(first_title_val == '前沿预判跟踪')
        {
            second_title_obj = generateOption(second_title_obj,leadingPredictionList );
        }
        else if(first_title_val == '重点领域综合分析')
        {
            second_title_obj = generateOption(second_title_obj,keyAreaAnalysisList );
        }
        else if(first_title_val == '企业创新活动')
        {
            second_title_obj = generateOption(second_title_obj,innovationActivitiesList );
        }
        else if(first_title_val == '科技成果转化')
        {
            second_title_obj = generateOption(second_title_obj,achievementTransformationList );
        }
        else if(first_title_val == '区域协同')
        {
            second_title_obj = generateOption(second_title_obj,regionalSynergyList );
        }
        else if(first_title_val == '科技政策')
        {
            second_title_obj = generateOption(second_title_obj,technologyPolicyList );
        }
        else if(first_title_val == '城市化精细管理')
        {
            second_title_obj = generateOption(second_title_obj,urbanManagementList );
        }
        else {
            item_option = '<option value="科技资源">科技资源</option>';
            second_title_obj.append(item_option)
        }
    }
}