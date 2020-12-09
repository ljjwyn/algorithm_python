import json
import time

import pika


def sendTest():
    count = 0
    value = 0.01
    loss = 1
    while count < 100:
        # 建立连接
        userx = pika.PlainCredentials("guest", "guest")
        conn = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, '/', credentials=userx))
        # 开辟管道
        channelx = conn.channel()
        channelx.queue_declare(queue="modelProcessTest", durable=True)

        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 发送数据，发送一条，如果要发送多条则复制此段
        channelx.basic_publish(exchange="",
                               routing_key="modelProcessTest",  # 队列名
                               body=json.dumps({"batchId": count, "train_acc": round(value, 2), "loss": round(loss, 2), "time":nowTime})  # 发送的数据
                               )
        count += 1
        value += 0.01
        loss -= 0.01
        time.sleep(2)
        print("--------发送数据完成-----------")
        conn.close()


if __name__ == '__main__':
    sendTest()
    t = int(time.time())
    print(t, type(t))

