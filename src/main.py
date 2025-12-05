#!/usr/bin/python3



# -------- IMPORTATIONS --------

#system
import os, sys
CXD  = os.path.dirname(os.path.realpath(sys.argv[0]))
pCXD = os.path.dirname(CXD)
sys.path.append(CXD)

#obv
from obv     import *
from obv_run import * #in Z, I would LOVE  "obv-run"






# -------- EXECUTION --------

#main
def main():

	#args: filepath
	if len(sys.argv) < 2:
		print("obv-run: Missing arguments (at least 1 required: \"filepath\").")
		exit(1)
	filepath = sys.argv[1]

	#prepare runtime env
	or_ = Obv_Run_init(filepath)

	#run
	while True:
		or_.draw()
		input()
		or_.run()

#run main
main()
