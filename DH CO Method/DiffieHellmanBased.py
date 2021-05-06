import random
import hashlib
import codecs


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
    """
    Simulates the Oblivious Transfer process between Alice and Bob
    :return: Nothing
    """
    shared_g = 2  # g is a generator number for the Diffie-Hellman Key Exchange that was previously agreed upon

    alice_messages = ['Message0IsThisOne', 'thisIsMessage1']  # Alice's Messages

    bob_c = 1 # Bob's c value

    print("Alice generates a random 'a' value")
    alice_a = random.randint(0, 2 ** 5)
    print(f"Alice's a = {alice_a}")

    print("")
    print("Bob generates a random 'b' value")
    bob_b = random.randint(0, 2 ** 5)
    print(f"Bob's b = {bob_b}")

    print("")

    print("Alice generates 'A' = g^a and sends it to Bob")
    alice_A = shared_g ** alice_a
    bob_A = alice_A
    print(f"Alice sends A = '{alice_A}' to Bob")

    print("")

    print("Bob checks his 'c' value and will make one of two B values")
    print("If c=0, B=g^b")
    print("If c=1, B=A*g^b")
    if bob_c == 0:
        print("Since c=0, B=g^b")
        bob_B = shared_g ** bob_b
    else:
        print("Since c=1, B=A*g^b")
        bob_B = bob_A * shared_g ** bob_b

    print("Bob generates his k value by calculating A^b")
    bob_k = bob_A**bob_b
    print(f"Bob's k = {bob_k}")

    bob_k_hash = getHash(bob_k.to_bytes(500, "big"))
    print(f"Bob takes the SHA256 hash of his k value to use as an encryption key - {bob_k_hash}")

    print("Bob sends his B value to Alice")
    print(f"Bob sends B={bob_B} to Alice")
    alice_B = bob_B

    print("")

    print("Alice generates the two potential k values for each potential B value she could have received from Bob")
    alice_kVals = ['','']
    alice_kVals[0] = alice_B ** alice_a
    alice_kVals[1] = int((alice_B / alice_A) ** alice_a)

    alice_kVals_hashes = [getHash(val.to_bytes(500, "big")) for val in alice_kVals]
    print(f"Alice takes the SHA256 hash of the two potential k values - {alice_kVals_hashes}")

    alice_encodedMessages = [encode(x, y) for (x,y) in zip(alice_messages, alice_kVals_hashes)]
    print("Alice encodes each message with its respective k value hash as the key")
    print(f"Encoded messages - {alice_encodedMessages}")

    print("Alice sends the encoded messages to Bob")
    bob_encodedMessages = alice_encodedMessages

    print("")

    print("Bob decodes his message using his hashed k value")
    bob_decodedMessages = [decode(mess, bob_k_hash) for mess in bob_encodedMessages]

    print(f"Bob's message that he received is: {bob_decodedMessages[bob_c]}")
    bob_otherIndex = 0 if bob_c == 1 else 1
    print(f"The other message that Bob would see if he tried to decrypt it is: '{bob_decodedMessages[bob_otherIndex]}'")
