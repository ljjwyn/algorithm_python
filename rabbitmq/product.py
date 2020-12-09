import json
import pika


def sendProcess(modelUid, buildProcess):
    # 建立连接
    userx = pika.PlainCredentials("guest", "guest")
    conn = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, '/', credentials=userx))
    # 开辟管道
    channelx = conn.channel()
    if modelUid == '':
        mqQueues = "modelProcess_init"
    else:
        mqQueues = "modelProcess_" + modelUid
    # 声明队列，参数为队列名
    print("--------发送数据开始-----------:")
    print(buildProcess)
    channelx.queue_declare(queue=mqQueues, durable=True)
    # 发送数据，发送一条，如果要发送多条则复制此段
    channelx.basic_publish(exchange="",
                           routing_key=mqQueues,  # 队列名
                           body=buildProcess  # 发送的数据
                           )
    print("--------发送数据完成-----------:")
    conn.close()


def sendTestProcess(modelUid, buildProcess):
    # 建立连接
    userx = pika.PlainCredentials("guest", "guest")
    conn = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, '/', credentials=userx))
    # 开辟管道
    channelx = conn.channel()
    if modelUid == '':
        mqQueues = "modelTestProcess_init"
    else:
        mqQueues = "modelTestProcess_" + modelUid
    # 声明队列，参数为队列名
    print("--------模型评估发送数据开始-----------:")
    print(buildProcess)
    channelx.queue_declare(queue=mqQueues, durable=True)
    # 发送数据，发送一条，如果要发送多条则复制此段
    channelx.basic_publish(exchange="",
                           routing_key=mqQueues,  # 队列名
                           body=buildProcess  # 发送的数据
                           )
    print("--------模型评估发送数据完成-----------:")
    conn.close()


