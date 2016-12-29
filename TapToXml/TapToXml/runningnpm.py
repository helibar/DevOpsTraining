"""Run npm script_name and Convert tap to xml.

Requirements:

	1. install npm.
	2. Save 4 scripts on PATH:
		TapToXml.py
		tap_parser.py
		xml_creator.py
		runningnpm.py
	
Location:

	runningnpm.py located in PATH.
	
Run this script from:	
	
	runningnpmtest.py should run from the source code folder.
	
Usage:

	python runnpmtest.py <script_name> <xml_file_name.xml>
	Args:
		script_name: The script running npm tests.
		xml_file_name: xml_file_name.xml
	
"""
import sys
import subprocess
import os

def run_test(script_name,xml_file_name):
	"""Run npm task script_name, Convert tap to xml.
	
	"""
	print ("running npm", script_name)
	
	npmrun = "npm run %s > %s" %(script_name,"tap_file")
	process = subprocess.Popen(npmrun, shell=True)
	process.wait()
	os.getenv('PATH')
	cmd = "TapToXml.py %s %s" %("tap_file",xml_file_name)
	process = subprocess.Popen(cmd, shell=True)
	process.wait()
	
def check():
	"""Check npm task script_name failed or pass.
	
		Returns:
			exit code 1: failed.
			exit code 0: pass.
	"""
	is_err_file=os.path.isfile("npm-debug.log")
	if is_err_file:
		return sys.exit(1)
	else:
		return sys.exit(0)
	
	
def main(script_name,xml_file_name):
	run_test(script_name,xml_file_name)
	check()
	
	
if __name__ == '__main__':
	try:   
		main(sys.argv[1],sys.argv[2])
	except IndexError:  
		print ("Usage is: python runnpmtest.py <script_name> <xml_file_name.xml>")
		sys.exit()
	