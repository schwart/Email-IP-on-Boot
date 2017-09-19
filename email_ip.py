#!/usr/bin/env python

import subprocess

# the command that will be executed by bash
command = 'ip route list'

# run the command in bash piping the output back to the child process
process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)

# get the output from the child process
output = process.communicate()

# split line output up at each space
words = [i.strip() for i in output[0].split(' ') if i]

# enumerate through all the 
for c, l in enumerate(words):
	if l == 'via':
		# the router IP always follows 'via'
		router_ip = words[c + 1]
		# the interface always follows 'dev'
	elif l == 'dev':
		interface = words[c + 1]
	elif l == 'src':
		# the device IP always follows 'src'
		ip_address = words[c + 1]

if router_ip and interface and ip_address:
	print('Router IP: {0}\nInterface: {1}\nIP Address: {2}'.format(router_ip, interface, ip_address))
