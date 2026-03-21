import dns.message
import dns.rdatatype
import dns.rdataclass
import dns.rdtypes
import dns.rdtypes.ANY
from dns.rdtypes.ANY.MX import MX
from dns.rdtypes.ANY.SOA import SOA
import dns.rdata
import socket
import threading
import signal
import os
import sys
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_aes_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )
    key = kdf.derive(password.encode('utf-8'))
    key = base64.urlsafe_b64encode(key)
    return key

def encrypt_with_aes(input_string, password, salt):
    key = generate_aes_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(input_string.encode('utf-8'))
    return encrypted_data    

def decrypt_with_aes(encrypted_data, password, salt):
    key = generate_aes_key(password, salt)
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

salt = b'Tandon' 
password = 'amn9412@nyu.edu'
input_string = "Always Watching"

encrypted_value = encrypt_with_aes(input_string, password, salt)
decrypted_value = decrypt_with_aes(encrypted_value, password, salt)

dns_records = {
    'example.com.': {
        dns.rdatatype.A: '192.168.1.101',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        dns.rdatatype.MX: [(10, 'mail.example.com.')],
        dns.rdatatype.CNAME: 'www.example.com.',
        dns.rdatatype.NS: 'ns.example.com.',
        dns.rdatatype.TXT: ('This is a TXT record',),
        dns.rdatatype.SOA: ('ns1.example.com.', 'admin.example.com.', 2023081401, 3600, 1800, 604800, 86400),
    },
    'safebank.com.': { dns.rdatatype.A: '192.168.1.102' },
    'google.com.': { dns.rdatatype.A: '192.168.1.103' },
    'legitsite.com.': { dns.rdatatype.A: '192.168.1.104' },
    'yahoo.com.': { dns.rdatatype.A: '192.168.1.105' },
    'nyu.edu.': { 
        dns.rdatatype.A: '192.168.1.106',
        dns.rdatatype.TXT: (str(encrypted_value),), 
        dns.rdatatype.MX: [(
