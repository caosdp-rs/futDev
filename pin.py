import json
import re
import time
from datetime import datetime
from random import random
import requests


class Pin(object):
    def __init__(self, pidId, personaId, dob, sid, pinUrl):
        self.pinUrl = pinUrl
        self.pidId = pidId
        self.personaId = personaId
        self.dob = dob
        self.sid = sid
        self.s = 1

        self.r = requests.Session()
        self.r.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'accounts.ea.com',
            'Origin': 'https://www.easports.com',
            'Referer': 'https://www.easports.com/fifa/ultimate-team/web-app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        self.r.headers['x-ea-game-id'] = 'FUT20WEB'
        self.r.headers['x-ea-game-id-type'] = 'easku'
        self.r.headers['x-ea-taxv'] = '1.1'

    def ts(self):
        ts = datetime.utcnow()
        ts = ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return ts

    def event(self, en, status=False, pgid=False, source=False, end_reason=False):
        data = {
            'core': {
                's': 1,
                'pidt': 'persona',
                'pid': self.personaId,
                'ts_event': self.ts(),
                'en': en,
                'pidm': {
                    'nucleas': self.pidId
                },
            }
        }
        data['core']['dob'] = self.dob

        if pgid:
            data['pgid'] = pgid
        if status:
            data['status'] = status
        if source:
            data['source'] = source
        if end_reason:
            data['end_reason'] = end_reason

        if en == 'login':
            data['type'] = 'utas'
            data['userid'] = self.personaId
        elif en == 'page_view':
            data['type'] = 'menu'
        elif en == 'error':
            data['server_type'] = 'utas'
            data['errid'] = 'server_error'
            data['type'] = 'disconnect'
            data['sid'] = self.sid

        self.s += 1

        return data

    def send(self, events):
        time.sleep(0.5 + random() / 50)
        data = {
            'custom': {
                'networkAccess': 'G', 'service_plat': 'ps4'
            },
            'et': 'client',
            'events': events,
            'gid': 0,
            'is_sess': True,
            'loc': 'en_US',
            'plat': 'web',
            'rel': 'prod',
            'taxv': '1.1',
            'tid': 'FUT20WEB',
            'tidt': 'easku',
            'ts_post': self.ts(),
            'v': '20.4.2',
            'sid': self.sid
        }
        self.r.options(self.pinUrl)
        rc = self.r.post(self.pinUrl, data=json.dumps(data)).json()
        if rc['status'] != 'ok':
            print('pin event not okay')
            
        return True