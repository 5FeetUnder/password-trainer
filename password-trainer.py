import os, hashlib, binascii
from getpass  import getpass

def hash_password(password, salt=None, iterations=260000):
    """Hash a password for Storing"""
    if salt is None:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, iterations)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password, iterations=260000):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), iterations)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

repeat = True

while repeat:
    password = hash_password(getpass("Please enter the password you want to train: "))
    successes = 0
    tries = int(input("Please enter as a number how many times you want to try: "))
    for i in range(1, tries + 1):
        print(f'\n\n{i}. try')
        if verify_password(password, getpass("Please try to enter your password: ")):
            successes += 1
            print(f"Correct! You've entered your password correctly {successes} times out of {i} tries.")
        else:
            print("Incorrect. Please try again.")
    print(f"\n\nYou've successfully entered your password {successes} out of {tries} times.")
    if input("Do you want to go again? (Y/N): ") not in "Yy":
        repeat = False
