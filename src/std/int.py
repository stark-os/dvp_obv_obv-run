#!/usr/bin/python3



# -------- HEX --------

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
'''
MORE OPTIMIZED Z VERSION
s8 chr.halfHex_toS8(typ) {
	t = typ$s8
	if t >= '0'$s8 && t <= '9'$s8 { ret t - '0'$s8       }
	if t >= 'a'$s8 && t <= 'f'$s8 { ret t - 'a'$s8 + `0a }
	ret `ff
}
'''

def hex_toS8(h1, h0):
	return (chr_halfHex_toS8(h1) << 4) + chr_halfHex_toS8(h0)

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

def str_hex_toS32(s):
	if len(s) != 8:
		print("Hex string \"" + s + "\" must be only 8 characters to be converted into s32.")
		exit(1)
	pow7 = chr_halfHex_toS8(s[0])
	pow6 = chr_halfHex_toS8(s[1])
	pow5 = chr_halfHex_toS8(s[2])
	pow4 = chr_halfHex_toS8(s[3])
	pow3 = chr_halfHex_toS8(s[4])
	pow2 = chr_halfHex_toS8(s[5])
	pow1 = chr_halfHex_toS8(s[6])
	pow0 = chr_halfHex_toS8(s[7])
	if pow0 == -1 or pow1 == -1 \
	or pow2 == -1 or pow3 == -1 \
	or pow4 == -1 or pow5 == -1 \
	or pow6 == -1 or pow7 == -1:
		print("Unconvertible hex string \"" + s + "\" into numerical value.")
		exit(1)
	return \
		pow7 << 28 | pow6 << 24 | \
		pow5 << 20 | pow4 << 16 | \
		pow3 << 12 | pow2 <<  8 | \
		pow1 <<  4 | pow0

def str_hex_toS64(s):
	if len(s) != 16:
		print("Hex string \"" + s + "\" must be only 16 characters to be converted into s64.")
		exit(1)
	powF = chr_halfHex_toS8(s[ 0])
	powE = chr_halfHex_toS8(s[ 1])
	powD = chr_halfHex_toS8(s[ 2])
	powC = chr_halfHex_toS8(s[ 3])
	powB = chr_halfHex_toS8(s[ 4])
	powA = chr_halfHex_toS8(s[ 5])
	pow9 = chr_halfHex_toS8(s[ 6])
	pow8 = chr_halfHex_toS8(s[ 7])
	pow7 = chr_halfHex_toS8(s[ 8])
	pow6 = chr_halfHex_toS8(s[ 9])
	pow5 = chr_halfHex_toS8(s[10])
	pow4 = chr_halfHex_toS8(s[11])
	pow3 = chr_halfHex_toS8(s[12])
	pow2 = chr_halfHex_toS8(s[13])
	pow1 = chr_halfHex_toS8(s[14])
	pow0 = chr_halfHex_toS8(s[15])
	if pow0 == -1 or pow1 == -1 \
	or pow2 == -1 or pow3 == -1 \
	or pow4 == -1 or pow5 == -1 \
	or pow6 == -1 or pow7 == -1 \
	or pow8 == -1 or pow9 == -1 \
	or powA == -1 or powB == -1 \
	or powC == -1 or powD == -1 \
	or powE == -1 or powF == -1:
		print("Unconvertible hex string \"" + s + "\" into numerical value.")
		exit(1)
	return \
		powF << 60 | powE << 56 | \
		powD << 52 | powC << 48 | \
		powB << 44 | powA << 40 | \
		pow9 << 36 | pow8 << 32 | \
		pow7 << 28 | pow6 << 24 | \
		pow5 << 20 | pow4 << 16 | \
		pow3 << 12 | pow2 <<  8 | \
		pow1 <<  4 | pow0






# -------- DECIMAL --------

#conversions
def chr_dec_toS8(c):
	if c == '0':
		return 0
	if c == '1':
		return 1
	if c == '2':
		return 2
	if c == '3':
		return 3
	if c == '4':
		return 4
	if c == '5':
		return 5
	if c == '6':
		return 6
	if c == '7':
		return 7
	if c == '8':
		return 8
	if c == '9':
		return 9
	return -1 #`ff

#signed
MAX_LEN_DEC_S8  =  3 #(2** 7/2).toStr().length
MAX_LEN_DEC_S16 =  5 #(2**15/2).toStr().length
MAX_LEN_DEC_S32 = 10 #(2**31/2).toStr().length
MAX_LEN_DEC_S64 = 19 #(2**63/2).toStr().length

#unsigned
MAX_LEN_DEC_U8  =  3 #(2** 8 -1).toStr().length
MAX_LEN_DEC_U16 =  5 #(2**16 -1).toStr().length
MAX_LEN_DEC_U32 = 10 #(2**32 -1).toStr().length
MAX_LEN_DEC_U64 = 20 #(2**64 -1).toStr().length
def str_dec_toUM(s, sMaxLen, uMaxLen, forbidNegative=False):
	maxLenAllowed = uMaxLen #using unsigned limit by default

	#empty string
	if len(s) == 0:
		print("Empty string cannot be converted into numerical value.")
		exit(1)

	#negativity
	realLength    = len(s)
	negative      = (s[0] == '-')
	if negative:

		#no negation allowed
		if forbidNegative:
			print("Negative number is forbidden here.")
			exit(1)

		#negative => use signed limit instead
		realLength   -= 1
		maxLenAllowed = sMaxLen

	#too long
	if realLength > maxLenAllowed:
		print("Decimal string \"" + s + "\" too big to be converted into numerical value.")
		exit(1)

	#parsing by reading backward
	lastIdx = len(s)-1
	pow     = 1
	result  = 0
	for i in range(realLength):
		d = chr_dec_toS8(s[lastIdx-i])
		if d == -1:
			print("Unconvertible decimal string \"" + s + "\" into numerical value.")
			exit(1)
		result += d * pow
		pow    *= 10

	#apply negativity if any
	if negative:
		result *= -1
	return result

def str_dec_toS8(s):
	return str_dec_toUM(s, MAX_LEN_DEC_S8, MAX_LEN_DEC_U8)

def str_dec_toS16(s):
	return str_dec_toUM(s, MAX_LEN_DEC_S16, MAX_LEN_DEC_U16)

def str_dec_toS32(s):
	return str_dec_toUM(s, MAX_LEN_DEC_S32, MAX_LEN_DEC_U32)

def str_dec_toS64(s):
	return str_dec_toUM(s, MAX_LEN_DEC_S64, MAX_LEN_DEC_U64)

def pad(i, step):
	if i%step != 0:
		i += 1
	return i
