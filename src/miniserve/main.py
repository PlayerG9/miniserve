#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import fastapi.middleware.cors
import fastapi.middleware.gzip
# import fastapi.staticfiles
# baize is needed for better FileResponses because starlette doesn't support range-headers
from baize.asgi.staticfiles import Files as StaticFiles, Pages as StaticPages
from config import args, __version__
import auth
from api import api as api_router
from preview import preview as preview_router, lowRes as lowRes_router


app = fastapi.FastAPI(
    title="miniserve",
    version=__version__,
    docs_url=None,
    dependencies=[auth.auth_dependency] if args.auth else None,
    # redoc_url=None,
)
app.add_middleware(
    fastapi.middleware.gzip.GZipMiddleware,
)
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=list(auth.get_origins()),
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(preview_router)
app.include_router(lowRes_router)
app.mount(
    "/files",
    StaticFiles(directory=args.root)
)
app.mount(
    "/",
    StaticPages(directory=os.path.join(os.path.dirname(__file__), "web-ui"))
)
