import pika

# 建立连接
userx = pika.PlainCredentials("guest", "guest")
conn = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", 5672, '/', credentials=userx))

# 开辟管道
channelx = conn.channel()

# 声明队列，参数为队列名
channelx.queue_declare(queue="modelProcess")


# 消息处理函数，执行完成才说明接收完成，此时才可以接收下一条，串行
def dongcallbackfun(v1, v2, v3, bodyx):
    messageJson = eval(bodyx.decode('utf-8'))
    print("得到的数据为:", messageJson)
    print(type(messageJson))


# 接收准备
channelx.basic_consume(
    "modelProcess",  # 队列名
    dongcallbackfun,  # 收到消息的回调函数
    True,  # 是否发送消息确认
                       )
print("-------- 开始接收数据 -----------")

# 开始接收消息
channelx.start_consuming()
