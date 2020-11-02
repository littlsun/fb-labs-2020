#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter, attrgetter

from math import log

f = open("./text2.txt",  encoding="utf8")
data = f.read()
text1=""
dictionary1="абвгдежзийклмнопрстуфхцчшщъыьэюя"
keylist1=["да","нет","жаль","может","форель","наверно","возможно","кукарекал","десятьбукв","аггресивный","жонглировать","автотрранспор"]
keylist=["ав","авт","авто","автот","автотр","автотра","автортран","автотранс","автотрансп","автотранспо","автотранспор","автотранспорт"]
for y in data:
    y = y.lower()
    for x in dictionary1:
        if y=="ё":
            y="e"
        if y==x:
            text1+=y
        else:
            continue

thislist=list()
for i in range (0, len(dictionary1)):
    thislist.append(dictionary1[i])


def findcharnumb(ch):
    for i in range(0, len(thislist)):
        if ch==thislist[i]:
            return i;

def findchar(nm):
    for i in range(0, len(thislist)):
        if nm==i:
            return thislist[i];

def encode(t,s):
#взять букву с текста и сложить по модулю с ключём
    temp=""
    for i in range(0,len(t)):
            temp+=findchar((findcharnumb(t[i])+findcharnumb(s[i%len(s)]))%32)
    return temp

def mono_freq(t):
    letter = dict()
    for i in t:
        if i == u'\n':
            continue
        if i in letter:
            letter[i] = float(letter.get(i) + 1.0/len(t))
        else:
            letter[i] = float(1.0/len(t))
    return letter

letter1 = mono_freq(text1)

print ("\n======================= Відкритий текст =====================================")
for key, value in sorted(letter1.items(), key= itemgetter(1), reverse=True):
    print ("\"%s\": %s" % (key, round(value,7)),end="\t")

print("\n\n",text1[0:25])

for i in range(0, len (keylist)):
    print ("\n\n========================================== Шифрований текст",i,"=====================================")
    print("\nдлинна ключа=",len(keylist[i]),"\n\n",text1[0:25],"\n",encode(text1,keylist[i])[0:25],"\n")
    for key, value in sorted(mono_freq(encode(text1,keylist[i])).items(), key= itemgetter(1), reverse=True):
        print ("\"%s\": %s" % (key, round(value,7)), end="\t")

print("\n")