# -*- coding: utf-8 -*-
# @Time    : 2018/4/1 上午12:11
# @Author  : 伊甸一点
# @FileName: testCode.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io
import random
from PIL import Image, ImageDraw

def verify_code():
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 60), 255, random.randrange(0, 50))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # font = ImageFont.truetype('FreeMono.ttf', 23)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(70, 255), random.randrange(200, 255))
    # 9，绘制4个字
    draw.text((5, 8), rand_str[0],  fill=fontcolor)
    draw.text((25, 8), rand_str[1], fill=fontcolor)
    draw.text((50, 8), rand_str[2], fill=fontcolor)
    draw.text((75, 8), rand_str[3], fill=fontcolor)
    # 9，用完画笔，释放画笔
    im.show()
    del draw
    # 10，存入session，用于做进一步验证
    # request.session['verifycode'] = rand_str
    # 11，内存文件操作
    # buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    # im.save(buf, 'png')
    im.save("imfor0010.jpg", "jpeg")
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    # return HttpResponse(buf.getvalue(), 'image/png')

verify_code()