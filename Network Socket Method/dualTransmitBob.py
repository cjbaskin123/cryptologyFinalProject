import math
import pickle
import random
import socket

import rsa

HOST = '127.0.0.1'
PORT = 5464

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


def convertToBytes(val:int, len:int=64):
    return val.to_bytes(len, byteorder='big', signed=False)


if __name__ == '__main__':
    maxRandomExp = 40

    socketComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketComm.bind((HOST, PORT))
    if socketComm is None:
        exit(-1)

    socketComm.listen()
    conn, addr = socketComm.accept()

    data = conn.recv(1024)
    bob_randoms: list = pickle.loads(data)
    print(f"Bob received randoms from Alice - {bob_randoms}")
    conn.sendall(b"RECEIVED MESSAGE WITH RANDOM X VALS")

    pubKeyData = conn.recv(1024)

    alicePubKey: rsa.PublicKey = pickle.loads(pubKeyData)

    e = alicePubKey.e
    n = alicePubKey.n

    print(f"Bob received e={e}, n={n} from Alice")

    print("Bob picks a 'b' value as an index of the values sent to him.")
    bob_bVal = input(f"Please pick a 'b' value (0 to {len(bob_randoms)}): ").strip()
    bob_bVal = int(bob_bVal)

    x_b = bob_randoms[bob_bVal]
    kVal = random.randint(0, int(math.pow(2, maxRandomExp)))
    print(f"Bob calculates a random 'k' value - {kVal}")

    v = rsa.encrypt(pickle.dumps(kVal+x_b), alicePubKey)  # Using pickle to make it into a byte string
    print("Bob encrypts the value 'x_b + k' with Alice's public key.  Since Alice does not know k, she cannot fully "
          "decrypt it.")
    print(f"v={v}")
    print(f"Bob sends {v} to Alice")

    conn.sendall(pickle.dumps(v))
    alice_altMessages = pickle.loads(conn.recv(1024))
    print(f"Bob receives {alice_altMessages} from Alice")

    print("Bob knows what his 'b' value is so he can pick the correct message and subtract K from it to view it")
    corrMessage = convertToBytes(int(alice_altMessages[bob_bVal] - kVal))
    corrMessage = corrMessage.strip(b'\x00')
    print(f"Bob has message '{corrMessage}' which is the correct message")

    otherMessages = []
    for altMess in alice_altMessages:
        if altMess == alice_altMessages[bob_bVal]:
            continue
        bob_otherMessage = convertToBytes(int(altMess - kVal))
        bob_otherMessage = bob_otherMessage.strip(b'\x00')
        otherMessages.append(bob_otherMessage)

    print("If bob tried to decrypt the other messages, he would not get the correct results")
    print(f"The other messages would be '{otherMessages}' which are incorrect")