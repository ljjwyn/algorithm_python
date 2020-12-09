import queue

q = queue.Queue(maxsize=10)


def insertQueue1(process):
    q.put(process)
    print('Finished')


def pullQueue():
    if q.qsize()==0:
        return "Queue is empty"
    out = q.get()
    print("pullQueue left:{},out element:{}".format(q.qsize(), out))
    return out


def getQ():
    return q


if __name__ == '__main__':
    process = {"id": 1, "acc": 0.45}
    insertQueue1(str(process))
    process = {"id": 2, "acc": 0.46}
    insertQueue1(str(process))

    # pullQueue()
