#
# Copyright (C) 2020 Adam Meily
#
# This file is subject to the terms and conditions defined in the file 'LICENSE', which is part of
# this source code package.
#
import sys
import subprocess

if sys.platform == 'win32':
    def ping_windows(target: str, count: int = 1, timeout_ms: int = 1000) -> bool:
        try:
            subprocess.check_call(['ping', '-n', str(count), '-w', str(timeout_ms), target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            ret = False
        else:
            ret = True
        return ret


    ping = ping_windows
else:
    def ping_nix(target: str, count: int = 1, timeout_ms: int = 1000) -> bool:
        timeout = int(timeout_ms / 1000)
        if timeout_ms % 1000:
            timeout += 1

        try:
            subprocess.check_call(['ping', '-c', str(count), '-W', str(timeout), target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            ret = False
        else:
            ret = True
        return ret


    ping = ping_nix
