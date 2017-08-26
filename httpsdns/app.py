#!/usr/bin/env python
# -*- coding:utf8 -*-

import requests
import dns.resolver
from flask import Flask
from flask import request, Response, abort, jsonify
import config
from httpsdns.utils.logger import logger

## init logger https://github.com/senko/python-logger/blob/master/logger.py
logger.basicConfig()

app = Flask(__name__)

@app.route(config.FLASK_URI, methods=['GET'])
def dns_resolver():
    if not request.method == 'GET':
        abort(400)
        return
    ## get params
    name = request.args.get("name", "")
    if name == "":
        abort(400)
        return
    logger.info("GET args name %r" % (name))
    ## do resolve
    url = config.URL_DNSHTTPS
    params = {}
    params["name"] = name
    headers = {}
    ## using Safari UA string
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
    r = requests.get(url = url,
            params = params,
            headers = headers)
    logger.info("GET result status_code %r" % (r.status_code))
    if not r.status_code == 200:
        abort(400)
        return
    logger.info("GET result content %r" % (r.content))
    results = r.json()
    return (jsonify(results), r.status_code)

@app.route(config.FLASK_LOCAL_URI, methods=['GET'])
def dns_local_resolver():
    if not request.method == 'GET':
        abort(400)
        return
    ## get params
    name = request.args.get("name", "")
    dnstype = request.args.get("type", "A")
    if name == "":
        abort(400)
        return
    if not dnstype in ["A", "CNAME", "MX"]:
        abort(400)
        return
    logger.info("GET args name %r" % (name))
    logger.info("GET args type %r" % (dnstype))
    ## do resolve
    results = {}
    try:
        ## question setion returns
        results_question = []
        results_que = {}
        results_que["name"] = name
        results_que["type_text"] = dnstype
        results_question.append(results_que)
        results['Question'] = results_question
        answers = dns.resolver.query(name, dnstype)
        ## answer setion returns
        results_answers = []
        for ans in answers:
            results_ans = {}
            results_ans["data"] = ans.to_text()
            results_ans["type"] = ans.rdtype
            # results_ans["TTL"] = ans.validate()
            results_answers.append(results_ans)
        results['Answer'] = results_answers
    except Exception as e:
        logger.error("ERROR %r" %(e.args))
        abort(406)
        return
    logger.info("GET result content %r" % (str(results)))
    return (jsonify(results), 200)
