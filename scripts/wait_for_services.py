#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import time
import os
import sys
from typing import Dict, Tuple


def main() -> None:
    """Main."""

    services: Dict[str, Tuple[str, int]] = {"db": ("", 0), "cache": ("", 0)}

    port = 5432
    if os.environ.get("DB_PORT"):
        port = int(os.environ["DB_PORT"])
    host = os.environ.get("DB_HOST") or "localhost"
    services["db"] = (host, port)

    port = 6379
    if os.environ.get("CACHE_PORT"):
        port = int(os.environ["CACHE_PORT"])
    host = os.environ.get("CACHE_HOST") or "localhost"
    services["cache"] = (host, port)

    for service, tup in services.items():
        (host, port) = tup
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Trying to connect on service '{}' {}:{}".format(service, host, port))

        max_retries = 60
        retry_number = 0
        while retry_number < max_retries:
            try:
                s.connect((host, port))
                s.close()
                print("Connected!")
                break
            except socket.error:
                time.sleep(1)
                print("Couldn't connect yet...sleping for 1s")
                retry_number += 1
                if retry_number == max_retries:
                    print("Max number of retries has been reached. Aborting!")
                    sys.exit(1)


if __name__ == "__main__":
    main()
