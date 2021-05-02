import math
import pickle
import time
import random
import rsa

randomSeed = int(round(time.time() * 10))


def convertFromBytes(bytesVal):
    return int.from_bytes(bytesVal, byteorder='little', signed=False)


def convertToBytes(intVal: int, len: int = 64):
    return intVal.to_bytes(len, byteorder='little', signed=False)


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

    alice_messages = ['Message0IsThisOne'.encode("UTF-8"), 'thisIsMessage1'.encode("UTF-8"),
                      'thisIsTestingItem2'.encode("UTF-8"),
                      'thisIsTestingItem3'.encode("UTF-8"), 'thisIsTestingTheItem4'.encode("UTF-8"),
                      'thisIsTestingTheItem5'.encode("UTF-8")]

    alice_public, alice_private = rsa.newkeys(512)

    print(f"Alice sends e={alice_public.e} and n={alice_public.n} to Bob")
    bob_N = alice_public.n
    bob_E = alice_public.e

    alice_randoms_x = []
    for i in range(len(alice_messages)):
        alice_randoms_x.append(random.randint(0, int(math.pow(2, maxRandomExp))))

    # Send randoms to Bob
    print(f"Alice sends {alice_randoms_x} to Bob")
    bob_randoms_x = alice_randoms_x

    bob_b = len(alice_messages) // 2
    print(f"Bob picks a 'b' value as an index of the values sent to him.  Suppose Bob picks b={bob_b}")
    bob_x_b = bob_randoms_x[bob_b]
    bob_kVal = random.randint(0, int(math.pow(2, maxRandomExp)))
    print(f"Bob calculates a random 'k' value - {bob_kVal}")

    bob_v = rsa.encrypt(pickle.dumps(bob_kVal + bob_x_b), alice_public)
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
        alice_kVal = kva - val
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

    bob_otherMessages = []
    for altMess in bob_altMessages:
        if altMess == bob_altMessages[bob_b]:
            continue
        bob_otherMessage = convertToBytes(int(altMess - bob_kVal))
        bob_otherMessage = bob_otherMessage.strip(b'\x00')
        bob_otherMessages.append(bob_otherMessage)

    print(f"If bob tried to view the other messages with his K intVal, he would get {bob_otherMessages}, which are "
          f"incorrect values")
