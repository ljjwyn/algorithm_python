import json
import time
from datetime import timedelta
import operator
import torch
import torch.utils.data.dataloader as DataLoader

from connect_mysql import updateModelTestAccuracy
from rabbitmq.product import sendTestProcess


# 模型测试模块
from testBERT.BERT import Model
from testBERT.bert_CNN import Model_CNN
from testBERT.bert_RCNN import Model_RCNN
from torch_NER.BiLSTM_CRF import BiLSTM_CRF
from torch_NER.CRF import CRF
from torch_NER.modelHelp import getCharLenth, getTagLenth
from dataset import classfiyDataset
from torch_NER.nerDataSet import nerDataSet
from torch_model.BiLSTM import BiLSTM_Attention


def modelTest(uid, dataSetName, modelName, configMap, algorithm):
    batch_size = int(configMap["batch_size"])

    vocab_size = 21128
    start_time = time.time()
    if algorithm == 1:
        model = Model(configMap)
    elif algorithm == 2:
        model = Model_CNN(configMap)
    elif algorithm == 3:
        model = Model_RCNN(configMap)
    elif algorithm == 4:
        rootPath = "/home/jiajie/test/data/" + dataSetName
        class_list = [x.strip() for x in open(rootPath + "/Class").readlines()]
        num_classes = len(class_list)
        model = BiLSTM_Attention(vocab_size, configMap['embedding_dim'], configMap['n_hidden'], num_classes)
    elif algorithm == 5:
        evalNER(uid, dataSetName, modelName, configMap, start_time)
        return None
    else:
        print("错误的algorithm值，没有对应的模型")
        return json.dumps({"code": 500, "message": "错误的algorithm参数没有对应的模型"})

    model.load_state_dict(torch.load("/home/jiajie/test/data/models/" + modelName))

    test_dataset = classfiyDataset(rootPath + "/Test", int(configMap['sequence_length']), 1, 1)
    test_loader = DataLoader.DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    with torch.no_grad():
        correct = 0
        total = 0
        attention_sum = []
        for i, (input_batch) in enumerate(test_loader):
            sentence = input_batch[0]
            labels = input_batch[1].data
            outputs, attention = model(sentence)
            attention_sum.extend(attention.tolist())
            _, predicted = torch.max(outputs.data, 1)
            total = labels.size(0)
            correct = (predicted == labels).sum()
            time_dif = get_time_dif(start_time)
            recordMap = {
                'correct': correct.item(),
                'total': total,
                'batchId': i,
                'accuracy': int(100*correct / total)/10,
                'flag': 0,
                'time': str(time_dif)
            }
            time.sleep(2)

            sendTestProcess(uid, json.dumps(recordMap))
        sendTestProcess(uid, json.dumps({'accuracy': int(100 * correct / total)/10, 'flag': 1}))
        updateModelTestAccuracy(uid, int(100 * correct / total))
        print('Accuracy of the model on the {} test images: {} %'.format(total, 100 * correct / total))


def evalNER(uid, dataSetName, modelName, configMap, start_time):
    batch_size = int(configMap["batch_size"])
    lstm_hiddens = int(configMap["lstm_hiddens"])
    lstm_layers = int(configMap["lstm_layers"])
    dropout = float(configMap["dropout"])
    embedding_dim = int(configMap["embedding_dim"])
    charLenth = getCharLenth(dataSetName)
    tagSize = getTagLenth(dataSetName)
    args_crf = dict({'target_size': tagSize, 'device': "cpu"})
    model_CRF = CRF(**args_crf)
    model = BiLSTM_CRF(embed_num=charLenth, embed_dim=embedding_dim, label_num=tagSize,
                       paddingId=0, dropout_emb=dropout, dropout=dropout,
                       lstm_hiddens=lstm_hiddens, lstm_layers=lstm_layers,
                       pretrained_embed=False,
                       device="cpu", CRF=model_CRF)
    model.load_state_dict(torch.load("/home/jiajie/test/data/models/" + modelName))
    model.eval()

    s = nerDataSet(dataSetName, 1, batch_size)
    gold_labels = []
    dev_dataset = DataLoader.DataLoader(s, batch_size=batch_size, shuffle=False, num_workers=0)
    acc_count = 0
    for i, (input_batch) in enumerate(dev_dataset):
        batchCount = 0
        sentencesLenth = input_batch[4].numpy().tolist()
        path_score, best_paths = model(input_batch[0], sentencesLenth, input_batch[3])
        # path_score, best_paths = model_crf(outputs, input_batch[3])
        for index in range(len(input_batch[2])):
            inst_lenth = input_batch[4][index].item()
            inst_label = input_batch[2][index].numpy()[:inst_lenth]
            gold_labels.append(inst_label)
            label_ids = best_paths[index].data.numpy()[:inst_lenth]
            label = []
            accLabel = operator.eq(label_ids.tolist(), inst_label.tolist())
            if accLabel is True:
                acc_count += 1
                batchCount += 1
        time_dif = get_time_dif(start_time)
        recordMap = {
            'correct': batchCount,
            'total': batch_size,
            'batchId': i,
            'accuracy': int(100 * batchCount / batch_size) / 10,
            'flag': 0,
            'time': str(time_dif)
        }
        sendTestProcess(uid, json.dumps(recordMap))
        time.sleep(2)
        print('acc_count {} batch_size: {}'.format(batchCount, batch_size))
        if i == 99:
            break
    acc = round(acc_count / (batch_size * 100),2)
    sendTestProcess(uid, json.dumps({'accuracy': int(100 * acc) / 10, 'flag': 1}))
    updateModelTestAccuracy(uid, int(100 * acc))
    print('Accuracy of the model on the {} test images: {} %'.format(batch_size * 100, acc))
    return acc


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))


if __name__ == "__main__":
    tempMap = {'LR': 0.01, 'epoch': 3, 'sequence_length': 25, 'n_hidden': 5, 'batch_size': 128, 'embedding_dim': 50}
    modelTest('34324', 'THUCNews', 'fa9a文本分类_1126.ckpt', tempMap, 4)
