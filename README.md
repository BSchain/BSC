# BSC
chain for science data sharing

## 数据库迁移指令
>`python3 manage.py makemigrations  BSCapp`
>
>`python3 manage.py migrate`

## 项目运行指令
>`python3 manage.py runserver`
>
>在浏览器网站中输入 `127.0.0.1:8000/index` 默认端口为8000
>
>点击右上角的login，里面可以选择注册还是登陆

## 创建超级用户指令
>`python3 manage.py createsuperuser`
>
>在浏览器网站中输入 `http://127.0.0.1:8000/admin/` 即可管理数据库

## TODO:
* <font color=#0099ff size=5 face="黑体"> 1.实名注册(Done) </font>
>用户注册需要的信息：登录名、密码、邮箱信息.
>用户表，保存登录名，密码，邮箱到表中。

* <font color=#0099ff size=5 face="黑体"> 2.用户登录 && 管理员登录 (TODO: add admin) </font>
>用户或者管理员登录：需要进行数据库查询操作，登陆后跳转至页面：按数据上传时间最新排序.
* <font color=#0099ff size=5 face="黑体"> 3.用户个人信息完善(Doing) </font>
>个人信息完善包括：真实姓名、手机号、身份证号、所在公司、个人头衔、居住地.
>
>个人信息表，保存真实姓名、手机号、身份证号、所在公司、个人头衔、居住地。
* <font color=#0099ff size=5 face="黑体"> 4.用户查看订单信息 </font>
>日期、行为、金额、区块信息；
>
>页面显示：账户余额，交易表和数据信息表(订单号，购买时间，出售方，购买数据名，数据详细信息，购买价格，订单详情【可以显示数据详细信息，参考京东等服务页面】)
>
>需要搜索交易表，交易id、购买方id、购买时间、出售方id、购买的数据id.
* <font color=#0099ff size=5 face="黑体"> 5.账户充值 </font>
>选择充值方式，充值，完成支付，更新账户余额(数据库需要进行更新操作)
>
>用户充值记录表，保存当前充值时间，充值大小，充值前账户余额，充值后账户余额。
>
>用户账户余额表，更新当前的用户余额;
>
>充值完成后生成一个transaction，并发布至网络中，服务器得到并进行存储，待后续挖矿使用；
>
>out_coin表，保存当前的coin_uuid,并且保存该coin的owner为seller,同时标记当前的coin是否花费为unspent.
<pre>transaction{
    in_coins = NULL
    out_coins = [{
        coin_uuid: generate_uuid_coin,
        number_coin: 100 ( equals to credit )
        owner: seller ('zpf_uuid')
    }]
    timestamp = 1515855931.2668328
    action = 'recharge'
    seller = 'zpf_uuid'
    buyer = NULL
    reviewer = NULL
    data_uuid = 'mydata_uuid'
    credit = 100.0
}</pre>
* <font color=#0099ff size=5 face="黑体"> 6.用户上传数据 </font>
>上传数据、填写数据信息(填写数据名、数据简介信息、数据tag选择、数据售价(信用/次下载)、数据上传时间，数据保存格式、数据保存服务器地址)
>
>数据库保存当前数据上传时间，保存当前数据的uuid,保存当前数据上传者的id,保存数据名，保存数据简介信息，保存数据tag,保存数据售价；
* <font color=#0099ff size=5 face="黑体"> 7.用户搜索数据 </font>
>(0)模糊匹配(匹配数据名，数据上传者名，数据简介信息，数据tag，数据上传时间，数据来源，保存格式)
>
>(1)按照数据上传时间搜索
>
>(2)选择数据保存格式进行搜索 (word,csv,excel,txt,jpg or 文本、压缩包、图片、视频)
>
>(3)选择数据来源(医疗、交通、农业、教育等)
* <font color=#0099ff size=5 face="黑体"> 8.用户购买数据 </font>
>购买表，生成购买信息，交易id,购买方id、购买时间、出售方id、购买的数据id,购买时间,购买价格,
<pre>transaction{
    in_coins = [{
        coin_uuid: generate_uuid_coin,
        number_coin: 100 ( equals to credit )
        owner: seller ('zpf_uuid')
    }]
    out_coins = [{
        coin_uuid: generate_uuid_coin,
        number_coin: 100 ( equals to credit )
        owner: seller ('zpf_uuid')
    }]
    timestamp = 1515855931.2668328
    action = 'buy'
    seller = 'zpf_uuid'
    buyer = ''
    reviewer = NULL
    data_uuid = 'mydata_uuid'
    credit = 100.0
}</pre>

用户表

| 用户id | 登录名          | 密码    | 邮箱 |真实姓名| 手机号 |身份证号 |所在公司 |个人头衔| 居住地|
| ----- |:-------------:| :------:|:-------:| :----:| :----:| :----:| :----:| :----:| :----:|

个人信息表

| 用户id |真实姓名| 手机号 |身份证号 |所在公司 |个人头衔| 居住地|
| ----- |:----:| :----:| :----:| :----:| :----:| :----:|

交易表

| 交易id | 购买方id   | 出售方id    | 数据id |购买时间| 购买价格 |
| ----- |:----------:| :------:|:-------:| :----:| :----:|

数据表

| 数据id | 数据拥有者id| 数据名| 数据简介信息 | 数据上传时间 | 数据来源 |数据保存格式 |数据tag |数据保存服务器地址|
| ----- |:-------------:| :------:|:-------:| :----:| :----:| :----:| :----:| :----:|

coin表

| coin_id | coin拥有者id | coin大小 | coin是否花费 | coin创建时间|
| ----- |:-------------:| :------:|:-------:|:-------:|


用户充值表

| 用户id | 充值时间| 充值大小 | 充值前账户余额|充值后账户余额|充值coin_id|
| ----- |:-------------:| :------:|:-------:| :----:|:---:|

用户钱包表

| 用户id | 钱包余额|
| ----- |:------:|

用户下载数据表

| 用户id | 已下载数据id|
| ----- |:------:|


## (1) block文件
>基本函数: new_block（产生新的块）、to_dict（返回块对应的dict）、save_block(保存至文件),

>考虑字段有: index(块高度)、timestamp(时间戳)、prev_hash(前一块的hash)、nonce(关键字进行pow验证)、current_transactions（当前所有的交易）
## (2) chain文件
>由于随着交易进行，chain会逐渐增长，目前没有打算直接保存在内存中。至于对chain合法性的验证，可以通过依次读取block文件，进行hash值校验以及pow证明；

>基本函数有: find_block_by_index、 add_block
>考虑字段有: chain_length（长度）、chain（所有的block构成）
## (3) coin文件

作为transaction的一个属性，用于记录信用度是否花费，（这里没有想太明白）
## (4) transaction文件

>通过action关键字区分不同的操作。需要考虑的因素较多，login、upload、buy、download等，

>目前字段有: data_uuid、action、 buyer 、 seller （这个名字可以改改）、coin_in、coin_out

>主要函数:new_transaction等

## (5) config文件

保存block存储的文件目录、保存当前挖矿的难度系数、保存transaction以及block的字段类型等

## (6) utils 文件
常用的函数实现。
>hash(block) 根据传递的block生成hash值、chain_valid 验证chain的合法性、proof_of_work（pow函数实现）

## (7) node文件

用于其他网络节点的注册，函数目前未定义

## (8) cli文件

设置全局参数，尚未定义具体参数

## (9) mine文件

挖矿服务的主要函数。（主要通过传递的current_transactions 生成新的block）
