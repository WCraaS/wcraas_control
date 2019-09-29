# -*- coding: utf-8 -*-

"""The WCraaS Control module is responsible for the orchestration of tasks in the platform."""

import asyncio
import logging
import traceback
import aio_pika

from collections import deque
from enum import unique, IntEnum

from aio_pika.patterns import RPC
from aioredis import create_redis_pool

from wcraas_common import AMQPConfig, WcraasWorker
from wcraas_control.config import RedisConfig


__all__ = ("RedisLockState", "ControlWorker")


@unique
class RedisLockState(IntEnum):
    FREE = 0
    LOCK = 1
    DONE = 2
    FAIL = 3


class ControlWorker(WcraasWorker):
    """
    Control Worker for the WCraaS platfrom, responsible for the orchestration of tasks.

    >>> from wcraas_control.config import Config
    >>> cn = ControlWorker(*Config.fromenv())
    """

    def __init__(
        self,
        amqp: AMQPConfig,
        redis: RedisConfig,
        interval: int,
        loglevel: int,
        *args,
        **kwargs,
    ):
        super().__init__(amqp, loglevel)
        self.redis = redis
        self.poll_interval = interval
        self.logger = logging.getLogger("wcraas.control")
        self.logger.setLevel(loglevel)

    async def crawl(self, url: str):
        """
        Given URL orchestrate crawling of the target.

        :param url: Entrypoint URL for crawling the target.
        :type url: string
        """
        redis_pool = await create_redis_pool(self.redis)
        urls = deque((url,))
        async with self._amqp_pool.acquire() as channel:  # type: aio_pika.Channel
            rpc = await RPC.create(channel)
            while True:
                _url = urls.pop()
                # Acquire lock for the URL
                await redis_pool.set(_url, RedisLockState.LOCK.value)
                # Delegate discovery through RPC
                try:
                    resp = await rpc.proxy.discover(url=_url)
                except Exception as err:
                    self.logger.error(traceback.format_exc())
                    self.logger.error(err)
                    await redis_pool.set(_url, RedisLockState.FAIL.value)
                    continue
                await redis_pool.set(_url, RedisLockState.DONE.value)
                # For all inbound URLs (== same protocol, host, port) check if the URL
                # exists in redis & is not FREE; if so skip it otherwise add it to the
                # deque of URLs to crawl.
                for inbound_url in resp["data"]["inbound"]:
                    if await redis_pool.get(inbound_url):
                        continue
                    urls.append(inbound_url)
                # If there are no URLs left to crawl exit
                if not urls:
                    break
                await asyncio.sleep(self.poll_interval)

    def __repr__(self):
        return f"{self.__class__.__name__}(amqp={self.amqp}, redis={self.redis}, interval={self.poll_interval}, loglevel={self.loglevel})"
