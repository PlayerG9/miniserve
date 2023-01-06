#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import getpass
import hmac
import fastapi.security
from config import args


security = fastapi.security.HTTPBasic()


if args.auth is Ellipsis:
    # use system password
    import spwd
    import crypt

    try:
        spwd.getspnam(getpass.getuser())
    except PermissionError:
        raise PermissionError("unable to verify system password. please provide one with '--auth password'")

    @fastapi.Depends
    def auth_dependency(credentials: fastapi.security.HTTPBasicCredentials = fastapi.Depends(security)):
        print(credentials)
        username = credentials.username
        password = credentials.password
        try:
            enc_pwd = spwd.getspnam(username)
        except KeyError:
            raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)
        if not hmac.compare_digest(crypt.crypt(password, enc_pwd), enc_pwd):
            raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)
else:
    @fastapi.Depends
    def auth_dependency(credentials: fastapi.security.HTTPBasicCredentials = fastapi.Depends(security)):
        print(credentials)
        username = credentials.username
        print(username, getpass.getuser())
        if username.casefold() != getpass.getuser().casefold():
            raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)
        password = credentials.password
        if not hmac.compare_digest(password, args.auth):
            raise fastapi.HTTPException(fastapi.status.HTTP_401_UNAUTHORIZED)
