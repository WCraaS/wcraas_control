# -*- coding: utf-8 -*-

"""Console script for wcraas_control."""
import asyncio
import sys
import click

from wcraas_control import ControlWorker, Config


@click.command()
@click.argument("target")
def main(target):
    worker = ControlWorker(*Config.fromenv())
    asyncio.get_event_loop().run_until_complete(worker.crawl(target))


@click.command()
def list_collections():
    worker = ControlWorker(*Config.fromenv())
    resp = asyncio.get_event_loop().run_until_complete(worker.list_collections())
    print(resp)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
