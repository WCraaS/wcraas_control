import logging

from collections import namedtuple
from environs import Env

from wcraas_common import AMQPConfig


class RedisConfig(namedtuple("RedisConfig", ("host", "port"))):
    __slots__ = ()

    @classmethod
    def fromenv(cls):
        """
        Create a `wcraas_control.RedisConfig` from Environment Variables.

        >>> conf = RedisConfig.fromenv()
        >>> type(conf)
        <class 'config.RedisConfig'>
        >>> conf._fields
        ('host', 'port')
        >>> conf.host
        'localhost'
        >>> conf.port
        6379
        """
        env = Env()
        env.read_env()

        with env.prefixed("REDIS_"):
            return cls(host=env.str("HOST", "localhost"), port=env.int("PORT", 6379))


class Config(namedtuple("Config", ("amqp", "redis", "interval", "loglevel"))):
    __slots__ = ()

    @classmethod
    def fromenv(cls):
        """
        Create a `wcraas_control.Config` from Environment Variables.

        >>> conf = Config.fromenv()
        >>> type(conf)
        <class 'config.Config'>
        >>> conf._fields
        ('amqp', 'redis', 'interval', 'loglevel')
        >>> conf.amqp
        AMQPConfig(host='localhost', port=5672, user='guest', password='guest')
        >>> conf.redis
        RedisConfig(host='localhost', port=6379)
        >>> conf.interval
        10
        >>> conf.loglevel
        20
        """
        env = Env()
        env.read_env()

        return cls(
            amqp=AMQPConfig.fromenv(),
            redis=RedisConfig.fromenv(),
            interval=env.int("POLLING_INTERVAL", 10),
            loglevel=getattr(logging, env.str("LOGLEVEL", "INFO")),
        )
