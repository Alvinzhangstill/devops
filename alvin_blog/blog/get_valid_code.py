from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def get_random_str():
    random_digit = str(random.randint(0, 9))
    lower_str = chr(random.randint(65, 90))
    upper_str = chr(random.randint(97, 122))
    return random.choice([random_digit, lower_str, upper_str])


def get_valid(request):
    img = Image.new('RGB', (260, 33), get_random_color())
    draw = ImageDraw.Draw(img)
    # static前不用加/
    font = ImageFont.truetype('static/font/KumoFont.ttf', size=30)

    valid_code_char = ''
    for i in range(5):
        random_char = get_random_str()
        draw.text((20 + i * 50, 1), random_char, get_random_color(), font)
        # 保存验证码
        valid_code_char += random_char

    # 将验证码设置cookie方便后续验证
    request.session['valid_code'] = valid_code_char

    print("valid_code_char:", valid_code_char)

    # # 噪点噪线
    # width = 260
    # height = 33
    #
    # # 划线
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 画点
    # for i in range(50):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 文件操作从磁盘中读取数据相对较慢，改用内存句柄
    # with open('valid_code_img.png','wb')as f:
    #     img.save(f,'png')
    #
    # with open('valid_code_img.png','rb')as f:
    #     data=f.read()

    # 内存操作
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()

    return data
