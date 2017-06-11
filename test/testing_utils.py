from omnithumb.worker import Worker

class RunOnceWorker(Worker):
    '''
    Worker that just goes through a given queue
    '''
    def __init__(self, queue):
        self.queue = queue

    @property
    def running(self):
        return bool(self.queue)

    async def get_next(self):
        return self.queue.pop(0)

    async def check_download(self, foreign_resource):
        self.check_download_was_called = True
        return True

    async def check_convert(self, converter, in_r, out_r):
        self.check_convert_was_called = True
        return True

