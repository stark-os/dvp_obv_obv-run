# -------- IMPORTATIONS --------

#std
from std import *






# -------- SEMANTIC --------

#output
OBV__SEP = '\t'






# -------- PARSING --------

#obv
class obvExe:
	def __init__(sbj, ist, args, begBlanks):
		sbj.ist       = ist  #str
		sbj.args      = args #lst[str]
		sbj.begBlanks = begBlanks #str

	def toStr(sbj):
		res = sbj.begBlanks + sbj.ist
		for a in sbj.args:
			res += OBV__SEP + a
		return res



#extract OBV ist & args from line
def obvParse(rawLine):
	commentIdx = str_findFirstChr(rawLine, '#')
	if commentIdx == 0:
		return None #empty line => no exe
	if commentIdx != -1:
		rawLine = str_sub(rawLine, stop=commentIdx-1)

	#strip
	line        = str_stripBeg(rawLine)
	begBlankLen = len(rawLine) - len(line)
	line        = str_stripEnd(line)

	#empty line => no exe
	if len(line) == 0:
		return None

	#args
	args = line.split(OBV__SEP)[1:]
	a = 0
	while a < len(args):
		if len(args[a]) == 0:
			args = lst_remove(args, a)
		else:
			a += 1

	#parse
	ox = obvExe(line[:3], args, rawLine[:begBlankLen])
	obvExe_checkIntegrity(ox)
	return ox



#check args
def mustHaveNArgs(ox, argsNbr):
	if len(ox.args) != argsNbr:
		print("ERROR: Instruction \"" + ox.ist + "\" must have exactly " + str(argsNbr) + " args, got " + str(len(ox.args)) + ".")
		exit(1)

#def argMustBeDatChk(arg):
#	

#def argMustBeReg(arg):
#	

#def argMustBeVal(arg):
#	

def obvExe_checkIntegrity(ox):

	#rsv
	if ox.ist == "rsv":
		mustHaveNArgs(ox, 2)

	#cpy val 2 reg
	elif ox.ist == "v2r":
		mustHaveNArgs(ox, 2)

	#cpy val 2 dat
	elif ox.ist == "v2d":
		mustHaveNArgs(ox, 2)

	#cpy reg 2 reg
	elif ox.ist == "r2r":
		mustHaveNArgs(ox, 2)

	#cpy reg 2 dat
	elif ox.ist == "r2d":
		mustHaveNArgs(ox, 2)

	#cpy dat 2 dat
	elif ox.ist == "d2d":
		mustHaveNArgs(ox, 3)

	#cpy dat 2 reg
	elif ox.ist == "d2r":
		mustHaveNArgs(ox, 2)

	#bck
	elif ox.ist == "bck":
		mustHaveNArgs(ox, 0)

	#ivq
	elif ox.ist == "ivq":
		mustHaveNArgs(ox, 1)

	#fct
	elif ox.ist == "fct":
		mustHaveNArgs(ox, 1)

	#syc
	elif ox.ist == "syc":
		mustHaveNArgs(ox, 0)

	#unknown
	else:
		print("ERROR: Unknown instruction \"" + ox.ist + "\".")
		exit(1)
