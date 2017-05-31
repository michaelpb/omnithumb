import logging
import asyncio
import aiohttp
import async_timeout

from enum import Enum
log = logging.getLogger()

class Task(Enum):
    FUNC = 1          # Synchronous function
    DOWNLOAD = 2      # Downloading a file
    CONVERT = 3       # Running a converter

DOWNLOAD_TIMEOUT = 20
DOWNLOAD_CHUNK_SIZE = 1024

class Worker:
    '''
    Simple Co-Routine queue consumer
    '''
    async def run(self):
        while self.running:
            # Queue up consuming next item
            task_type, args = await self.queue.get()

            # Determine the type of task, and possibly skip if we have
            # it "locked" that we are already doing it
            if task_type == Task.FUNC:
                method = self.run_func

            elif task_type == Task.DOWNLOAD:
                if not await self.check_download(*args):
                    log.debug('Already downloading %s' % repr(task_args))
                    continue
                method = self.run_download

            elif task_type == Task.CONVERT:
                if not await self.check_convert(*args):
                    log.debug('Already converting %s' % repr(task_args))
                    continue
                method = self.run_convert

            # Queue it up and run it
            try:
                await method(*args)
            except Exception as e:
                log.error('Error in task: "%s"' % repr(e))

    async def run_func(self, func, *func_args):
        func(*func_args)

    async def run_download(self, foreign_resource):
        url = foreign_resource.url_string
        with foreign_resource.cache_open('wb') as f_handle:
            await self.download_async(url, f_handle)

    async def download_async(self, url, f_handle):
        with async_timeout.timeout(DOWNLOAD_TIMEOUT):
            async with self.aiohttp.get(url) as response:
                while True:
                    chunk = await response.content.read(DOWNLOAD_CHUNK_SIZE)
                    if not chunk:
                        break
                    f_handle.write(chunk)
                return await response.release()

    async def run_convert(self, converter, in_resource, out_resource):
        # TODO make async
        converter.convert(in_resource, out_resource)

class AioWorker(Worker):
    '''
    Uses an asyncio Queue to enqueue tasks
    '''
    def __init__(self, queue):
        self.queue = queue
        self.running = True
        self.aiohttp = aiohttp.ClientSession(loop=asyncio.get_event_loop())

        # Sets that 
        self.downloading_resources = set()
        self.converting_resources = set()

    async def enqueue(self, task_type, args):
        return await self.queue.put((task_type, args))

    async def get_next(self):
        # Queue up consuming next item
        return await self.queue.get()

    async def check_download(self, foreign_resource):
        return True # TODO
        if foreign_resource in self.downloading_resources:
            return False
        self.downloading_resources.add(foreign_resource)
        return True

    async def check_convert(self, converter, in_r, out_r):
        return True # TODO
        if (in_r, out_r) in self.converting_resources:
            return False
        self.converting_resources.add((in_r, out_r))
        return True

