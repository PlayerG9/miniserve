#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
from config import args
import qr_code_printer

if __name__ == '__main__':
    import uvicorn
    print(args)
    qr_code_printer.run_background()
    uvicorn.run("main:app", host=args.host, port=args.port, app_dir=os.path.dirname(__file__), workers=args.worker)
