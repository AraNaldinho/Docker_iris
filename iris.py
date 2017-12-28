
import cv2
import numpy as np
import random
from random import randint


'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


def is_prime1(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

def generate_big_prime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n-1), 2**n)
        if is_prime1(p, 1000):
            return p



'''
Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    #n = pq
    n = p * q

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    print ("in generating phi",phi)
    print ("in generating e",e)
    #Use Extended Euclid's Algorithm to generate the private key
    d = modinv(e, phi)
    print (d)    
    #Return public and private keypair
    #Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char)** key) % n for char in plaintext]
    #Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)

def circle_det(a):
    img = cv2.imread(a,0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    circles=10
    circles = np.uint16(np.around(circles))
    return circles

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    print ("RSA Encrypter/ Decrypter")
    a=circle_det('download.jpeg')
    p = generate_big_prime(a)
    q = generate_big_prime(a)
    print ("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print ("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print ("Your encrypted message is: ")
    print (''.join(map(lambda x: str(x), encrypted_msg)))
    print ("Decrypting message with public key ", public ," . . .")
    print ("Your message is:")
    print (decrypt(public, encrypted_msg))
