import json


def loadLabel(dataSetName):
    rootPath = "/home/jiajie/test/data/" + dataSetName
    count = 0
    labelList = []
    for line in open(rootPath + "/tagId"):
        if len(line.strip('\n').split("_")) > 1:
            labelList.append(line.strip('\n').split("_")[1])
        else:
            labelList.append(line.strip('\n'))
        count += 1
    labelList = list(set(labelList))


def loadClass(dataSetName):
    try:
        labelList = []
        with open("/home/jiajie/test/data/" + dataSetName + "/Class", 'r') as load_f:
            load_dict = json.load(load_f)
        for (k, v) in load_dict.items():
            tempMap = {
                'name': k,
                'label': v,
                'color':    ''
            }
            labelList.append(tempMap)
    except Exception:
        responseMap = {
            'labelList': '',
            'code': 500,
            'message': '标签文件解析错误！'
        }
        print('标签文件解析错误！')
    else:
        responseMap = {
            'labelList': labelList,
            'code': 200,
            'message': '成功！'
        }
    responseMap = json.dumps(responseMap)
    return responseMap


if __name__ == "__main__":
    loadClass("medicalNER")
