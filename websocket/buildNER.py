import json


def buildNER():
    labelMap = {
        '疾病和诊断': 'DAD',
        '检查': 'INS',
        '检验': 'TES',
        '手术': 'OPA',
        '药物': 'DRU',
        '解剖部位': 'ANA',
        '影像检查': 'IMA',
        '实验室检验': 'LAB'
    }
    f = open("/home/jiajie/test/data/medical/medical.json")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    labelAllChars = []
    while line:
        entity = eval(line)
        labelChars = []
        tempSentence = entity.get('originalText')
        for char in tempSentence:
            if char == '，' or char == '。':
                tempLabel = {
                    "char": char,
                    "label": "splice"
                }
            else:
                tempLabel = {
                    "char": char,
                    "label": "O"
                }
            labelChars.append(tempLabel)
        labelList = entity.get('entities')
        for L in labelList:
            print(L.get('label_type'))
            labelType = labelMap.get(L.get('label_type'))
            startIndex = L.get('start_pos')
            endIndex = L.get('end_pos')
            labelChars[startIndex]['label'] = 'B_' + labelType
            for index in range(1, endIndex - startIndex):
                labelChars[startIndex + index]['label'] = 'I_' + labelType
        labelAllChars.extend(labelChars)
        line = f.readline()
    f.close()
    count = 0
    for index in range(1, len(labelAllChars)):
        if labelAllChars[index].get('label') == 'splice' and labelAllChars[index - 1].get('label') != 'splice':
            with open("/home/jiajie/test/data/medical/medicalOut", "a") as dump_f:
                dump_f.write('\n')
        elif labelAllChars[index].get('label') != 'splice' and labelAllChars[index].get('char') != '':
            sentence = labelAllChars[index].get('char') + ' ' + labelAllChars[index].get('label') + '\n'
            with open("/home/jiajie/test/data/medical/medicalOut", "a") as dump_f:
                dump_f.write(sentence)
        elif labelAllChars[index].get('char') == '':
            print("空格")
        else:
            print("处理到第：{}个句子".format(count))
            count += 1


if __name__ == "__main__":
    buildNER()
