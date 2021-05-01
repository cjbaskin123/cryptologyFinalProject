import math
import time
import random
import rsa


randomSeed = 5#int(round(time.time() * 10))


def convertFromBytes(val):
    return int.from_bytes(val, byteorder='big')


def convertToBytes(val:bytes):
    return val.decode("UTF-8")
    # return val.to_bytes(5, byteorder='big')


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
    maxRandomExp = 8

    alice_messages = ['item1'.encode("UTF-8"), 'item2'.encode("UTF-8")]#, b'item3', b'item4', b'item5']

    alice_randoms = []
    for i in range(2):
        alice_randoms.append(random.randint(0, int(math.pow(2, maxRandomExp))))

    # Send randoms to Bob
    print(f"Alice sends {alice_randoms} to Bob")
    bobRandomVals = alice_randoms

    alice_public, alice_private = rsa.newkeys(16)

    print(f"Alice sends e={alice_public.e} and n={alice_public.n} to Bob")
    bob_N = alice_public.n
    bob_E = alice_public.e


    print("Bob picks a 'b' value as an index of the values sent to him.  Suppose Bob picks b=1")
    bob_b = 1
    bob_x_b = bobRandomVals[bob_b]
    bob_kVal = random.randint(0, int(math.pow(2, maxRandomExp)))
    print(f"Bob calculates a random 'k' value - {bob_kVal}")


    bob_v = modExp(bob_x_b + bob_kVal, bob_E, bob_N)
    print(f"Bob calculates v=(x_b + k)^e mod N")
    print(f"v={bob_v}")
    print(f"Bob sends {bob_v} to Alice")

    alice_v = bob_v

    print(f"ALice calculates for each k value k[i]=(v-x[i])^d mod n")
    alice_kVals = []
    for val in alice_randoms:
        alice_kVal = modExp(alice_v-val, alice_private.d, alice_private.n)
        alice_kVals.append(alice_kVal)

    alice_altMessages = []
    for index in range(len(alice_messages)):
        alice_altMessages.append(convertFromBytes(alice_messages[index]) + alice_kVals[index])

    print(f"Alice sends {alice_altMessages} to Bob")

    bob_altMessages = alice_altMessages

    print(bob_altMessages[bob_b] - bob_kVal)

    bob_corrMessage = convertToBytes(int(bob_altMessages[bob_b] - bob_kVal))
    print(f"Bob has message {bob_corrMessage}")




    # print(int(aliceMessages[0]))

    # alicePublic, alicePrivate = rsa.newkeys(16)
    # print(alicePublic)
    # print()
    # print(alicePrivate)
    #
    # print(alicePublic.n)
    # print(alicePublic.e)

    # Alice sends n and e to Bob


