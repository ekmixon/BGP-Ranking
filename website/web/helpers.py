#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

import pycountry  # type: ignore

from flask import request, session

from bgpranking.default import get_homedir


def src_request_ip(request) -> str:
    return request.headers.get('X-Real-IP') or request.remote_addr


@lru_cache(64)
def get_secret_key() -> bytes:
    secret_file_path: Path = get_homedir() / 'secret_key'
    if (
        not secret_file_path.exists() or secret_file_path.stat().st_size < 64
    ) and (
        not secret_file_path.exists() or secret_file_path.stat().st_size < 64
    ):
        with secret_file_path.open('wb') as f:
            f.write(os.urandom(64))
    with secret_file_path.open('rb') as f:
        return f.read()


def load_session():
    if request.method == 'GET':
        d = request.args  # type: ignore

    elif request.method == 'POST':
        d = request.form
    for key in d:
        if '_all' in d.getlist(key):
            session.pop(key, None)
        elif values := [v for v in d.getlist(key) if v]:
            session[key] = values[0] if len(values) == 1 else values
    # Edge cases
    if 'asn' in session:
        session.pop('country', None)
    elif 'country' in session:
        session.pop('asn', None)
    if 'date' not in session:
        session['date'] = (date.today() - timedelta(days=1)).isoformat()


def get_country_codes():
    for c in pycountry.countries:
        yield c.alpha_2, c.name
