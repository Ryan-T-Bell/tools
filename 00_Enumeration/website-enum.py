#!/usr/bin/python3

import argparse
import os

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-ip", "--ip", help="RHOST: Remote IP of target")
	parser.add_argument("-p", "--ports", help="ports list (csv format: \"80, 443, 8080\")", default="80")
	parser.add_argument("-e", "--extension", help="url extension after FUZZ", default="")
	return parser.parse_args()

def array_builder(ip, ports, extension):
	cmds = []

	for port in ports:

		# File Enumeration
		cmds.append("wfuzz -c -z file,/usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-files.txt --hc 404 {}:{}/FUZZ".format(ip, port))
		
		# Directory Enumeration
		cmds.append("wfuzz -c -z file,/usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-directories.txt --hc 404 {}:{}/FUZZ/".format(ip, port))
		
		# Extensions
		cmds.append("wfuzz -c -z file,/usr/share/wordlists/seclists/Discovery/Web-Content/raft-medium-words.txt --hc 404 {}:{}/FUZZ.{}".format(ip, port, extension))

	return cmds

def system_caller(cmds):
	for cmd in cmds:
		os.system(cmd)

def main():
	args = parse_args()
	ip = args.ip
	ports = args.ports.replace(" ", "").split(",")
	extension = args.extension

	cmds = array_builder(ip, ports, extension)
	system_caller(cmds)

if __name__ == "__main__":
	main()

