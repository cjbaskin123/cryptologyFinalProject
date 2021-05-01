# RSA-Based Oblivious Transfer Method

This method of completing the 1-2 Oblivious Transfer method utilizes RSA for its security.  

The 1-2 Oblivious Transfer method starts with the sender (Alice) who has two messages and the receiver (Bob) who wants one of them.
Alice does not want Bob to know the contents of the other message and Bob does not want Alice to know which message Bob received.

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

# Usage
- The `allInOneMethod.py` file includes both Bob and Alice in one file and shows the values that are sent in the console.  It simply needs to be run in Python 3
- The files in the `Network Socket Method` folder include network socket communication between Alice and Bob.  The `dualTransmitBob.py` file must be run first and then the `dualTransmitAlice.py` file.  These files will open a socket on `localhost` on port `5464` so network communication must be enabled and permitted to run these files. 

# References

https://en.wikipedia.org/wiki/Oblivious_transfer#1%E2%80%932_oblivious_transfer

https://courses.grainger.illinois.edu/cs598dk/fa2019/Files/OT_notes.pdf

Even, Shimon, et al. “A Randomized Protocol for Signing Contracts.” Communications of the ACM, vol. 28, no. 6, June 1985, pp. 637–47. DOI.org (Crossref), doi:10.1145/3812.3818.