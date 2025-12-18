import subprocess

#term
def Term__cup(x,y):
	return "\x1b[" + str(y+1) + ';' + str(x+1) + 'H'

def Term__width():
	return int(subprocess.check_output(["tput","cols"])[:-1])

def Term__height():
	return int(subprocess.check_output(["tput","lines"])[:-1])

#meta
Term__CLEAR  = "\x1b[H\x1b[2J\x1b[3J"

#styles
Term__STYLE_RESET = "\x1b(B\x1b[m"
Term__STYLE_BOLD  = "\x1b[1m"
Term__STYLE_BLINK = "\x1b[5m"

#back color
Term__BCOLOR_BLUE   = "\x1b[48;5;20m"
Term__BCOLOR_GRAY   = "\x1b[48;5;245m"
Term__BCOLOR_YELLOW = "\x1b[48;5;226m"
Term__BCOLOR_PURPLE = "\x1b[48;5;93m"
Term__BCOLOR_RED    = "\x1b[48;5;196m"
Term__BCOLOR_ORANGE = "\x1b[48;5;208m"
Term__BCOLOR_GREEN  = "\x1b[48;5;46m"
Term__BCOLOR_LGREEN = "\x1b[48;5;48m"
Term__BCOLOR_LCYAN  = "\x1b[48;5;115m"
Term__BCOLOR_BLACK  = "\x1b[48;5;232m"
Term__BCOLOR_WHITE  = "\x1b[48;5;255m"

#front colors
Term__FCOLOR_BLUE   = "\x1b[38;5;20m"
Term__FCOLOR_GRAY   = "\x1b[38;5;245m"
Term__FCOLOR_YELLOW = "\x1b[38;5;226m"
Term__FCOLOR_PURPLE = "\x1b[38;5;93m"
Term__FCOLOR_RED    = "\x1b[38;5;196m"
Term__FCOLOR_ORANGE = "\x1b[38;5;208m"
Term__FCOLOR_GREEN  = "\x1b[38;5;46m"
Term__FCOLOR_LGREEN = "\x1b[38;5;48m"
Term__FCOLOR_LCYAN  = "\x1b[38;5;115m"
Term__FCOLOR_BLACK  = "\x1b[38;5;232m"
Term__FCOLOR_WHITE  = "\x1b[38;5;255m"

#io
def readFile(filename):
	f = open(filename, "r")
	data = f.read()
	f.close()
	return data

#hexadecimal string representation on fixed amount of digits
def hexOnN(b, N):

	#negativity with python
	if b < 0:
		if N == 2:
			return hexOnN(0x1_00 + b, N)
		elif N == 4:
			return hexOnN(0x1_0000 + b, N)
		elif N == 8:
			return hexOnN(0x1_0000_0000 + b, N)
		elif N == 16:
			return hexOnN(0x1_0000_0000_0000_0000 + b, N)
		print("ERROR IN STD/int.py (invalid number of hex digits for negative output)")
		exit(1)

	#regular execution
	h = hex(b)[2:]
	if len(h) > N:
		print("ERROR IN STD/int.py ["+h+","+str(N)+"]")
		exit(1)
	while len(h) < N:
		h = '0' + h
	return h

#conversions
def chr_halfHex_toS8(h):
	if h == '0':
		return 0
	if h == '1':
		return 1
	if h == '2':
		return 2
	if h == '3':
		return 3
	if h == '4':
		return 4
	if h == '5':
		return 5
	if h == '6':
		return 6
	if h == '7':
		return 7
	if h == '8':
		return 8
	if h == '9':
		return 9
	if h == 'a':
		return 10
	if h == 'b':
		return 11
	if h == 'c':
		return 12
	if h == 'd':
		return 13
	if h == 'e':
		return 14
	if h == 'f':
		return 15
	return -1 #`ff

def str_hex_toS8(s):
	if len(s) != 2:
		print("Hex string \"" + s + "\" must be only 2 characters to be converted into s8.")
		exit(1)
	pow1 = chr_halfHex_toS8(s[0])
	pow0 = chr_halfHex_toS8(s[1])
	if pow0 == -1 or pow1 == -1:
		print("Unconvertible hex string \"" + s + "\" into numerical value.")
		exit(1)
	return pow1 << 4 | pow0

