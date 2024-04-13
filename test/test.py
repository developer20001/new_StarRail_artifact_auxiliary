# import requests
#
# response = requests.get('https://api.github.com/repos/SkeathyTomas/genshin_artifact_auxiliary/releases/latest')
# print(response.json()['tag_name'])

# import os
#
# folder = os.path.expanduser('~/Documents')
# folder = folder + '/keqing'
#
# # os.chdir(folder)
# os.startfile(folder)
# print("弹窗")

class Data:
    def __init__(self):
        print("Data")
        self.str = "Data"

    def getStr(self):
        return self.str

dataManager = Data()


# print(dataManager.getStr())


# a = ["1","2", "3"]
#
#
# print(a.index("3"))