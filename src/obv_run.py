# -------- IMPORTATIONS --------

#system
import os, sys
CXD  = os.path.dirname(os.path.realpath(sys.argv[0]))
pCXD = os.path.dirname(CXD)
sys.path.append(CXD)

#input
import subprocess

#obv parser
from std.std import *
from obv.src.exe import *
from obv.src.seg import *






# -------- TOOLS -------- <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PYTHONIC

#input keys
KEY__ARROW_LEFT  = b'[D'
KEY__ARROW_RIGHT = b'[C'
KEY__ARROW_UP    = b'[A'
KEY__ARROW_DOWN  = b'[B'
KEY__PAGE_UP     = b'[5'
KEY__PAGE_DOWN   = b'[6'
KEY__ENTER       = b''

#input without ENTER
def getByte():
	return subprocess.check_output([pCXD + "/src/getChr"])

def getChr():
	c = getByte()
	if c == b'\x1b':
		c =  getByte()
		c += getByte()
	return c






# -------- SETTINGS --------

#sys
ARCH_SIZE = 8 #in bytes
REGS      = {
	"p1":0, "p2":0, "p3":0, "p4":0, #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< later, add sp/sb & every real regs
	"p5":0, "p6":0, "r" :0
}
SEG_NAMES = ("DATA", "HEAP", "STACK")
SEG_SIZES = [     0,   1024,    1024] #in bytes, "DATA" size will be set at init

#display: spacing
SPACE_BETWEEN_COLM = 3 #6

#display: seg colms
ADR_ON_HEX_DIGITS = 4
COLM_LEN          = 3 + ADR_ON_HEX_DIGITS + (2*ARCH_SIZE) #1 for '@', 1 for space between adr & colm, 1 for mid-colm blank
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

#display: dynamic
UPDATE_DIMENSIONS_ON_KEYPRESS = True

