#!/usr/bin/env python

import subprocess, smtplib
from collections import namedtuple
from datetime import datetime
from configparser import SafeConfigParser
from email.mime.text import MIMEText

# init a config parser
parser = SafeConfigParser()
# read the config file
parser.read('config.ini')

# get the username and password for the email sender
mail_user = parser.get('email_sender', 'email')
mail_pass = parser.get('email_sender', 'password')
# get a list of all the recipients
recipients = [i for k, i in parser.items('recipients')]

def gmail_login(u, p):
	''' Create a gmail server instance and log in. '''
	# create an SMTP instance
	server = smtplib.SMTP('smtp.gmail.com', 587)
	# say hello
	server.ehlo()
	# start TLS encryption
	server.starttls()
	# say hello again
	server.ehlo()
	# log in to the server
	server.login(u, p)
	# return the server instance
	return server

def create_message(ip, interface, gateway, sender, recipient):
	''' Create an email message using MIME. '''
	# create a mime message with the network information
	message = MIMEText('Your IP address is {0}.\nYou\'re connected using the {1} interface to the router ({2}).\n\n'.format(ip, interface, gateway))
	# get a datetime instance for the current day
	today = datetime.now()
	# define the subject for the email, with the date
	message['Subject'] = 'IP Address for RaspberryPi on {0}'.format(today.strftime('%b-%d-%Y %H:%M:%S'))
	# define who the message is from
	message['From'] = sender
	# define who the message is to
	message['To'] = recipient
	# return the MIME message
	return message

def send_message(server, user, recipient, message):
	''' Send the email to a recipient. '''
	server.sendmail(user, recipient, message.as_string())

def parse_command():
	# the command that will be executed by bash
	command = 'ip route list'
	
	# run the command in bash piping the output back to the child process
	process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
	
	# get the output from the child process
	output = process.communicate()
	
	# split line output up at each space
	words = [i.strip('\n') for i in output[0].decode('utf-8').split(' ') if i]
	
	# enumerate through all the 
	for c, l in enumerate(words):
		if l == 'via':
			# the router IP always follows 'via'
			gateway = words[c + 1]
			# the interface always follows 'dev'
		elif l == 'dev':
			interface = words[c + 1]
		elif l == 'src':
			# the device IP always follows 'src'
			ip_address = words[c + 1]
	
	# check that we have a value for all items
	if gateway and interface and ip_address:
		# named tuple for the network information
		NetInfo = namedtuple('NetInfo', ['gateway', 'interface', 'ip'])
		info = NetInfo(gateway, interface, ip_address)
		return info
	else:
		# this is where we'll deal with any weirdness, not sure how atm.
		pass

# get the network information
net_info = parse_command()
# login to the server
server = gmail_login(mail_user, mail_pass)
# create an empty list for the messages
messages = []
# loop through all the recipients
for r in recipients:
	# create a message for the current recipient
	message = create_message(net_info.ip, net_info.interface, net_info.gateway, mail_user, r)
	# send the message to the current user
	send_message(server, mail_user, r, message)

# shutdown the server
server.quit()




