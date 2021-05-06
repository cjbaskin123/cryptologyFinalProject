import codecs
import hashlib
import random
import socket
import pickle

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
            # print(f"{x}^{y}={x^y}")
            outVals.append(x^y)
    else:
        for (x,y) in zip(a[:len(b)], b):
            # print(f"{x}^{y}={x ^ y}")
            outVals.append(x^y)
    return bytes(outVals)


def encode(message: str, key: str):
    """
    Encodes the given message with the given key using XOR encoding
    :param message: Message to encode
    :param key: Encoding key
    :return: ciphertext
    """
    messageBytes = message.encode('utf-8')
    messageHex = str(messageBytes.hex())

    while(len(messageHex) < len(key)):
        messageHex += "0"

    key_bytes = codecs.decode(key, 'hex')
    mess_bytes = codecs.decode(messageHex, 'hex')
    xored = a_xor_b(mess_bytes, key_bytes)
    return codecs.encode(xored, 'hex')


if __name__ == '__main__':
    shared_g = 2  # g is a generator number for the Diffie-Hellman Key Exchange that was previously agreed upon
    socketComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketComm.connect((HOST, PORT))

    messages = ['Message0IsThisOne', 'thisIsMessage1']  # Alice's Messages

    print("Alice generates a random 'a' value")
    a = random.randint(0, 2 ** 5)
    print(f"Alice's a = {a}")

    print("Alice generates 'A' = g^a and sends it to Bob")
    A = shared_g ** a

    socketComm.sendall(pickle.dumps(A))

    B = pickle.loads(socketComm.recv(1024))
    print(f"Alice received B={B} from Bob")

    print("Alice generates the two potential k values for each potential B value she could have received from Bob")
    kVals = ['', '']
    kVals[0] = B ** a
    kVals[1] = int((B / A) ** a)

    kVals_hashes = [getHash(val.to_bytes(500, "big")) for val in kVals]
    print(f"Alice takes the SHA256 hash of the two potential k values - {kVals_hashes}")

    encodedMessages = [encode(x, y) for (x, y) in zip(messages, kVals_hashes)]
    print("Alice encodes each message with its respective k value hash as the key")
    print(f"Encoded messages - {encodedMessages}")
    print("Alice sends the encoded messages to Bob")

    socketComm.sendall(pickle.dumps(encodedMessages))