#display: pannels
LEFT_PANNEL_WIDTH_RATIO_X  = 0.25
RIGHT_PANNEL_WIDTH_RATIO_X = 0.75






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
	fctMap = {} #map[str,idx]
	oxes   = [] #lst[obvExe]

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
	def __init__(sbj, oxes, fctMap):

		#dat seg spc
		sbj.datSegIdx     = sbj.getSegIdxByName("DATA")
		sbj.lastDatLclAdr = 0

		#compute dat seg sz
		datSegSz = 0
		for ox in oxes:
			if ox.ist == "dat":
				datSegSz += ox.sz >> 3
		SEG_SIZES[sbj.datSegIdx] = datSegSz

		#segs
		sbj.segFocus          = 0
		sbj.segs              = []
		prevSeg_lastGblAdr    = -1
		for s in range(len(SEG_NAMES)):

			#create & add seg
			curSeg = seg(SEG_NAMES[s], prevSeg_lastGblAdr+1, SEG_SIZES[s])
			sbj.segs.append(curSeg)
			prevSeg_lastGblAdr = curSeg.lastGblAdr

		#init lineShifts & max
		sbj.segs_lineShift    = [0] * len(SEG_NAMES)
		sbj.segs_maxLineShift = [0] * len(SEG_NAMES)

		#display
		sbj.width            = 0
		sbj.height           = 0
		sbj.midH             = 0
		sbj.curChkColor      = 0
		sbj.rowPerColm       = 0
		sbj.leftPannel_maxX  = 0
		sbj.rightPannel_minX = 0
		sbj.updateDimensions() #=> also update lineShifts

		#CPU ctx
		sbj.regs   = REGS
		sbj.prgCnt = 0

		#stack spc
		s                     = sbj.getSegIdxByName("STACK")
		sbj.stackPtr          = sbj.segs[s].lastGblAdr   #set stackPtr, start at adr max, dsc order
		sbj.segs_lineShift[s] = sbj.segs_maxLineShift[s] #set default view at end of stack (more interesting)

		#abstract
		sbj.oxes        = oxes #lst[obvExe]
		sbj.fctMap      = fctMap
		sbj.stackFrames = [{}] #lst[map[str,obvDI]]

		#start at main fct
		'''while True:
			ox = sbj.oxes[0]

			#no main fct found before end of exe
			if sbj.prgCnt == len(sbj.oxes):
				print("ERROR: No main function found to run.")
				exit(1)

			#main fct found => start here
			if ox.ist == "fct" and ox.ist:
				sbj.prgCnt += 1
				break

			#inc
			sbj.prgCnt += 1'''



	#seg tools
	def getSegIdxByName(sbj, segName):
		for s in range(len(SEG_NAMES)):
			if SEG_NAMES[s] == segName:
				return s
		return -1



	#inc
	def inc(sbj):
		sbj.prgCnt += 1

		#end of prg
		if sbj.prgCnt == len(sbj.oxes):
			print("END OF PROGRAM EXECUTION")
			exit(0)






	# -------- EXECUTION --------

	#lineshifts
	def lineShiftIcr(sbj):
		if sbj.segs_lineShift[sbj.segFocus] != sbj.segs_maxLineShift[sbj.segFocus]:
			sbj.segs_lineShift[sbj.segFocus] += 1

	def lineShiftDcr(sbj):
		if sbj.segs_lineShift[sbj.segFocus] != 0:
			sbj.segs_lineShift[sbj.segFocus] -= 1

	#main
	def mainLoop(sbj):
		while True:
			if UPDATE_DIMENSIONS_ON_KEYPRESS:
				sbj.updateDimensions()
			sbj.draw()
			k = getChr()

			#change seg focus
			if k == KEY__ARROW_LEFT:
				if sbj.segFocus != 0:
					sbj.segFocus -= 1
			elif k == KEY__ARROW_RIGHT:
				if sbj.segFocus != len(SEG_NAMES)-1:
					sbj.segFocus += 1

			#change cur seg lineShift, precision
			elif k == KEY__ARROW_UP:
				sbj.lineShiftDcr()
			elif k == KEY__ARROW_DOWN:
				sbj.lineShiftIcr()

			#change cur seg lineShift, whole colm
			elif k == KEY__PAGE_UP:
				for l in range(sbj.rowPerColm):
					sbj.lineShiftDcr()
			elif k == KEY__PAGE_DOWN:
				for l in range(sbj.rowPerColm):
					sbj.lineShiftIcr()

			#ENTER => run nxt ist
			elif k == KEY__ENTER:
				sbj.run()






	# -------- DISPLAY --------

	#dynamic resize
	def updateLineShifts(sbj):
		for s in range(len(SEG_NAMES)):

			#re-compute max lineShift
			maxLineShift = 0
			segLineNbr   = int(SEG_SIZES[s]/ARCH_SIZE)
			if segLineNbr > sbj.rowPerColm:
				maxLineShift = segLineNbr - sbj.rowPerColm

			#update max lineShift
			sbj.segs_maxLineShift[s] = maxLineShift

			#if necessary, reset lineShift in its new range
			if sbj.segs_lineShift[s] > maxLineShift:
				sbj.segs_lineShift[s] = maxLineShift

	def updateDimensions(sbj):

		#display: general
		sbj.width  = Term__width()
		sbj.height = Term__height()
		sbj.midH   = int(sbj.height/2)-1

		#display: segments
		sbj.rowPerColm  = sbj.height-5 #seg name, space, "..." on top & bottom

		#display: pannels
		sbj.leftPannel_maxX  = int(sbj.width *  LEFT_PANNEL_WIDTH_RATIO_X)
		sbj.rightPannel_minX = int(sbj.width * RIGHT_PANNEL_WIDTH_RATIO_X)

		#update lineShifts also
		sbj.updateLineShifts()



	#coloration
	def pickChkColor(sbj):
		res = CHK_COLORS[sbj.curChkColor]
		sbj.curChkColor += 1
		if sbj.curChkColor == len(CHK_COLORS):
			sbj.curChkColor = 0
		return res



	#generic draw
	def drawVertLine(sbj, width):
		output = ""
		for h in range(sbj.height):
			output += Term__cup(width, h) + '|'
		return output



	#specific draw: ist pannel
	def drawIstPannel(sbj):
		output   = ""
		ist_maxX = sbj.leftPannel_maxX - 2 #ist starts 2 chr from the left

		#blanks before code
		if sbj.prgCnt < sbj.midH:
			exesBefore = sbj.prgCnt
			output    += '\n' * (sbj.midH - exesBefore)
		else:
			exesBefore = sbj.midH

		#code before cur idx
		for i in range(exesBefore,0,-1):
			output += "  " + str_sub(
				sbj.oxes[sbj.prgCnt-i].unparse().replace('\t', ' '),
				stop=ist_maxX
			) + '\n'

		#cur ist
		output += "> " + str_sub(
			sbj.oxes[sbj.prgCnt].unparse().replace('\t', ' '),
			stop=ist_maxX
		) + '\n'

		#code after cur idx
		exesAfter = len(sbj.oxes) - sbj.prgCnt -1
		if exesAfter > sbj.midH:
			exesAfter = sbj.midH
		for i in range(exesAfter):
			output += "  " + str_sub(
				sbj.oxes[sbj.prgCnt+i+1].unparse().replace('\t', ' '),
				stop=ist_maxX
			) + '\n'

		#blanks after code
		return output + '\n' * (sbj.midH - exesAfter)



	#specific draw: seg dump
	def drawSeg(sbj, seg, x, skipBegLines, inBold):
		haveRemainingBytes  = True
		etcDotsSpacingBlank = 3 + ADR_ON_HEX_DIGITS

		#display in bold style
		boldStyle = ""
		if inBold:
			boldStyle = Term__STYLE_BOLD

		#seg name
		output = Term__cup(x,0) + Term__STYLE_RESET + boldStyle + ' '*etcDotsSpacingBlank + seg.name

		#"..." at the top
		if skipBegLines != 0:
			output += Term__cup(x,2) + boldStyle + ' '*etcDotsSpacingBlank + "..."

		#draw byte per byte, on whole dedicated height
		lclAdr = int(ARCH_SIZE * skipBegLines)
		gblAdr = seg.firstGblAdr + lclAdr
		y      = 1
		for i in range(sbj.rowPerColm * ARCH_SIZE):

			#new line
			if i%ARCH_SIZE == 0:
				y += 1
				output += Term__cup(x,y) + Term__STYLE_RESET + boldStyle + '@' + hexOnN(gblAdr, ADR_ON_HEX_DIGITS)

			#reset style in all cases
			output += Term__STYLE_RESET + boldStyle
			if lclAdr%(ARCH_SIZE>>1) == 0:
				output += ' '

			#coloration: can be the location of a datItm => look in every stack frame, if an adr matches
			DISFIFound = None #di_sf
			for sfi in range(len(sbj.stackFrames)):
				for di in sbj.stackFrames[sfi].values():

					#datItm is contained in that region
					if di.containsAdr(gblAdr):
						if DISFIFound is not None:
							print("ERROR: Found at least 2 datItm sharing the same byte @" + hexOnN(gblAdr, ADR_ON_HEX_DIGITS))
							print("       \"" + di.name + "\"[StackFrame" + str(sfi) + "] and")
							print("       \"" + DISFIFound.di.name + "\"[StackFrame" + str(DISFIFound.sfi) + "].")
							exit(1)
						DISFIFound = di_sfi(di, sfi)
						output    += di.color

			#blink: stack ptr
			if gblAdr == sbj.stackPtr:
				output += Term__STYLE_BLINK

			#draw single byte
			output += hexOnN(seg.dat[lclAdr], 2)

			#nxt byte
			lclAdr += 1
			gblAdr += 1

			#not enough bytes to fulfill colm => stop here
			if lclAdr > seg.lastLclAdr:
				haveRemainingBytes = False
				break

		#"..." at the bottom
		if haveRemainingBytes:
			output += Term__cup(x,y+1) + Term__STYLE_RESET + boldStyle + ' '*etcDotsSpacingBlank + "..."

		#reset at end of colm draw
		return output + Term__STYLE_RESET



	#specific draw: regs
	def drawRegs(sbj, col1X, col2X, y):
		output   = Term__cup(col1X,0) + "[REGISTERS]"

		#max X get over
		col1_maxX = col2X-1
		col2_maxX = sbj.width

		#regs
		y       += 2
		maxX     = col1_maxX
		reg_keys = list(sbj.regs.keys())
		for k in range(len(reg_keys)):

			#on 2 colms
			if k&1 == 0:
				x    = col1X
				maxX = col1_maxX
			else:
				x    = col2X
				maxX = col2_maxX
				y += 1

			#reg
			key    = reg_keys[k]
			regTxt = key + ' ' + hexOnN(sbj.regs[key], ARCH_SIZE)

			#draw with potential cut at the end if doesn't fit
			output += Term__cup(x,y) + str_sub(regTxt, stop=(maxX - x-1))

		#height is useful for displaying further things under
		return (output,y+1)



	#specific draw: stack frames
	def drawStackFrames(sbj, col1X, col2X, y):
		output = ""

		#max X get over
		col1_maxX = col2X-1
		col2_maxX = sbj.width

		#stack frames
		x    = col1X
		maxX = col1_maxX
		for sf in range(len(sbj.stackFrames)):
			y += 1
			output += Term__cup(x,y) + "[StackFrame" + str(sf) + ']'
			y += 1

			#both colms will progress at their own speed
			y1 = y
			y2 = y

			#datItms
			curStackFrame = sbj.stackFrames[sf]
			di_keys       = list(curStackFrame.keys())
			for k in range(len(di_keys)):
				di = curStackFrame[di_keys[k]]
				diTxt = di.name + '/' + hexOnN(di.size, 4)
				output += Term__cup(x,y) + di.color + str_sub(diTxt, stop=(maxX - x-1)) + Term__STYLE_RESET
				y += 1

				#switching colm
				if k&1 == 0:
					y1   = y
					y    = y2
					x    = col2X
					maxX = col2_maxX
				else:
					y2   = y
					x    = col1X
					maxX = col1_maxX

		#y is useful for displaying further things under
		return (output,y)



	#main draw
	def draw(sbj):

		#clear screen
		output = Term__CLEAR + Term__STYLE_RESET

		#ist
		output += sbj.drawIstPannel()

		#sep line
		output += sbj.drawVertLine(sbj.leftPannel_maxX)

		#check whether we have enough place to displat at least one seg
		minX = sbj.leftPannel_maxX + 1
		maxX = minX + SPACE_BETWEEN_COLM + COLM_LEN
		if maxX >= sbj.rightPannel_minX:
			return

		#prepare segs maxX as we were drawing all of them
		segs_maxX = []
		for s in range(len(sbj.segs)):
			segs_maxX.append(maxX)
			maxX += SPACE_BETWEEN_COLM + COLM_LEN

		#as long as focused seg is not visible, rm the first seg from display
		segsToDraw = len(sbj.segs) #first, considering drawing all segs
		segOffset  = 0             #nbr or seg to skip drawing
		while segs_maxX[sbj.segFocus - segOffset] > sbj.rightPannel_minX:
			segOffset  += 1
			segsToDraw -= 1
			if segOffset > sbj.segFocus: #too small => no seg to draw finally
				break

		#tricky trick: adding minX as 1st elm makes it a minX lst => can be used for display then!
		segs_maxX = [minX] + segs_maxX

		#draw concerned segs until they no longer fit in display
		for s in range(segsToDraw):
			if segs_maxX[s+1] >= sbj.rightPannel_minX:
				break

			#still fitting => draw
			segIdx  = segOffset + s
			output += sbj.drawSeg(
				sbj.segs[segIdx],
				segs_maxX[s],
				sbj.segs_lineShift[segIdx],
				segIdx == sbj.segFocus
			)

		#sep line
		output += sbj.drawVertLine(sbj.rightPannel_minX)

		#next displays will be split in 2 colms
		secondColmX = (sbj.width + sbj.rightPannel_minX)>>1

		#regs
		o,y = sbj.drawRegs(sbj.rightPannel_minX+1, secondColmX, 0)
		output += o

		#stack frames right under
		o,y = sbj.drawStackFrames(sbj.rightPannel_minX+1, secondColmX, y)
		output += o

		#draw
		print(output, end="")






	# -------- RUN --------

	#run cur ist + inc to nxt one
	def run(sbj):
		ox = sbj.oxes[sbj.prgCnt]



		#MEM

		#dat
		if ox.ist == "dat":
			lit       = ox.args[0]
			datSegDat = sbj.segs[sbj.datSegIdx].dat
			for i in range(len(lit)>>1):
				d = i<<1
				datSegDat[sbj.lastDatLclAdr] = hex_toS8(lit[d], lit[d+1])
				sbj.lastDatLclAdr += 1

		#rsv
		elif ox.ist == "rsv":
			n  = ox.args[0]
			sz = str_hex_toS16(ox.args[1])

			#check already dcl in cur stack frame
			lastStackFrame = sbj.stackFrames[-1]
			if n in lastStackFrame.keys():
				print("Reserving data with name \"" + n + "\" but it is already taken.")
				exit(1)

			#dcl in cur stack frame
			lastStackFrame[n] = obvDI(n, sbj.stackPtr, sbj.pickChkColor(), sz)
			sbj.stackPtr     -= sz



		#CPY FROM VAL INTO ...

		#cpy val 2 reg
		elif ox.ist == "v2r":
			pass

		#cpy val 2 dat
		elif ox.ist == "v2d":
			pass

		#cpy val 2 at-adr
		elif ox.ist == "v2a":
			pass



		#CPY FROM REG INTO ...

		#cpy reg 2 reg
		elif ox.ist == "r2r":
			pass

		#cpy reg 2 dat
		elif ox.ist == "r2d":
			pass

		#cpy reg 2 at-adr
		elif ox.ist == "r2a":
			pass



		#CPT FROM DAT INTO ...

		#cpy dat 2 reg
		elif ox.ist == "d2r":
			pass

		#cpy dat 2 dat
		elif ox.ist == "d2d":
			pass

		#cpy dat 2 at-adr
		elif ox.ist == "d2a":
			pass



		#CPY FROM PTR INTO ...

		#cpy at-adr 2 reg
		elif ox.ist == "a2r":
			pass

		#cpy at-adr 2 dat
		elif ox.ist == "a2d":
			pass

		#cpy at-adr 2 at-adr
		elif ox.ist == "a2a":
			pass



		#DECISIONAL

		#dor
		elif ox.ist == "dor":
			pass

		#dan
		elif ox.ist == "dan":
			pass



		#ATH

		#bad
		elif ox.ist == "bad":
			pass

		#bsu
		elif ox.ist == "bsu":
			pass

		#amu
		elif ox.ist == "amu":
			pass

		#adi
		elif ox.ist == "adi":
			pass

		#amo
		elif ox.ist == "amo":
			pass



		#LOGIC

		#sin
		elif ox.ist == "sin":
			pass

		#lor
		elif ox.ist == "lor":
			pass

		#lan
		elif ox.ist == "lan":
			pass

		#lxo
		elif ox.ist == "lxo":
			pass

		#lls
		elif ox.ist == "lls":
			pass

		#lrs
		elif ox.ist == "lrs":
			pass



		#CMP

		#sno
		elif ox.ist == "sno":
			pass

		#ceq
		elif ox.ist == "ceq":
			pass

		#cne
		elif ox.ist == "cne":
			pass

		#clt
		elif ox.ist == "clt":
			pass

		#cgt
		elif ox.ist == "cgt":
			pass

		#cle
		elif ox.ist == "cle":
			pass

		#cge
		elif ox.ist == "cge":
			pass

		#cmp
		elif ox.ist == "CMP":
			pass



		#FCT RELATED

		#bck
		elif ox.ist == "bck":
			pass

		#ivq
		elif ox.ist == "ivq":
			sbj.prgCnt = sbj.fctMap[ox.args[0]] -1 #-1 will be compensated by end-of-ist inc()

		#fct
		elif ox.ist == "fct":
			sbj.inc()
			sbj.run() #no exe for this ist => run directly the nxt one
			return



		#SYSTEM

		#syc
		elif ox.ist == "syc":
			pass

		#inc
		sbj.inc()
