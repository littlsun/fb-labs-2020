#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter, attrgetter

from math import log

f = open("C:\\Users\\Natalia\\Desktop\\text.txt",  encoding="utf8")
f1 = open("C:\\Users\\Natalia\\Desktop\\text1.txt",  encoding="utf8")
text = f.read()
text1 = f1.read()


def mono_freq(t):
    letter = dict()
    for i in t:
        i = i.lower()
        if i == u'\n':
            continue
        if i in letter:
            letter[i] = float(round(letter.get(i) + 1.0/len(t), 6))
        else:
            letter[i] = float(round(1.0/len(t), 6))
    return letter

def cross_bigrams(t):
    bigram = dict()
    t = t.lower()
    for i in range(len(t)):
        if t[i:i+2] in bigram:
            bigram[t[i:i+2]] = float(round(bigram.get(t[i:i+2]) +1.0/len(t), 7))
        else:
            bigram[t[i:i+2]] = float(round(1.0/len(t), 7))
    return bigram



def noncross_bigrams(t):
    ncbigrm = dict()
    t = t.lower()
    for i in range(0,len(t),2):
        if t[i] == u' ' and t[i+1] == u' ':
            continue
        if t[i:i+2] in ncbigrm:
            ncbigrm[t[i:i+2]] = float(round(ncbigrm.get(t[i:i+2]) + 1.0/len(t)*2, 7))
        else:
            ncbigrm[t[i:i+2]] = float(round(1.0/(len(t))*2, 7))
    return ncbigrm

def count_entropy(mydict):
    e = 0.0
    p = 0.0

    for i in mydict:
        p = float(mydict[i])
        e += p * log(p,2)
    return float(round(e*-1, 5))

def count_entropy_b(mydict):
    e = 0.0
    p = 0.0
    print (float(round(sum(mydict.values()), 5)))
    for i in mydict:
        p = float(mydict[i])
        e += p * log(p,2)/log(4,2)
    return float(round(e*-1, 5))

def count_entropy_b2(mydict):
    e = 0.0
    p = 0.0
    print (float(round(sum(mydict.values()), 5)))
    for i in mydict:
        p = float(mydict[i])
        e += p * log(p,2)/log(4,2)
    return float(round(e*-1, 5))

letter = mono_freq(text)
letter1 = mono_freq(text1)
bigram = cross_bigrams(text)
bigram1 = cross_bigrams(text1)
bezpbigram = noncross_bigrams(text)
bezpbigram1 = noncross_bigrams(text1)


print ("==============================MONOGRAMS WITH SPACE=================================")
for key, value in sorted(letter.items(), key= itemgetter(1), reverse=True):
        print ("%s: %s" % (key, value))

print (" ")    
print ("=======================MONOGRAMS WITHOUT SPACE=====================================")
for key, value in sorted(letter1.items(), key= itemgetter(1), reverse=True):
    print ("%s: %s" % (key, value))

print (" ")
print ("========================CROSSING BIGRAMS WITH SPACE================================")
for key, value in sorted(bigram.items(), key= itemgetter(1), reverse=True):
    print ("%s: %s" % (key, value))

print (" ")    
print ("=======================CROSSING BIGRAMS WITHOUT SPACE==============================")
for key, value in sorted(bigram1.items(), key= itemgetter(1), reverse=True):
    print ("%s: %s" % (key, value))

print (" ")    
print ("=========================NON-CROSSING BIGRAMS WITH SPACE===========================")
for key, value in sorted(bezpbigram.items(), key= itemgetter(1), reverse=True):
    print ("%s: %s" % (key, value))

print (" ")    
print ("=========================NON-CROSSING BIGRAMS WITHOUT SPACE========================")
for key, value in sorted(bezpbigram1.items(), key= itemgetter(1), reverse=True):
    print ("%s: %s" % (key, value))

print (" ")
print ("============================ H1 ===================")
print ("with space:")
print (count_entropy(letter))
print ("no space:")
print (count_entropy(letter1))
print (" ")
print ("============================ H2 ===================")
print ("############# crossing")
print ("with space:")
print (count_entropy_b(bigram))
print ("no space:")
print (count_entropy_b(bigram1))
print ("#############  non-crossing")
print ("with space:")
print (count_entropy_b2(bezpbigram))
print ("no space:")
print (count_entropy_b2(bezpbigram1))
