#!/usr/bin/python3

import sys

def test(env):
	if len(env)>0:
		print("Test "+env[0]+" successful!")

if __name__ == "__main__":
	test(sys.argv[1:])
	print("Test "+ str(sys.argv[1:])+ " Done")
