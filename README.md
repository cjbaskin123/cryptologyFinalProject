# Implementation Overviews

The 1-2 Oblivious Transfer method starts with the sender (Alice) who has two messages and the receiver (Bob) who wants one of them.
Alice does not want Bob to know the contents of the other message and Bob does not want Alice to know which message Bob received.


## RSA-Based Oblivious Transfer Method

This method of completing the 1-2 Oblivious Transfer method utilizes RSA for its security.  It was created by Shimon Even, Oded Goldreich, and Abraham Lempel.

This process works as follows:

1. Alice has 2 messages <img src="https://render.githubusercontent.com/render/math?math=m_1"> and <img src="https://render.githubusercontent.com/render/math?math=m_2">
2. Alice generates an RSA public-private key pair
3. Alice generates 2 random integer values <img src="https://render.githubusercontent.com/render/math?math=x_0, x_1"> and sends them with her public key to Bob
4. Bob picks one of the random values and sets <img src="https://render.githubusercontent.com/render/math?math=b"> equal to the index of that value
5. Bob generates a random value <img src="https://render.githubusercontent.com/render/math?math=k"> and computes <img src="https://render.githubusercontent.com/render/math?math=x_b%2bk">
6. Bob encrypts that computed value with Alice's public key and sends it to Alice
7. Alice does not know what Bob chose as <img src="https://render.githubusercontent.com/render/math?math=b"> so when she decrypts the value that Bob sends, she can only determine <img src="https://render.githubusercontent.com/render/math?math=x_b%2Bk">.  By taking both of the <img src="https://render.githubusercontent.com/render/math?math=x"> values, she can determine 2 potential <img src="https://render.githubusercontent.com/render/math?math=k"> values, only one of which having any meaning.
8. Alice will take her 2 calculated possible <img src="https://render.githubusercontent.com/render/math?math=k"> values and add them to her message values (making <img src="https://render.githubusercontent.com/render/math?math=m_1^'"> and <img src="https://render.githubusercontent.com/render/math?math=m_2^'">) and send both of them to Bob
9. Bob knows his <img src="https://render.githubusercontent.com/render/math?math=b"> and <img src="https://render.githubusercontent.com/render/math?math=k"> values so he takes <img src="https://render.githubusercontent.com/render/math?math=m_b^'"> and subtracts <img src="https://render.githubusercontent.com/render/math?math=k"> in order to determine <img src="https://render.githubusercontent.com/render/math?math=m_b">, the original message

As can clearly be seen, this process allows Alice to send one (and only one) of her messages to Bob and Bob is only able to see the message he chose.  Alice also does not know which message Bob received.

*Note: This description of the process is what would occur utilizing it as a 1-2 Oblivious Transfer method.  The implementation in the code is a 1-5 method which operates on the same principles, simply with more random integer values sent in step 3 and more k values calculated by Alice and sent to Bob in steps 7-9.*

## Diffie-Hellman Key Exchange Based Oblivious Transfer Method
This method of completing the 1-2 Oblivious Transfer process is based upon the Diffie-Hellman Key Exchange.  It was created by Tung Chou and Claudio Orlandi.

This process works as follows:
1. Alice and Bob have an agreed upon generator value <img src="https://render.githubusercontent.com/render/math?math=g">, equivalent to the <img src="https://render.githubusercontent.com/render/math?math=g"> value used in the Diffie-Hellman key exchange
2. Alice has 2 messages <img src="https://render.githubusercontent.com/render/math?math=m_1"> and <img src="https://render.githubusercontent.com/render/math?math=m_2">, Bob has a bit value <img src="https://render.githubusercontent.com/render/math?math=c"> (either 0 or 1)
3. Alice and Bob both generate a random integer value each <img src="https://render.githubusercontent.com/render/math?math=a, b">  (These values are **NEVER** shared directly with anyone)
4. Alice calculates <img src="https://render.githubusercontent.com/render/math?math=A=g^a"> and sends the value to Bob
5. Bob checks his <img src="https://render.githubusercontent.com/render/math?math=c"> value and calculates 1 of 2 possible <img src="https://render.githubusercontent.com/render/math?math=B"> values.  If <img src="https://render.githubusercontent.com/render/math?math=c=0, B=g^b"> and if <img src="https://render.githubusercontent.com/render/math?math=c=1, B=A*g^b">.  Bob then sends this B value to Alice.
6. Bob generates his <img src="https://render.githubusercontent.com/render/math?math=k"> value which is equal to <img src="https://render.githubusercontent.com/render/math?math=A^b">.  He then takes the hash of this value to use as an encryption key.   
7. Alice does not know what Bob's <img src="https://render.githubusercontent.com/render/math?math=B"> value is so there are one of two possible <img src="https://render.githubusercontent.com/render/math?math=k"> values that she generates, one value for each potential <img src="https://render.githubusercontent.com/render/math?math=B"> value that Bob may have sent.  She then takes the hash of the <img src="https://render.githubusercontent.com/render/math?math=k"> values to use in the encryption in the next step
8. Alice encrypts each message with the respective hashed <img src="https://render.githubusercontent.com/render/math?math=k"> value as the key.  She then sends these values to Bob.
9. Bob knows which message is his since he picked his <img src="https://render.githubusercontent.com/render/math?math=c"> value.  He then decrypts that value using his hashed <img src="https://render.githubusercontent.com/render/math?math=k"> value as the decryption key.

# Usage
- The two methods are separated into separate folders, named for the method type.
- Within each respective method folder:  
    - The `allInOneMethod.py` file includes both Bob and Alice in one file and shows the values that are sent in the console.  It simply needs to be run.
    - The files in the `Network Socket Method` folder include network socket communication between Alice and Bob.  The `dualTransmitBob.py` file must be run first and then the `dualTransmitAlice.py` file.  These files will open a socket on `localhost` on port `54645` so network communication must be enabled and permitted to run these files.
- All python files in this program are created and designed to be run in Python 3
## Requirements

This program has the following required imports (I attempted to keep everything in the standard python libraries but apologies if I missed any and you need to `pip install` them):

- `import random`
- `import hashlib`
- `import codecs`
- `import time`  
- `import rsa` (Only in the RSA based version)  
- `import socket` (Only in the network socket version)
- `import pickle` (Only in the network socket version)

# References

Chou, Tung, and Claudio Orlandi. “The Simplest Protocol for Oblivious Transfer.” Progress in Cryptology -- LATINCRYPT 2015, 2015, pp. 40–58., doi:10.1007/978-3-319-22174-8_3. 

Crépeau, C. (1988). Equivalence Between Two Flavours of Oblivious Transfers. In Advances in Cryptology — CRYPTO ’87 (pp. 350–354). Springer Berlin Heidelberg. https://doi.org/10.1007/3-540-48184-2_30

Even, Shimon, et al. “A Randomized Protocol for Signing Contracts.” Communications of the ACM, vol. 28, no. 6, June 1985, pp. 637–647., doi:10.1145/3812.3818. 

Rabin, M. O. (1981). How to exchange secrets with oblivious transfer. Technical Report TR-81. Aiken Computation Lab, Harvard University. Retrieved from https://eprint.iacr.org/2005/187.pdf