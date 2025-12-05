# -------- IMPORTATIONS --------

#obv parser
from std import *
from obv import *






# -------- SETTINGS --------

#sys
ARCH_SIZE      =    8 #in bytes
DEF_STACK_SIZE = 1024 #in bytes
REGISTERS      = {
	"p1":0, "p2":0, "p3":0, "p4":0, #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< later, add sp/sb & every real regs
	"p5":0, "p6":0, "r" :0
}

#display: stack
SPACE_BETWEEN_ADR_AND_ROW = 2
SPACE_BETWEEN_COLM        = 6
ADR_ON_HEX_DIGITS         = 4
COLM_LEN                  = 2 + ADR_ON_HEX_DIGITS + SPACE_BETWEEN_ADR_AND_ROW + (2*ARCH_SIZE) #1 for '@', 1 for mid-colm blank
CHK_COLORS = (
	Term__FCOLOR_BLACK + Term__BCOLOR_PURPLE,
	Term__FCOLOR_BLACK + Term__BCOLOR_YELLOW,
	Term__FCOLOR_BLACK + Term__BCOLOR_LCYAN,
	Term__FCOLOR_WHITE + Term__BCOLOR_RED,
	Term__FCOLOR_BLACK + Term__BCOLOR_GREEN,
	Term__FCOLOR_BLACK + Term__BCOLOR_BLUE,
	Term__FCOLOR_WHITE + Term__BCOLOR_ORANGE,
	Term__FCOLOR_BLACK + Term__BCOLOR_LGREEN
)

#display: sep
SEP_LINE_PADDING = 2
SEP_LINE_1_X     = 60
SEP_LINE_2_INV_X = 40 #real X will be width-X






# -------- OBV DAT ITM --------

#dat itm
class obvDI:
	def __init__(sbj, name, adr, color, size):
		sbj.name  = name
		sbj.adr   = adr
		sbj.color = color
		sbj.size  = size

	def containsAdr(sbj, adr):
		return adr <= sbj.adr and adr > sbj.adr-sbj.size

#gbl compare di between stack frames
class di_sfi:
	def __init__(sbj, di, sfi):
		sbj.di  = di
		sbj.sfi = sfi #stack frame idx






# -------- OBV RUN INIT --------

#init
def Obv_Run_init(filename):
	oxes   = [] #lst[obvExe]
	fctMap = {} #map[str,idx]

	#parse obv file
	for l in readFile(filename).split('\n'):
		ox = obvParse(l)
		if ox is None:
			continue

		#fct => keep cur idx for potential ivq
		if ox.ist == "fct":
			fn = ox.args[0]
			if fn in fctMap.keys():
				print("Already got a \"fct\" instruction with the given name \"" + fn + "\".")
				exit(1)
			fctMap[fn] = len(oxes)

		#store ox
		oxes.append(ox)

	#res
	return obvRun(oxes, fctMap)

