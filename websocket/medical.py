import json


def buildTextClassify():
    with open("/home/jiajie/test/data/medical/CMID.json", 'r') as load_f:
        load_dict = json.load(load_f)
    head = "sentences,label\n"
    # 病症 药物 治疗方案 其他
    labelList = ['病症', '药物', '治疗方案', '其他']
    with open("/home/jiajie/test/data/medical/textClassifyOut", "a") as dump_f:
        dump_f.write(head)
    count = 0
    for entity in load_dict:
        if count >= 7754:
            print(entity)
            labelContents = entity['label_4class'][0]
            index = str(labelList.index(labelContents))
        else:
            labelContents = entity['label_4class'][0].split('\'')[1]
            index = str(labelList.index(labelContents))
        print("----写入第：{}个----句子标签:{}".format(count, entity['label_4class'][0].split('\'')))
        sentence = entity['originalText'].replace(',', '。')+","+index+"\n"

        with open("/home/jiajie/test/data/medical/textClassifyOut", "a") as dump_f:
            dump_f.write(sentence)
        count += 1

    # Write your code here
    # i = 1
    # f = open("/home/jiajie/test/data/medical/textClassifyOut", "a")  # 利用追加模式,参数从w替换为a即可
    # while i <= 10:
    #     f.write("{}\n".format(i))
    #     i = i + 1
    # f.close()


if __name__ == "__main__":
    buildTextClassify()
