# BSC
chain for science data sharing

## 下一步开发
> *block生成 Proof of work算法，开发已完成.*

### 当前已完成

>* 0.`链数据信息展示`
>> 块的高度，块中交易个数，块的具体信息

>* 1.`收益的比例分配`
>> 用户上传页面设置，多个用户，收益占比，由用户输入确定。

>* 2.`添加评分机制 五星级（评分人数）`
>> 避免上传数据与描述不符。
>>
>> 需要在purchase表中添加新的字段。记录每条用户的评价等级。1~5星;
>>
>> 需要在数据data表中添加新的字段，记录当前该数据评价平均等级;
>>
>> 需要在data表中添加新的字段，记录评价该数据的用户个数。

>* 3.`下载时间隔5分钟`
>> 避免多次下载导致transaction文件过多。
>>
>> 需要新增加download表，用于记录用户下载的信息。每次更新用户最近一次的下载时间。
>>
>> 下载数据前，判断当前时间和最近一次下载的时间是否在10分钟之内，十分钟之内则不可以下载。

>* 5.`挖矿的block大小限制`
>> 暂时没有设定，后期添加block最大限度。
>>
>> 修改后挖矿时，transaction文件删除的逻辑需要同时进行修改。

>* 6.`挖矿的block产生时间间隔`
>> 修改为5分钟

>* 4.`链数据同步至mysql`

>> 用于数据库信息修正。
>>
>> 同步信息目前只涉及到coin是否花费。
<pre><code>遍历当前所有的block文件，
    获取所有的transaction中coin_in和coin_out的coin地址。
        1.仅出现在coin_in中的则在mysql中设置为未花费。
        2.出现在coin_in中且出现在coin_out中的coin则设置为已花费。
</code></pre>

### 待完成

>* `区块链详细信息弹窗设计`
>* `修复查找结果的bug`


## 当前已有功能

> * `用户注册登录`
> * `用户修改个人信息`
> * `用户上传数据`
> * `用户设定数据价格`
> * `用户添加数据收益者`
> * `用户查看历史上传数据`
> * `管理员审核数据`
> * `用户按照数据明和数据简介搜索数据`
> * `用户购买数据`
> * `用户下载数据`
> * `用户充值`(暂时不需要)
> * `用户查看审核等通知信息`
> * `用户上传数据进行唯一性验证【验证MD5】`
> * `数据侵权信息通知【上传时产生MD5冲突】`
> * `区块信息展示页面(需要设计详细信息的弹窗)`
> * `进行挖矿服务端的开发【另外开启一个线程进行挖矿服务】(当前为了debug设置为10秒)`
> * `收益自动分配【最多额外5人收益】`
> * `数据评分机制【1~5星级】`
> * `多个页面中的升序降序功能`
> * `主页显示区块信息`
> * `挖矿的block大小限制`
> * `挖矿的block产生时间设置`
> * `需要读取整条链的信息，成功将当前交易打包入链，删除当前的交易信息文件`
> * `区块数据coin与数据库进行定期同步`

## 待完成功能

> * `使用区块链进行数据检索`

#### 数据库，Download表改为 Purchase表， 其他表有字段有修改；
#### 可以先尝试
>`python3 manage.py makemigrations  BSCapp`
>
>`python3 manage.py migrate`
#### 如果遇到问题，尝试重新创建数据库。


## 数据库重新建立(设置utf8编码)
>`mysql -u root -p`
>
>`输入mysql密码`
>
> 如果原来的database需要删除：
>> `drop database bsc_db;`
>
> 如果原来的不存在，需要重新创建,运行以下指令，设定为utf8编码格式:
>
> `create database bsc_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;`
>
## 数据库迁移指令
>`python3 manage.py makemigrations BSCapp`
>
>`python3 manage.py migrate`

## 创建超级用户指令
>`python3 manage.py createsuperuser`
>
>运行项目 `python3 manage.py runserver`
>删除block数据信息 `delete from BSCapp_block;`
>
>在浏览器网站中输入 `http://127.0.0.1:8000/admin/` 即可管理数据库

## 项目运行指令
>`python3 manage.py runserver`
>
>在浏览器网站中输入 `127.0.0.1:8000/Index` 默认端口为8000
>
>点击右上角的login，里面可以选择注册还是登陆

## Done:
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

用户表 BSCapp_user

| 用户id | 登录名          | 密码    | 邮箱 |真实姓名| 手机号 |身份证号 |所在公司 |个人头衔| 居住地|
| ----- |:-------------:| :------:|:-------:| :----:| :----:| :----:| :----:| :----:| :----:|

数据表 BSCapp_data

| 数据id | 数据拥有者id| 数据名| 数据简介信息 | 数据上传时间 | 数据来源 |数据保存格式 |数据tag |数据审核状态|数据md5值|数据大小|数据下载量|数据购买量|数据定价|数据保存服务器地址|数据评级|评价数据人数|
| ----- |:-------------:| :------:|:-------:| :----:| :----:| :----:| :----:|:----:|:----:|:----:|:----:| :----:|:----:|:----:|:----:|:----:|

交易表 BSCapp_transaction

| 交易id | 购买方id   | 出售方id    | 数据id |购买时间| 购买价格 |交易者对数据评级|数据评价内容(暂时无用)|数据上次下载时间|
| ----- |:----------:| :------:|:-------:| :----:| :----:|:----:|:----:|:----:|


coin表 BSCapp_coin

| coin_id | coin拥有者id | coin大小 | coin是否花费 | coin创建时间|
| ----- |:-------------:| :------:|:-------:|:-------:|


用户充值表 BSCapp_recharge

| 充值id | 用户id | 充值时间| 充值信用大小 | 充值前账户余额|充值后账户余额|充值生成的coin_id|
|---| :-------------: |:-------------:| :------:|:-------:| :----:|:---:|

用户钱包表 BSCapp_wallet (仅用于展示，实际需要遍历区块链)

| 用户id | 钱包余额|
| ----- |:------:|

用户下载数据表  BSCapp_download  (用户id和 已下载数据id作为联合主键)

| 用户id | 已下载数据id|
| ----- |:------:|

管理员表  BSCapp_admin

| 用户id | 管理员登录名|管理员密码|
| ----- |:------:|:------:|

管理员审核数据表  BSCapp_review

| 管理员id | 所审核数据id | 数据状态 | 审核时间|
| ----- |:------:|:------:|:---:|

通知信息表  BSCapp_notice

| 通知信息id | 信息发送者id | 信息接收者id | 信息内容 | 信息是否被查看|
| ----- |:------:|:------:|:---:|:---:|

收益分配表  BSCapp_Income

| 数据id | 收益用户名 | 收益占比 |
| ----- |:------:|:------:|

区块信息表  BSCapp_block

| 区块高度height | 区块产生时间戳 | 区块大小(B) | 区块包含的交易数量 | 当前区块hash值|
| ----- |:------:|:------:|:---:|:---:|



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