class obvRun:
	def __init__(sbj, oxes, fctMap, stackSz=DEF_STACK_SIZE):

		#concrete
		sbj.stack    = [0] * stackSz
		sbj.stackIdx = stackSz-1 #start at adr max, dsc order
		sbj.regs     = REGISTERS
		sbj.exeIdx   = 0

		#abstract
		sbj.oxes        = oxes #lst[obvExe]
		sbj.fctMap      = fctMap
		sbj.stackFrames = [{}] #lst[map[str,obvDI]]

		#display
		sbj.width       = Term__width()
		sbj.height      = Term__height()
		sbj.midH        = int(sbj.height/2)-1
		sbj.rowPerColm  = sbj.height-1
		sbj.curChkColor = 0

		#special case: starting on "fct" => nxt
		if len(sbj.oxes) != 0 and sbj.oxes[0].ist == "fct":
			sbj.inc()



	#inc
	def inc(sbj):
		sbj.exeIdx += 1

		#end of prg
		if sbj.exeIdx == len(sbj.oxes):
			print("END OF PROGRAM EXECUTION")
			exit(0)






	# -------- DISPLAY --------

	#coloration
	def pickChkColor(sbj):
		res = CHK_COLORS[sbj.curChkColor]
		sbj.curChkColor += 1
		if sbj.curChkColor == len(CHK_COLORS):
			sbj.curChkColor = 0
		return res

	def draw(sbj):

		#clear screen
		output = Term__CLEAR + Term__STYLE_RESET



		# IST PANNEL, LEFT SIDE

		#blanks before code
		if sbj.exeIdx < sbj.midH:
			exesBefore = sbj.exeIdx
			output    += '\n' * (sbj.midH - exesBefore)
		else:
			exesBefore = sbj.midH

		#code before cur idx
		for i in range(exesBefore,0,-1):
			output += "  " + sbj.oxes[sbj.exeIdx-i].toStr() + '\n'

		#cur ist
		output += "> " + sbj.oxes[sbj.exeIdx].toStr() + '\n'

		#code after cur idx
		exesAfter = len(sbj.oxes) - sbj.exeIdx -1
		if exesAfter > sbj.midH:
			exesAfter = sbj.midH
		for i in range(exesAfter):
			output += "  " + sbj.oxes[sbj.exeIdx+i+1].toStr() + '\n'

		#blanks after code
		output += '\n' * (sbj.midH - exesAfter)

		#sep line
		for h in range(sbj.height):
			output += Term__cup(SEP_LINE_1_X, h) + '|'



		# STACK COLMS, AFTER LEFT SIDE

		#as long as we have mem chk to draw
		width = SEP_LINE_1_X + SEP_LINE_PADDING
		adr   = 0
		while adr < len(sbj.stack):

			#new colm
			height = -1
			for i in range(sbj.rowPerColm * ARCH_SIZE):

				#new line
				if i%ARCH_SIZE == 0:
					height += 1
					output += Term__cup(width, height) + Term__STYLE_RESET + '@' + hexOnN(adr, ADR_ON_HEX_DIGITS) + ' '*SPACE_BETWEEN_ADR_AND_ROW

				#reset in all cases
				output += Term__STYLE_RESET
				if adr%(ARCH_SIZE/2) == 0:
					output += ' '

				#look for datItm on this byte (in all cases)
				DISFIFound = None #di_sf
				for sfi in range(len(sbj.stackFrames)):
					for di in sbj.stackFrames[sfi].values():
						if di.containsAdr(adr):
							if DISFIFound is not None:
								print("ERROR: Found at least 2 datItm sharing the same byte @" + hexOnN(adr, ADR_ON_HEX_DIGITS))
								print("       \"" + di.name + "\"[StackFrame" + str(sfi) + "] and")
								print("       \"" + DISFIFound.di.name + "\"[StackFrame" + str(DISFIFound.sfi) + "].")
							DISFIFound = di_sfi(di, sfi)
							output    += di.color

				#current stack idx: blink
				if adr == sbj.stackIdx:
					output += Term__STYLE_BLINK

				#draw single byte
				output += hexOnN(sbj.stack[adr], 2)
				adr += 1

				#ended inside colm
				if adr >= len(sbj.stack):
					break

			#shift nxt colm
			width += SPACE_BETWEEN_COLM + COLM_LEN

		#reset at end of stack colm draw
		output += Term__STYLE_RESET



		# REGISTERS & DAT ITMS, RIGHT SIDE

		#sep line
		rightSideWidth = SEP_LINE_2_INV_X + SEP_LINE_PADDING
		for h in range(sbj.height):
			output += Term__cup(sbj.width - rightSideWidth, h) + '|'

		#split right side in 2 colms
		rightSideX_col1 = sbj.width - SEP_LINE_2_INV_X
		rightSideX_col2 = sbj.width - int(rightSideWidth/2) + SEP_LINE_PADDING

		#regs
		output  += Term__cup(rightSideX_col1, 0) + "[REGISTERS]"
		height   = 2
		reg_keys = list(sbj.regs.keys())
		for k in range(len(reg_keys)):

			#on 2 colms
			if k&1 == 0:
				output += Term__cup(rightSideX_col1, height)
			else:
				output += Term__cup(rightSideX_col2, height)
				height += 1

			#reg
			key     = reg_keys[k]
			output += '\"' + key + "\" " + hexOnN(sbj.regs[key], ARCH_SIZE)
		height += 1

		#stack frames
		width = rightSideX_col1
		for sf in range(len(sbj.stackFrames)):
			height += 1
			output += Term__cup(width, height) + "[StackFrame" + str(sf) + ']'
			height += 1

			#datItms
			height1       = height
			height2       = height
			curStackFrame = sbj.stackFrames[sf]
			di_keys       = list(curStackFrame.keys())
			for k in range(len(di_keys)):
				di = curStackFrame[di_keys[k]]
				output += Term__cup(width, height) + di.color + '\"' + di.name + "\" (" + hexOnN(di.size, 4) + " B)" + Term__STYLE_RESET
				height += 1

				#switching colm
				if k&1 == 0:
					height1 = height
					height  = height2
					width   = rightSideX_col2
				else:
					height2 = height
					width   = rightSideX_col1

		#draw
		print(output, end="")






	# -------- RUN --------

	#run cur ist + inc to nxt one
	def run(sbj):
		ox = sbj.oxes[sbj.exeIdx]

		#rsv
		if ox.ist == "rsv":
			n  = ox.args[0]
			sz = str_hex_toS16(ox.args[1])

			#check already dcl in cur stack frame
			lastStackFrame = sbj.stackFrames[-1]
			if n in lastStackFrame.keys():
				print("Reserving data with name \"" + n + "\" but it is already taken.")
				exit(1)

			#dcl in cur stack frame
			lastStackFrame[n] = obvDI(n, sbj.stackIdx, sbj.pickChkColor(), sz)
			sbj.stackIdx     -= sz

		#cpy val 2 reg
		elif ox.ist == "v2r":
			pass

		#cpy val 2 dat
		elif ox.ist == "v2d":
			pass

		#cpy reg 2 reg
		elif ox.ist == "r2r":
			pass

		#cpy reg 2 dat
		elif ox.ist == "r2d":
			pass

		#cpy dat 2 dat
		elif ox.ist == "d2d":
			pass

		#cpy dat 2 reg
		elif ox.ist == "d2r":
			pass

		#bck
		elif ox.ist == "bck":
			pass

		#ivq
		elif ox.ist == "ivq":
			sbj.exeIdx = sbj.fctMap[ox.args[0]] -1 #-1 will be compensated by end-of-ist inc()

		#fct
		elif ox.ist == "fct":
			sbj.inc()
			sbj.run() #no exe for this ist => run directly the nxt one
			return

		#bck
		elif ox.ist == "syc":
			pass

		#inc
		sbj.inc()
