'''图像识别、文字处理，考虑多种ocr方式'''

from PIL import ImageGrab, Image
from rapidocr_onnxruntime import RapidOCR
import re


def rapidocr(x, y, w, h):
    '''返回使用paddle ocr引擎识别及处理结果
    参数：
        x：截图坐标x
        y：截图坐标y
        w：截图宽度w
        h：截图高度h
    返回：
        basic：主词条等基本信息list
            名称，部位，主属性，数值，等级
            ['雷云之笼', '时之沙', '攻击力', '46.6%', '+20']
        result：副词条属性dict
            key：词条属性（含百分比差异说明）
            value；词条数值
            如：{'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
    '''

    result = orcImage(x, y, w, h)
    if not result:
        print('识别失败')
        return False
    # print(result)

    # 千位符（含误识别的.）兼容
    pattern_thou = '\d\.\d{3}|\d\,\d{3}'
    txt = [re.sub(pattern_thou, item.replace(',', '').replace('.', ''), item) for item in result]

    name = txt[0].\
        replace('者的', '莳者的'). \
        replace('臂罐', '臂鞲'). \
        replace('臂購', '臂鞲'). \
        replace('绝足锁', '绝足锁桎'). \
        replace("黑塔，", '黑塔'). \
        replace("黑塔」", '黑塔'). \
        replace("圳裂缆索", '坼裂缆索'). \
        replace("系因", '系囚'). \
        replace('铅石桔', '铅石梏铐').\
        replace('铅石枱', '铅石梏铐')
    parts = txt[1].replace("躯于", '躯干')
    lvl = txt[2]
    main_name = txt[3]
    main_digit = txt[4]
    basic = [name, parts, lvl, main_name, main_digit]

    # 中文和数字正则
    pattern_chinese = '[\u4e00-\u9fa5]+'
    pattern_digit = '\d+(\.\d+)?'

    result = {}
    for index in range(5, len(txt), 2):
        item = txt[index] + txt[index + 1]
        try:
            # 词条名称
            name = re.findall(pattern_chinese, item)
            name = name[0]
            # 数值
            digit = float(re.search(pattern_digit, item).group())
            # 兼容千位符
            if digit < 2:
                digit *= 1000
            if name in '速度':
                result['速度'] = digit
            elif name in '攻击力' and '%' in item:
                result['攻击力百分比'] = digit
            elif name in '攻击力':
                result['攻击力'] = digit
            elif name in '生命值' and '%' in item:
                result['生命值百分比'] = digit
            elif name in '生命值':
                result['生命值'] = digit
            elif name in '防御力' and '%' in item:
                result['防御力百分比'] = digit
            elif name in '防御力':
                result['防御力'] = digit
            elif name in '暴击率':
                result['暴击率'] = digit
            elif name in '暴击伤害':
                result['暴击伤害'] = digit
            elif name in '击破特攻':
                result['击破特攻'] = digit
            elif name in '效果命中':
                result['效果命中'] = digit
            elif name in '效果抵抗':
                result['效果抵抗'] = digit
            else:
                result[item] = 0
        except:
            result[item] = 0

    print(basic, result)
    return basic, result


def orcImage(x, y, w, h):
    result = False
    ocr = RapidOCR()
    tryTimes = 3
    flag = True
    while flag:
        tryTimes -= 1

        # 截屏与ocr识别
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img.save('src/grab.png')
        result, elapse = ocr('src/grab.png', use_det=True, use_cls=False, use_rec=True, text_score=0.35)
        # print(result)
        result = [item[1] for item in result]
        checkResult = check_data_compliance(result)
        if not checkResult:
            result = False
        if tryTimes <= 0 or checkResult:
            flag = False
    return result
def check_data_compliance(data):
    if len(data) != 13:
        print("数据长度不符合要求")
        return False
    if "" in data:
        print("数据中存在空值")
        return False
    if "0" in data:
        print("数据中存在0")
        return False
    return True


if __name__ == '__main__':
    # 截图坐标
    # x, y, w, h = (1808, 277, 377, 714) # 副词条
    # x, y, w, h = (1948, 200, 360, 70) # 圣遗物名称

    # ocr测试
    import time

    start = time.time()
    # ppocr(x, y, w, h)
    # rapidocr(x, y, w, h)

    result = orcImage('src/grab.png')
    print("_______________")
    print(result)

    end = time.time()
    print(end - start)

    # import score
    # print(score.cal_score(tesseract_ocr(x, y, w, h), '雷电将军'))
