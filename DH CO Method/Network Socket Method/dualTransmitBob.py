import codecs
import hashlib
import pickle
import random
import socket

HOST = '127.0.0.1'
PORT = 54645


def getHash(val):
    """
    Gets the SHA256 Hash of the provided value
    :param val: Value to get the hash of
    :return: The SHA256 hash of the given value
    """
    sha256 = hashlib.sha256()
    sha256.update(val)
    return sha256.hexdigest()


def a_xor_b(a, b):
    """
    Returns a XOR b
    Will only return a value that is as long as the shortest value of a or b
    :param a: First value to XOR
    :param b: Second value to XOR
    :return: a XOR b
    """
    outVals = []
    if (len(a) < len(b)):
        for (x,y) in zip(a, b[:len(a)]):
            outVals.append(x^y)
    else:
        for (x,y) in zip(a[:len(b)], b):
            outVals.append(x^y)
    return bytes(outVals)


def decode(ciphertext, key):
    """
    Decodes the given ciphertext with the given key using XOR encoding
    :param ciphertext: Ciphertext to decode
    :param key: Encoding key
    :return: Decoded ciphertext
    """
    key_bytes = codecs.decode(key, 'hex')

    ciphertext_bytes = codecs.decode(ciphertext, 'hex')

    xored = a_xor_b(ciphertext_bytes, key_bytes)

    xored = str(codecs.encode(xored, 'hex'))[2:-1]
    while(xored[-1] == '0'):
        xored = xored[0:-1]
    xored = codecs.decode(xored, 'hex')
    return xored.decode('utf-8', errors='ignore')


if __name__ == '__main__':
    shared_g = 2  # g is a generator number for the Diffie-Hellman Key Exchange that was previously agreed upon

    socketComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketComm.bind((HOST, PORT))

    socketComm.listen()
    conn, addr = socketComm.accept()

    print("Bob generates a random 'b' value")
    b = random.randint(0, 2 ** 5)
    print(f"Bob's b = {b}")

    print("Bob receives 'A' value from Alice")
    A = pickle.loads(conn.recv(1024))
    print(f"Bob received A={A}")

    print("Bob picks a 'c' value as either 0 or 1")
    c = input(f"Please pick a 'c' value (0 or 1): ").strip()
    c = int(c)

    print("Bob checks his 'c' value and will make one of two B values")
    print("If c=0, B=g^b")
    print("If c=1, B=A*g^b")
    if c == 0:
        print("Since c=0, B=g^b")
        B = shared_g ** b
    else:
        print("Since c=1, B=A*g^b")
        B = A * shared_g ** b

    print("Bob generates his k value by calculating A^b")
    k = A ** b
    print(f"Bob's k = {k}")

    k_hash = getHash(k.to_bytes(500, "big"))
    print(f"Bob takes the SHA256 hash of his k value to use as an encryption key - {k_hash}")

    print(f"Bob sends his B value (B={B}) to Alice")
    conn.sendall(pickle.dumps(B))

    encodedMessages = pickle.loads(conn.recv(1024))
    print(f"Bob received {encodedMessages} from Alice")

    print("Bob decodes his message using his hashed k value")
    decodedMessages = [decode(mess, k_hash) for mess in encodedMessages]

    print(f"Bob's message that he received is: {decodedMessages[c]}")
    bob_otherIndex = 0 if c == 1 else 1
    print(f"The other message that Bob would see if he tried to decrypt it is: '{decodedMessages[bob_otherIndex]}'")
