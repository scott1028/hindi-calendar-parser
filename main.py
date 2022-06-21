#!/usr/bin/env python3
# coding: utf

import re
import urllib
from urllib import request as urllib2
import http.cookiejar
import random
from datetime import datetime
import json

CJ = http.cookiejar.CookieJar()
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CJ))

def main(year = '2022' or '2021', langs = ['en', 'hi']):
    output = []
    for lang in langs:
        version = str(int(random.random() * 10 + 70))
        req = urllib.request.Request(
            f'https://timesles.com/{lang}/holidays/years/{year}/india-95/',
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s.0.1916.47 Safari/537.36' % version
            }
        )
        fd = OPENER.open(req, timeout=7)
        buf = fd.read()
        target_area = re.compile(r'<div class=h-table>(?P<area>.*?)<br>', re.DOTALL)
        match_content = target_area.search(buf.decode('utf-8')).group('area')
        festivals = re.findall(r'<div class=h-table-td-first>(?P<date_string>.*?)</div><div class=h-table-td><a href=".*?">(?P<label>.*?)</a></div><div class=h-table-td>(?P<date_type>.*?)</div><div class=h-table-td>.*?</div></div>', match_content)
        for idx, row in enumerate(festivals):
            if lang == 'en':
                date = datetime.strptime(row[0], "%b %d, %Y").strftime("%Y-%m-%d")
                label = row[1]
                output.append({
                    'date': date,
                    f'label_{lang}': label,
                })
            else:
                output[idx][f'label_{lang}'] = row[1]
        json_data = json.dumps(output, indent=4)
    with open(f'dist/output-{year}.json', 'w') as fd:
        fd.write(json_data)

if __name__ == "__main__":
    year = input('year(ex: 2022, 2021, ...)?')
    main(year)
