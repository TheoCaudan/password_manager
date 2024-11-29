import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Constants
KEY_LENGTH = 32
IV_LENGTH = 16
SALT_LENGTH = 16
ITERATIONS = 100000

# Database connection
def get_db_connection():
    conn = sqlite3.connect('password_manager.db')
    conn.row_factory = sqlite3.Row
    return conn

# Key generation from a password
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt a plaintext message
def encrypt(plaintext, password):
    salt = os.urandom(SALT_LENGTH)
    key = generate_key(password, salt)
    iv = os.urandom(IV_LENGTH)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext).decode()

# Decrypt a ciphertext message
def decrypt(ciphertext, password):
    data = base64.b64decode(ciphertext.encode())
    salt = data[:SALT_LENGTH]
    iv = data[SALT_LENGTH:SALT_LENGTH + IV_LENGTH]
    ciphertext = data[SALT_LENGTH + IV_LENGTH:]
    key = generate_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()
    return plaintext.decode()

# User management functions
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
        (username, generate_password_hash(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
        
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False

def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user['id']
    return None

# Password storage functions
def store_password(user_id, site, site_username, site_password, user_password):
    encrypted_password = encrypt(site_password, user_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (user_id, site, site_username, encrypted_password) VALUES (?, ?, ?, ?)', (user_id, site, site_username, encrypted_password))
    conn.commit()
    conn.close()
    
def retrieve_passwords(user_id, user_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT site, site_username, encrypted_password FROM passwords WHERE user_id = ?', (user_id,))
    user_passwords = cursor.fetchall()
    conn.close()
    decrypted_passwords = []
    for entry in user_passwords:
        decrypted_password = decrypt(entry['encrypted_password'], user_password)
        decrypted_passwords.append({'site': entry['site'], 'username': entry['site_username'], 'password': decrypted_password})
        return decrypted_passwords
    
