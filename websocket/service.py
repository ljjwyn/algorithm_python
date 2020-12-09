import asyncio
import functools
import queue

import websockets


# 检测客户端权限，用户名密码通过才能退出循环

q = queue.Queue(maxsize=10)


async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket, other_param):
    while True:
        # information = other_param.get()
        # print("other_param", information)
        # recv_text = await websocket.recv()
        # response_text = "your submit context:"+recv_text+information
        # print("recv_text", recv_text+information)
        # await websocket.send(response_text)
        for index in range(0, q.qsize()):
            out = q.get()
            print("out", out)
            await websocket.send(out)


def startSocket():
    # 把ip换成自己本地的ip
    # start_server = websockets.serve(main_logic, '127.0.0.1', 5678)
    start_server = websockets.serve(functools.partial(main_logic, other_param=q), '127.0.0.1', 5678)
    # 如果要给被回调的main_logic传递自定义参数，可使用以下形式
    # 一、修改回调形式
    # import functools
    # start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
    # 修改被回调函数定义，增加相应参数
    # async def main_logic(websocket, path, other_param)
    loop = asyncio.get_event_loop()
    # task = asyncio.ensure_future(coroutine)
    task = loop.create_task(start_server)
    print(task)
    loop.run_until_complete(task)

    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()


# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path, other_param):
    await check_permit(websocket)

    await recv_msg(websocket, other_param)


def insertQueue(process):
    q.put(process)
    print('Finished')


def pullQueue():
    if q.qsize()==0:
        return "Queue is empty"
    out = q.get()
    print("pullQueue left:{},out element:{}".format(q.qsize(), out))
    return out


def QLength():
    return q.qsize()


if __name__ == '__main__':
    process = {"id": 1, "acc": 0.45}
    insertQueue(str(process))
    process = {"id": 2, "acc": 0.46}
    insertQueue(str(process))
    startSocket()
    process = {"id": 3, "acc": 0.45}
    insertQueue(str(process))
    process = {"id": 4, "acc": 0.46}
    insertQueue(str(process))

