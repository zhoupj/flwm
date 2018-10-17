from multiprocessing.pool import ThreadPool  # 导入线程池

class PoolManger:

    def __init__(self,size=4):
        self.__pool = ThreadPool(size) # 参数是线程池的数量，默认为1

    def run(self,work,kwd=()):
        self.__pool.apply_async(work,kwd)

    def close(self):
        self.__pool.close()  # 关闭线程池 不再提交任务
        self.__pool.join()