#!/usr/bin/env python3
# kaktusas
# by the <tomas # hetmer # net>

import requests
import os.path
import sys
import pickle
import hashlib
import importlib

# konfig
CHECK_URL = "https://www.mujkaktus.cz/chces-pridat"
CHECK_STRING="Pokud si dneska"
MY_PROVIDER="slack_provider"

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def main():

	last_run_file = 'state.pickle'
	notify_needed = False
	check_md5 = 0
	response = None

	if os.path.isfile(last_run_file):
		with open(last_run_file, 'rb') as f:
			data = pickle.load(f)
	else:
		data = {}
		data['old_md5'] = 0

	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
		"Accept-Encoding": "gzip, deflate, br", 
		"Accept-Language": "cs,sk;q=0.8,en-US;q=0.6,en;q=0.4", 
		"Connection": "close", 
		"Dnt": "1", 
		"Host": "www.mujkaktus.cz", 
		"Upgrade-Insecure-Requests": "1", 
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36", 
		"X-Cookiesok": "I explicitly accept all cookies"
	}

	try:
		response = requests.get(CHECK_URL, headers=headers, timeout=30)

		if response.status_code != 200:
			notify_needed = True
			notify_text = 'Request to kaktus returned an error %s, the response is:\n%s' % (response.status_code, response.text)

	except:
		notify_needed = True
		notify_text = "An exception was thrown in requests"


	if response:
		check_ok = False
		for line in response.text.split('class="uppercase text-drawn">'):

			if CHECK_STRING in line:
				m = hashlib.md5()
				m.update(line.encode('utf-8'))
				check_md5 = m.hexdigest()
				check_ok = True
				break


		if check_ok:
			if check_md5 != data['old_md5']:
				notify_needed = True
				notify_text = ':cactus: Kaktusas notify!\nThe text monitored has changed since the last update, please review:\n\n'
				notify_text = notify_text + '*' + remove_html_markup(line.strip()) + '*'
				notify_text = notify_text + '\n\n' + '-> ' + CHECK_URL

		else:
			notify_needed = True
			notify_text = 'Check failed, please revise this script with an updated detection method.'

	if notify_needed:
		notify_provider = importlib.import_module(MY_PROVIDER, package=None)
		notify_provider.alarma(notify_text)


	data['old_md5'] = check_md5

	with open(last_run_file, 'wb') as f:
		pickle.dump(data, f)   

if __name__ == "__main__":
	sys.exit(main())

