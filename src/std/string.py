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
