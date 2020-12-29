#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,math
from math import log
from itertools import combinations,permutations,product
'''
=======================MONOGRAMS WITHOUT SPACE=====================================
"о": 0.1078668	"е": 0.0872157	"а": 0.0753882	"и": 0.070338
"н": 0.0666672	"т": 0.0582749	"с": 0.0545604	"л": 0.0490124
"р": 0.0440534	"в": 0.0411654	"к": 0.0369759	"д": 0.0334628
"м": 0.0302632	"у": 0.0294519	"п": 0.0277761	"г": 0.0196232
"ь": 0.0195643	"ы": 0.0193002	"б": 0.0182609	"я": 0.0179398
"з": 0.0153615	"ч": 0.0126616	"ж": 0.0099028	"й": 0.0099028
"х": 0.0088597	"ш": 0.0074138	"ю": 0.0055176	"ц": 0.0033402
"щ": 0.0028177	"ф": 0.0013224	
=========================NON-CROSSING BIGRAMS WITHOUT SPACE========================
"то": 0.0142204	"ст": 0.0129802	"ен": 0.0120949	"не": 0.0118921	"но": 0.0117946	
================ no space ===========================
h1 4.3717133
H2 non-overlapping 4.1296264
'''

from operator import itemgetter

f = open("./16.txt", encoding="utf8")
data = f.read()
my_dict = "абвгдежзийклмнопрстуфхцчшщьыэюя"
common = ['о', 'е', 'а', 'и', 'н', 'т']
bigrammes = ["ст", "но", "то", "на", "ен"]

my_dict_len = len(my_dict)

letter_to_number = {letter: num for num, letter in enumerate(my_dict[:])}
number_to_letter = {num: letter for num, letter in enumerate(my_dict[:])}


def count_entropy(mydict):
    e = 0.0
    p = 0.0

    for i in mydict:
        p = float(mydict[i])
        e += p * log(p,2)
    return float(round(e*-1, 7))


def print_factors(x):
	for i in range(x + 1, 1, -1):
		if x % i == 0:
			if i in range (0,my_dict_len) and int(x/i) in range (0,my_dict_len):
				return [i, int(x/i)]
				break


def clear(data):
	text = ''
	for y in data:
		y = y.lower()
		if y == "ё":
			text += "е"
		if y == "ъ":
			text += "е"
		elif y in my_dict:
			text += y
		else:
			continue
	return text


def count_bigram(x, y):
	global my_dict_len
	return x * my_dict_len + y


def gcd(x, y):
	if y == 0:
		return x
	else:
		return gcd(y, x % y)


