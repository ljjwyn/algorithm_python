import redis
# 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


def setNowModelProcess(uid, res, batchId):
    process = {"res": res, "batchId": batchId}
    r = redis.Redis(connection_pool=pool)
    # 将建模进度存到redis设置过期时间为1小时。这里将不断更新最新的建模进度
    try:
        r.set(uid+"_modelling", process, ex=3600)
    except BaseException as e:
        print("redis连接频繁")
        print(e)