def str_hex_toS16(s):
	if len(s) != 4:
		print("Hex string \"" + s + "\" must be only 4 characters to be converted into s16.")
		exit(1)
	pow3 = chr_halfHex_toS8(s[0])
	pow2 = chr_halfHex_toS8(s[1])
	pow1 = chr_halfHex_toS8(s[2])
	pow0 = chr_halfHex_toS8(s[3])
	if pow0 == -1 or pow1 == -1 \
	or pow2 == -1 or pow3 == -1:
		print("Unconvertible hex string \"" + s + "\" into numerical value.")
		exit(1)
	return \
		pow3 << 12 | pow2 << 8 | \
		pow1 <<  4 | pow0
#!/usr/bin/python3



# -------- IMPORTATIONS --------

#charsets
import string






# -------- TOOLS --------

#hex
HEX_DIGITS_LOWERCASE = string.hexdigits[:-6]

#TO BE ADDED TO STDZ : this is a tiny bit more optimized version of ==(str,str).
#                      We don't compare lengths, assuming that they have been checked before.
#                      By the way, it must be called in ==(str,str) instead.
def str_cmp(s1, s2):
	for c in range(len(s1)):
		if s1[c] != s2[c]:
			return False
	return True

def str_subEqual( #that is tab_subequal in stdz actually
	t, second,
	length      = -1,
	first_from  = 0,
	second_from = 0
):
	if length == -1:
		length = len(t)

	#length constraint
	if (first_from >= len(t)) or (first_from+length > len(t)) or (second_from >= len(second)) or (second_from+length > len(second)):
		return False

	#check equality on specified range
	for c in range(length):
		if second[second_from + c] != t[first_from + c]:
			return False
	return True

def negativeIndexing(idx, length):
	if idx < 0:
		return negativeIndexing(idx+length, length)
	return idx

def str_sub(s, start=None, stop=None):
	l = len(s)
	if l == 0:
		return ""
	if start is None:
		start = 0
	if stop is None:
		stop = l-1
	start = negativeIndexing(start, l)
	stop  = negativeIndexing(stop,  l)
	return s[start:stop+1]

def lst_sub(l, start=None, stop=None):
	length = len(l)
	if length == 0:
		return []
	if start is None:
		start = 0
	if stop is None:
		stop = length-1
	start = negativeIndexing(start, length)
	stop  = negativeIndexing(stop,  length)
	return l[start:stop+1]

def str_isConvertible_int(s):
	if len(s) == 0:
		return False
	positiveS = s
	if s[0] == '-':
		positiveS = s[1:]
	for c in s:
		if c not in string.digits:
			return False
	return True



#strip
def str_getEndStripIndex(t, charset=" \t"):
	endIdx = len(t)-1
	for i in range(len(t)):
		if t[endIdx] not in charset:
			break
		endIdx -= 1
	return endIdx

def str_stripEnd(t, charset=" \t"):
	return str_sub(t, stop=str_getEndStripIndex(t, charset))

def str_getBegStripIndex(t, charset=" \t"):
	startIdx = 0
	for i in range(len(t)):
		if t[startIdx] not in charset:
			break
		startIdx += 1
	return startIdx

def str_stripBeg(t, charset=" \t"):
	return str_sub(t, start=str_getBegStripIndex(t, charset))

def str_strip(t, charset=" \t"):
	return str_stripEnd(str_stripBeg(t, charset), charset)

def str_expandTabs(s, expansionLength):
	result    = ""
	expansion = ' ' * expansionLength
	for c in s:
		if c == '\t':
			result += expansion
		else:
			result += c
	return result

def str_findFirstChr(s, c):
	for i in range(len(s)):
		if s[i] == c:
			return i
	return -1

def str_findLastChr(s, c):
	for i in range(len(s)):
		if s[len(s)-1-i] == c:
			return i
	return -1

def str_insert(s, i, newStr):
	return str_sub(s, stop=i-1) + newStr + str_sub(s, start=i)

def str_truncate(s, start, stop):
	return str_sub(s, stop=start-1) + str_sub(s, start=stop+1)
