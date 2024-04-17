'''计算圣遗物评分、词条数、词条强化次数'''

# 基础词条系数
coefficient = {
    "速度": 2.492308,
    '暴击率': 2,
    '暴击伤害': 1,
    '攻击力百分比': 1.5,
    '攻击力': 0.076535,
    '生命值百分比': 1.5,
    '生命值': 0.153071,
    '防御力百分比': 1.2,
    '防御力': 0.153071,
    '击破特攻': 1,
    '效果命中': 1.5,
    '效果抵抗': 1.5
}
# 平均单词条数值
average = {
    "速度": 2.3,
    '暴击率': 2.915,
    '暴击伤害': 5.83,
    '攻击力百分比': 3.89,
    '生命值百分比': 3.89,
    '防御力百分比': 4.86,
    '攻击力': 18.966667,
    '生命值': 37.933333,
    '防御力': 18.966667,
    '击破特攻': 5.83,
    '效果命中': 3.89,
    '效果抵抗': 3.89
}


def cal_score(ocr_result_sub, config):
    '''计算圣遗物评分、词条数、词条强化次数
    参数：
        ocr_result_sub: ocr识别结果中副词条dict
            {'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
        config: 角色配置dict
            {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0}
    返回：
        scores: 每个词条单独的评分列表list
            [0.0, 6.3, 5.4, 0.0]
        round(sums, 1): 总分float
            11.7
        owerupArray: 强化次数列表list
            [0, 1, 2, 1]
        round(entriesSum, 1): 有效词条数float
            4.5
    '''

    scores = []
    powerupArray = []
    sums = 0
    entriesSum = 0

    # 补分逻辑
    # print("补分逻辑")
    # print(ocr_result_sub)
    # print(ocr_result_main)
    # if ocr_result_main in config and config[ocr_result_main]>0:
    #     if ocr_result_main==

    for key, value in ocr_result_sub.items():
        # 兼容角色配置未区分百分比的情况
        if key == '生命值百分比' or key == '攻击力百分比' or key == '防御力百分比':
            key_s = key[:3]
        else:
            key_s = key

        score = round(value * config[key_s] * coefficient[key], 1)
        scores.append(score)
        sums += score

        # 计算强化次数
        try:
            powerup = round(value / average[key]) - 1
        except:
            powerup = 0
        powerupArray.append(powerup)

        # 计算有效词条数量
        if key_s in config and config[key_s] > 0:
            entries = value / average[key]
            # print(key, entries)
            entriesSum += entries

    # print(scores, round(sums, 1), powerupArray, round(entriesSum, 1))
    return scores, round(sums, 1), powerupArray, round(entriesSum, 1)
