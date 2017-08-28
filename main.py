#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-28 17:46:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sanic
import aiohttp
from sanic.response import *

app = sanic.Sanic(__name__)


@app.middleware('request')
async def handle(request):

    async def streaming(response):
        chunk_size = 1024
        while True:
            body = await resp.content.read(chunk_size)
            if body is None:
                break
            response.write(body)

    url = request.url
    method = request.method.lower()
    body = request.body
    headers = request.headers
    cookies = request.cookies
    async with aiohttp.ClientSession(cookies=cookies) as session:
        method = getattr(session, method, 'None')
        print(url, body, headers, cookies, sep='\n')
        async with method(url, data=body, headers=headers) as resp:
            ret = await resp.read()
            if 'html' in resp.headers.get('Content-Type'):
                return html(ret.decode('utf8', errors='ignore'))
            return raw(ret)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
