import copy

basePlayer = {
    "win": 0,
    "lose": 0,
    "state": 0  # 0:alive, 1:win, 2:lose
}

playerNum = 176
playersPool = [[],[],[],[],[],[],[],[],[],[],[],[]]

# 初始化玩家池
for i in range(playerNum):
    player = copy.deepcopy(basePlayer)
    player["name"] = "player" + str(i)
    playersPool[0].append(player)

runTimes = 15

for times in range(runTimes):
    print("第{}次匹配".format(times+1))
    lenNum = len(playersPool)-1
    for num in range(lenNum, -1, -1):
        # print("第{}组玩家".format(num))

        playersPoolItem = playersPool[num]
        # print(playersPoolItem)
        tempPool1 = []
        tempPool2 = []


        for index, player in enumerate(playersPoolItem):
            # print("第{}组玩家".format(index))

            if index % 2 == 0:
                if index+1 < len(playersPoolItem):
                    player["lose"] += 1
                    if player["lose"] < 3:
                        tempPool1.append(player)
                    else:
                        print(player["name"] + "淘汰")
                else:
                    # 无对手 不操作
                    print(player["name"] + "无对手")
                    tempPool1.append(player)
            else:
                player["win"] += 1
                if player["win"] < 12:
                    tempPool2.append(player)
                else:
                    # print()
                    print(player["name"] + "获胜")
                    # raise 111


        # 整理数据
        playersPool[num] = tempPool1
        if num+1 < len(playersPool):
            playersPool[num+1] += tempPool2


    print("第" + str(times+1) + "轮结束")
    print(playersPool)

