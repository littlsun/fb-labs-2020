import json
from random import *

import requests


class Key:
	n = 0
	e = 0
	d = 0


class Message:
	k = 0
	s = 0

# GET http://asymcryptwebservice.appspot.com/rsa/encrypt?modulus=8092F9103640E910594AA0F4E2148B79&publicExponent=10001&message=Test_Message&type=TEXT
def encrypt(Modulus, publicExponent, Message, Type):
	return session.get("http://asymcryptwebservice.appspot.com/rsa/encrypt?modulus=" + hex(Modulus)[2:] + "&publicExponent=" + hex(publicExponent)[2:]+"&message="+Message+"&type="+ Type)


def verify(Message, Sign, Modulus, publicExponent):
	return session.get("http://asymcryptwebservice.appspot.com/rsa/verify?message=" + hex(Message)[2:] + "&type=BYTES&signature=" + hex(Sign)[2:] + "&modulus=" + hex(Modulus)[2:] + "&publicExponent=" + hex(publicExponent)[2:])


def sign(Message):
	return session.get("http://asymcryptwebservice.appspot.com/rsa/sign?message="+hex(Message)[2:]+"&type=BYTES")

# receive key and signature
def sendKey(Modulus, publicExponent):
	return session.get("http://asymcryptwebservice.appspot.com/rsa/sendKey?modulus=" + hex(Modulus)[2:] + "&publicExponent=" + hex(publicExponent)[2:])

# server my my my
def receiveKey(Key, Signature, Modulus, publicExponent):
	return session.get("http://asymcryptwebservice.appspot.com/rsa/receiveKey?key=" + hex(Key)[2:] + "&signature=" + hex(Signature)[2:] + "&modulus=" + hex(Modulus)[2:] + "&publicExponent=" + hex(publicExponent)[2:])


def encypher(m, n, e):
	return pow(m, e, n)


def decypher(c, n, d):
	return pow(c, d, n)


def create_sign(k, n, d):
	return pow(k, d, n)


def check_conf(m, n, d):
	return pow(m, d, n)


def check_sigh(s, n, e):
	return pow(s, e, n)


def create_message(k, d, e1, n, n1):
	k1 = encypher(k, n1, e1)
	s = create_sign(k, n, d)
	s1 = encypher(s, n1, e1)
	return [k1, s1]


def reverse(x, m):
	Gcd, a, b = gcdExtended(x, m)
	if Gcd == 1:
		return (a % m + m) % m


def create_keys(q, p):
	n = q * p  # modulus
	phi_n = (q - 1) * (p - 1)
	while True:
		e = randrange(2, phi_n - 1)
		if gcd(e, phi_n) == 1:
			d = reverse(e, phi_n)
			if d is None:
				continue
			else:
				return n, e, d
		else:
			continue


def generate(n, length):
	print("Відкинуті значення::")
	result = []
	counter = 0
	while True:
		numb = ['1']
		for x in range(0, length - 2):
			numb.append(str(getrandbits(1)))
		numb.append('1')
		nn = ""
		for x in numb:
			nn += x
		r_ = int(nn, 2)
		bp_flag = 0
		for bp in basic_primes:
			if r_ % bp != 0:
				bp_flag += 1
		if bp_flag == 4:
			if define_prime(r_) is True:
				result.append(r_)
				counter += 1
			else:
				print(r_)
		if counter == n:
			break
	return result


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


def define_prime(p):
	for bp in basic_primes:
		if p % bp == 0:
			return False
	k = 20
	z = 0
	d = p - 1
	while True:
		if d % 2 == 0:
			d = d // 2
			z += 1
		else:
			break
	for iteration in range(k):
		x = randint(2, p - 1)
		if gcd(x, p) == 1:
			pw = pow(x, d, p)
			if pw == 1 or pw - p == -1:
				print("", end="")
			else:
				flag = 0
				for r in range(1, z):
					xr = pow(x, d * (2 ** r), p)
					if xr - p == -1:
						flag = 1
						break
					elif xr == 1:
						return False
				if flag == 0:
					return False
		else:
			return False
	return True


basic_primes = [2, 3, 5, 7]

if __name__ == '__main__':
	session = requests.Session()
	serverPKey = json.loads(session.get("http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=512").content)

	digits = sorted(generate(4, 256))
	# n e d
	A = create_keys(digits[0], digits[1])
	B = create_keys(digits[2], digits[3])
	# [k1,s1]
	K = 0x100# randrange(0, A[0])
	# k d e1 n n1
	M = create_message(K, A[2], B[1], A[0], B[0])
	# m n d
	k = check_conf(M[0], B[0], B[2])
	# m n d
	s = check_conf(M[1], B[0], B[2])
	# s n e
	k_s = check_sigh(create_sign(K, A[0], A[2]), A[0], A[1])
	Ss = create_sign(K, A[0], A[2])

	print(f"\np  {digits[0]}\nq  {digits[1]}\np1 {digits[2]} \nq1 {digits[3]}\nA::\nn {A[0]}\ne {A[1]}\nd {A[2]}\nB::\nn {B[0]}\ne {B[1]}\nd {B[2]}")
	print(f"\nВТ::     {Ss}\nШТ::     {M[1]}\nПідпис:: {Ss}\n\nTests::\nstart   {K}\nconf	{k}\nauth	{k_s}")

	print("\nПеревірка verify")
	response = verify(K, create_sign(K, A[0], A[2]), A[0], A[1]).content
	y = json.loads(response)
	print(y)

	print("Перевірка sign")
	response = sign(K).content
	y = json.loads(response)
	print(y)

	print("Перевірка sendKey")
	response = sendKey(A[0], A[1]).content
	y = json.loads(response)
	print(y)

	print("Перевірка create_message")
	rKey = create_message(K, A[2], int(serverPKey['publicExponent'], 16), A[0], int(serverPKey['modulus'], 16))
	response = receiveKey(rKey[0], rKey[1], A[0], A[1]).content
	y = json.loads(response)
	print(y)

	print("\nМи шифруємо, сервер дешифрує")
	# def encrypt(Modulus, publicExponent, Message, Type):
	response = encrypt(int(serverPKey['modulus'], 16), int(serverPKey['publicExponent'], 16), "100", "BYTES").content
	y = json.loads(response)
	print(y)
	x = "http://asymcryptwebservice.appspot.com/rsa/decrypt?cipherText="+hex(rKey[0])[2:]+"&expectedType=BYTES"
	print(session.get(x).content)

	print("\nСервер шифрує, ми дешифруємо")
	response = encrypt(int(serverPKey['modulus'], 16), int(serverPKey['publicExponent'], 16), "100", "BYTES").content
	response = encrypt(A[0], A[1], hex(100)[2:], "BYTES").content
	y = json.loads(response)
	print(y)
	res = check_conf(int(y['cipherText'], 16), A[0], A[2])
	print(f"res {res}")