import math
import random
import socket
import pickle
import rsa

HOST = '127.0.0.1'
PORT = 54645


def convertFromBytes(val):
    return int.from_bytes(val, byteorder='big')


if __name__ == '__main__':
    socketComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketComm.connect((HOST, PORT))

    alice_messages = ['Message0IsThisOne'.encode("UTF-8"), 'thisIsMessage1'.encode("UTF-8"),
                'thisIsTestingItem2'.encode("UTF-8"),
                'thisIsTestingItem3'.encode("UTF-8"), 'thisIsTestingTheItem4'.encode("UTF-8"),
                'thisIsTestingTheItem5'.encode("UTF-8")]

    maxRandomExp = 40

    alice_randoms = []
    for i in range(len(alice_messages)):
        alice_randoms.append(random.randint(0, int(math.pow(2, maxRandomExp))))

    print(f"Alice sends {alice_randoms} to Bob")
    socketComm.sendall(pickle.dumps(alice_randoms))
    receivedMessage = socketComm.recv(1024)  # For Blocking
    alice_public, alice_private = rsa.newkeys(512)
    print(f"Alice sends e={alice_public.e} and n={alice_public.n} to Bob")

    socketComm.sendall(pickle.dumps(alice_public))

    v = pickle.loads(socketComm.recv(1024))
    print(f"Received v val from Bob - {v}")
    decV = rsa.decrypt(v, alice_private)
    decV = pickle.loads(decV)
    print("Alice decrypts the 'v' value with her private key and subtracts each k value from it")
    print("Since Alice does not know k, she cannot fully decrypt it.")
    print(f"Alice's decrypted 'v' value is {decV}")

    kVals = []
    for val in alice_randoms:
        kVal = decV-val
        kVals.append(kVal)

    print("Alice now develops integer strings which are composed of the integer-converted messages + the generated k "
          "values")
    alice_altMessages = []
    for index in range(len(alice_messages)):
        alice_altMessages.append(convertFromBytes(alice_messages[index]) + kVals[index])

    print(f"Alice sends {alice_altMessages} to Bob")
    socketComm.sendall(pickle.dumps(alice_altMessages))

