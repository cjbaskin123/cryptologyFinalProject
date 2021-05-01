import math
import pickle
import time
import random
import rsa


randomSeed = int(round(time.time() * 10))


def convertFromBytes(val):
    return int.from_bytes(val, byteorder='little', signed=False)


def convertToBytes(val:int, len:int=64):
    # return val.decode("UTF-8")
    return val.to_bytes(len, byteorder='little', signed=False)


def modExp(aVal, kVal, nVal):
    binKVals = bin(kVal)[2:]
    binKVals = binKVals[::-1]

    bVal = 1
    A_val = aVal

    for index in range(len(binKVals)):
        if index == 0:
            if binKVals[index] == '1':
                bVal = aVal
        else:
            A_val = math.pow(A_val, 2) % nVal
            if binKVals[index] == '1':
                bVal = A_val * bVal % nVal

    return bVal


if __name__ == '__main__':
    random.seed(randomSeed)
    maxRandomExp = 50

    alice_messages = ['Message0IsThisOne'.encode("UTF-8"), 'thisIsMessage1'.encode("UTF-8")]  #, b'item3', b'item4', b'item5']

    alice_public, alice_private = rsa.newkeys(512)

    print(f"Alice sends e={alice_public.e} and n={alice_public.n} to Bob")
    bob_N = alice_public.n
    bob_E = alice_public.e

    alice_randoms_x = []
    for i in range(2):
        alice_randoms_x.append(random.randint(0, int(math.pow(2, maxRandomExp))))

    # Send randoms to Bob
    print(f"Alice sends {alice_randoms_x} to Bob")
    bob_randoms_x = alice_randoms_x

    print("Bob picks a 'b' value as an index of the values sent to him.  Suppose Bob picks b=1")
    bob_b = 1
    bob_x_b = bob_randoms_x[bob_b]
    bob_kVal = random.randint(0, int(math.pow(2, maxRandomExp)))
    print(f"Bob calculates a random 'k' value - {bob_kVal}")

    # bob_v = int(modExp(int(bob_x_b + kVal), bob_E, bob_N))
    # bob_v = modExp(kVal, bob_E, bob_N)
    bob_v = rsa.encrypt(pickle.dumps(bob_kVal+bob_x_b), alice_public)
    print(f"Bob encrypts the value 'x_b + k' with Alice's public key.  Since Alice does not know k, she cannot fully "
          f"decrypt it.")
    print(f"Bob calculates v={bob_v}")
    print(f"Bob sends {bob_v} to Alice")

    alice_v = bob_v

    print("Alice decrypts the 'v' value with her private key and subtracts each k value from it")
    kva = rsa.decrypt(alice_v, alice_private)
    kva = pickle.loads(kva)

    print(f"Alice's decrypted 'v' value is {kva}")

    alice_kVals = []
    for val in alice_randoms_x:
        # alice_kVal = int(modExp(int(alice_v-val), alice_private.d, alice_private.n))
        alice_kVal = kva-val
        alice_kVals.append(alice_kVal)

    print("Alice now develops integer strings which are composed of the integer-converted messages + the generated k "
          "values")
    alice_altMessages = []
    for index in range(len(alice_messages)):
        alice_altMessages.append(convertFromBytes(alice_messages[index]) + alice_kVals[index])

    print(f"Alice sends {alice_altMessages} to Bob")
    bob_altMessages = alice_altMessages

    bob_corrMessage = convertToBytes(int(bob_altMessages[bob_b] - bob_kVal))
    bob_corrMessage = bob_corrMessage.strip(b'\x00')
    print(f"Bob has message {bob_corrMessage}")

    bob_otherMessage = convertToBytes(int(bob_altMessages[0] - bob_kVal))
    bob_otherMessage = bob_otherMessage.strip(b'\x00')

    print(f"If bob tried to view the other message with his K val, he would get {bob_otherMessage}, which is an "
          f"incorrect value")