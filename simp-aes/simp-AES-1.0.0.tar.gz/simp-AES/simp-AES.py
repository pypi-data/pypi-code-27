import os, random, string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def GenerateKey():
    """
    Generates a random symmetric key that is stored in a text file in the user's computer.
    Returns symmetric key.
    """
    key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))    # Key in string form
    return key.encode('utf-8')


def Encrypt(key, filename):
    chunksize = 64* 1024
    outputFile = filename + '.cat'
    filesize = str(os.path.getsize(filename)).zfill(16)     # Get the filesize and then zfill to 16 bytes
    IV = Random.new().read(16)                              # Read 16 bytes out of that

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))         # As filesize is a string, we are going to encode it into bytes
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:                     # Then we've run out of bytes to encrypt in the file
                    break
                elif len(chunk) % 16 != 0:
                    # If less than 16 bytes, then we'd need to pad
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

    # Remove the original file
    os.remove(filename)


def Decrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename[:-4]  # The output file name would be everything but the '.cat' extension.

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)              # To remove any padding that was added in during the encryption stage

    # Remove the encrypted version of the file
    os.remove(filename)


def GetKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")

    if choice == 'E':
        filename = input("File to encrypt: ")
        password = input("Password: ")
        Encrypt(GetKey(password), filename)
        print("Done.")

    elif choice == 'D':
        filename = input("File to decrypt: ")
        password = input("Password: ")
        Decrypt(GetKey(password), filename)
        print("Done.")

    else:
        print("No option selected, closing...")

if __name__ == '__main__':
    Main()