def gcdExtended(a, b):
	if a == 0:
		return b, 0, 1
	Gcd, x1, y1 = gcdExtended(b % a, a)
	x = y1 - (b // a) * x1
	y = x1
	return Gcd, x, y


def phi(x):
	counter = 0
	for y in range(1, int(x) + 1):
		if gcd(y, x) == 1:
			counter += 1
	return counter


def reverse(x, m):
	Gcd, a, b = gcdExtended(x, m)
	if Gcd == 1:
		return (a % m + m) % m


def encode(a, b, bigramme):
	global my_dict_len
	return  (a * bigramme + b) % my_dict_len ** 2


def decode(a, b, cyphered_bigramme):
	global my_dict_len
	if a != 0:
		try:
			return (reverse(a, my_dict_len**2) * (cyphered_bigramme - b)) % my_dict_len ** 2
		except TypeError as T:
			1 == 1


def mono_freq(t):
	letter = dict()
	for i in t:
		if i == u'\n':
			continue
		if i in letter:
			letter[i] = float(round(letter.get(i) + 1.0 / len(t), 7))
		else:
			letter[i] = float(round(1.0 / len(t), 7))
	return letter


def noncross_bigrams(t):
	ncbigrm = dict()
	for i in range(0, len(t), 2):
		if t[i] == u' ' and t[i + 1] == u' ':
			continue
		if t[i:i + 2] in ncbigrm:
			ncbigrm[t[i:i + 2]] = float(round(ncbigrm.get(t[i:i + 2]) + 1.0 / len(t) * 2, 7))
		else:
			ncbigrm[t[i:i + 2]] = float(round(1.0 / (len(t) * 2), 7))
	return ncbigrm


def convert_1_bigram(x):
	return count_bigram(letter_to_number.get(x[0]), letter_to_number.get(x[1]))


def linear_comparison(a, b, m):
	Gcd,x,y = gcdExtended(a,m)
	if Gcd > 1:
		if b%Gcd!=0:
			return []
		else:
			res = []
			t0 = m/Gcd
			t1 = reverse(a/Gcd, t0)
			t2 = (t1*b/Gcd)%t0
			res.append(t2)
			for x in range(1,int(Gcd)):
				res.append(int((x*t0+t2)%m))
			return res
	elif Gcd == 1:
		return [reverse(a,m)*b%m]


clear_text = clear(data)
def create_bigrams_list(text):
	text_lst = []
	numb_lst = []
	for x in range(0, len(text), 2):
		text_lst.append(text[x:x+2])
	for a in text_lst:
		numb_lst.append(count_bigram(letter_to_number.get(a[0]), letter_to_number.get(a[1])))
	return numb_lst


def from_number(x):
    return number_to_letter.get(int((x-x%my_dict_len)/my_dict_len))+number_to_letter.get(x%my_dict_len)

cypher_lst = create_bigrams_list(clear_text)
letter1 = mono_freq(clear_text)
bezpbigram1 = noncross_bigrams(clear_text)


k = 1
print (" ")
print ("=======================MONOGRAMS WITHOUT SPACE=====================================")
for key, value in sorted(letter1.items(), key= itemgetter(1), reverse=True):
	if k % 5 != 0:
   		print ("\"%s\": %s" % (key, value),end=" ")
	else:
		print("\"%s\": %s" % (key, value))
	k += 1
k = 1
print (" ")
print ("===========================================================NON-CROSSING BIGRAMS WITHOUT SPACE==================================================================")
for key, value in sorted(bezpbigram1.items(), key= itemgetter(1), reverse=True):
	if k % 10 != 0:
		print("\"%s\": %s" % (key, value), end=" ")
	else:
		print("\"%s\": %s" % (key, value))
	if k == 100:
		break
	k += 1

cypher_lst = []
alt = 0
for key, value in sorted(noncross_bigrams(clear_text).items(), key=itemgetter(1), reverse=True):
	cypher_lst.append(key)
	alt +=1
	if alt == 5:
		break

xb = 0
keys = []

for x in (product(range(5),repeat=4)):
	X_ = convert_1_bigram(bigrammes[x[0]])
	X__ = convert_1_bigram(bigrammes[x[1]])
	Y_ = convert_1_bigram(cypher_lst[x[2]])
	Y__ = convert_1_bigram(cypher_lst[x[3]])
	open_dist = (X_ - X__)
	cypher_dist = (Y_ - Y__)
	if open_dist == 0 or cypher_dist == 0:
		continue
	if open_dist < 0:
		open_dist += my_dict_len**2
	if cypher_dist < 0:
		cypher_dist += my_dict_len**2
	xz = (linear_comparison(open_dist,cypher_dist,my_dict_len**2))
	if xz != [] and xz is not None:
		for xa in xz:
			xb = (Y_-xa*X_)
			while xb < 0:
				xb += my_dict_len**2
			xb=xb% my_dict_len**2
			keys.append([int(xa),xb])

cypher_lst = create_bigrams_list(clear_text)
banned_lst = ["вэ","уы","ыа","зп","йй","хщ","йь","чщ","шщ","чэ","фц"]
banned_bigrams = [convert_1_bigram(a) for a in banned_lst]


result = []
entropies = []
posibble_str = ''
posibble_list = []
posibble_keys = []
for fkey in keys:
	for jkey in cypher_lst:
		lkey = decode(fkey[0],fkey[1],jkey)
		if lkey is not None:
			if lkey in banned_bigrams: # not in allowed_bigrams or lkey
				break
			else:
				posibble_list.append(lkey)
		else:
			break
	if posibble_list != []:
		for gkey in posibble_list:
			posibble_str+=(from_number(gkey))
		final = 0
		k = 0
		for key, value in sorted(noncross_bigrams(posibble_str).items(), key=itemgetter(1), reverse=True):
			if key in bigrammes:
				final += 1
			k += 1
			if final == 2:
				final_ = 0
				k_ = 0
				for key_, value_ in sorted(mono_freq(posibble_str).items(), key=itemgetter(1), reverse=True):
					if key_ in common:
						final_ += 1
					k_ += 1
					if final_ == 3:
						if posibble_str not in result:
							print(fkey)
							posibble_keys.append(fkey)
							result.append(posibble_str)
					if k_ == 5:
						break

			if k == 5:
				break
	posibble_list = []
	posibble_str = ''

print("\n==========================================================================================")

for p in result:
	print(p[:100])


while True:
	pp = int(input("\nwhich text to show? (-1 to exit)\n::\t "))
	if pp == -1:
		break
	else:
		print(posibble_keys[pp], result[pp])
		if input("Print to file this test (yes or no?)") == "yes":
			sys.stdout = open("result.txt", "w")
			for jkey in cypher_lst:
				print(from_number(decode(posibble_keys[pp][0], posibble_keys[pp][1], jkey)), end="")
			sys.stdout.close()
			break