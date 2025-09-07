# ----- License -------------------------------------------------- # 

#  VaultPass - VaultPass is a local, encrypted password manager built for privacy enthusiasts. Free, open-source, and offline secure.
#  Copyright (c) 2025 - Steven Pereira aka Cursed.

#  This software is an open-source cybersecurity tool developed for
#  penetration testing, threat modeling, and security research. It   
#  is licensed under the MIT License, allowing free use, modification, 
#  and distribution under the following conditions:
#
#  You MUST include this copyright notice in all copies.
#  You MAY use this software for personal or educational purposes ONLY.
#  This software is provided "AS IS," WITHOUT WARRANTY of any kind. 
#  You MAY NOT use this software for any illegal or unauthorized activity.

#  DISCLAIMER:
#  This tool is intended for **educational or ethical testing** purposes only.
#  Unauthorized or malicious use of this software against systems without 
#  proper authorization is strictly prohibited and may violate laws and regulations.
#  The author assumes no liability for misuse or damage caused by this tool.

#  🔗 License: MIT License
#  🔗 Repository: https://github.com/Cursed271
#  🔗 Author: Steven Pereira (@Cursed271)

# ----- Libraries ------------------------------------------------ #

import os
import time
import string
import base64
import hashlib
import sqlite3
import keyring
import pwinput
import secrets
from rich.table import Table
from rich.console import Console
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ----- Global Declaration --------------------------------------- #

console = Console()
salt_value = '6aa2460e7f81b533c3fd4a72e12e7508'

# ----- Database Creation ---------------------------------------- #

def create_database():
	conn = sqlite3.connect("VaultPass.db")
	data = conn.cursor()
	data.execute("""
		CREATE TABLE IF NOT EXISTS accounts (
			id INTEGER PRIMARY KEY,
			website_name TEXT NOT NULL,
			username TEXT NOT NULL,
			encrypted_password TEXT NOT NULL
		)
	""")
	conn.commit()
	conn.close()

# ----- Create Key for Master Password --------------------------- #

def derive_key(password):
	salt_bytes = bytes.fromhex(salt_value)
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt_bytes,
		iterations=1000000,
		backend=default_backend()
	)
	return kdf.derive(password.encode())

# ----- Master Password Setup ------------------------------------ #

def master_key():
	key = keyring.get_password("VaultPass", "MasterKey")
	if key is None:
		console.print(f"[bold red][!] No Master Password Set. Let's set it up: ")
		new_password = pwinput.pwinput("[?] Set the Master Password for the Vault: ")
		keyring.set_password("VaultPass", "MasterKey", new_password)
		return derive_key(new_password)
	else:
		input_password = pwinput.pwinput("[?] Enter the Master Password for the Vault: ")
		if input_password != key:
			console.print(f"[bold red][!] Incorrect Master Password. Exiting.....")
			exit()
		return derive_key(input_password)

# ----- AES Encryption ------------------------------------------- #

def aes_encrypt(plaintext, key):
	iv = os.urandom(16)
	padder = padding.PKCS7(128).padder()
	padded_data = padder.update(plaintext.encode()) + padder.finalize()
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()
	encrypted = encryptor.update(padded_data) + encryptor.finalize()
	return base64.b64encode(iv + encrypted).decode()

# ----- AES Decryption ------------------------------------------- #

def aes_decrypt(encrypted_text, key):
	raw = base64.b64decode(encrypted_text)
	iv = raw[:16]
	ct = raw[16:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()
	padded_plaintext = decryptor.update(ct) + decryptor.finalize()
	unpadder = padding.PKCS7(128).unpadder()
	plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
	return plaintext.decode()

# ----- Refresh -------------------------------------------------- #

def refresh():
	console.print(f"[#C6ECE3][*] Returning to main menu in 5 seconds.....")
	time.sleep(5)
	os.system("cls" if os.name == "nt" else "clear")
	ascii()

# ----- Add Accounts --------------------------------------------- #

def add_accounts(key):
	website = console.input(f"[#C6ECE3][?] Enter the name of the Website: ")
	username = console.input(f"[#C6ECE3][?] Enter the Username of the Website: ")
	password = pwinput.pwinput("[?] Enter the Password of the Website: ")
	encrypted_password = aes_encrypt(password, key)
	conn = sqlite3.connect("VaultPass.db")
	cursor = conn.cursor()
	cursor.execute("INSERT INTO accounts (website_name, username, encrypted_password) VALUES (?, ?, ?)", (website, username, encrypted_password))
	conn.commit()
	conn.close()
	console.print(f"[bold green][✓] Account added successfully.....")
	display_accounts(key)

# ----- Edit Accounts -------------------------------------------- #

def edit_accounts(key):
	display_accounts(key)
	try:
		account_id = int(console.input(f"[#C6ECE3][?] Enter the ID of the account that you want to edit: "))
	except ValueError:
		console.print(f"[bold red][!] Invalid ID Entered. Try Again.....")
		return
	conn = sqlite3.connect("VaultPass.db")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
	result = cursor.fetchone()
	if not result:
		console.print(f"[bold red][!] No account found with that ID.")
		conn.close()
		return
	website = console.input(f"[#C6ECE3][?] Enter the New Website Name (Leave Blank to keep '{result[1]}'): ") or result[1]
	username = console.input(f"[#C6ECE3][?] Enter the New Username (Leave Blank to keep '{result[2]}'): ") or result[2]
	old_decrypted_password = aes_decrypt(result[3], key)
	password = pwinput.pwinput(f"[?] Enter the New Password (Leave Blank to keep the current password): ") or old_decrypted_password
	encrypted_password = aes_encrypt(password, key)
	cursor.execute("UPDATE accounts SET website_name = ?, username = ?, encrypted_password = ? WHERE id = ?", (website, username, encrypted_password, account_id))
	conn.commit()
	conn.close()
	console.print(f"[bold green][✓] Account updated successfully.....")
	display_accounts(key)

# ----- Delete Accounts ------------------------------------------ #

def delete_accounts(key):
	display_accounts(key)
	try:
		account_id = int(console.input(f"[#C6ECE3][?] Enter the ID of the account that you want to DELETE: "))
	except ValueError:
		console.print(f"[bold red][!] Invalid ID Entered. Try Again.....")
		return
	confirm = console.input(f"[#C6ECE3][?] Are you sure you want to delete this account? (y/N): ").lower()
	if confirm != "y":
		console.print(f"[#C6ECE3][*] Deletion aborted!")
		return
	conn = sqlite3.connect("VaultPass.db")
	cursor = conn.cursor()
	cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
	conn.commit()
	conn.close()
	console.print(f"[bold green][✓] Account deleted successfully.....")
	display_accounts(key)

# ----- Display Accounts ----------------------------------------- #

def display_accounts(key):
	conn = sqlite3.connect("VaultPass.db")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM accounts")
	records = cursor.fetchall()
	conn.close()
	if not records:
		console.print(f"[bold red][!] No accounts found.")
		return
	table = Table(title="🔐 Password Vault", show_lines=True, style="bold")
	table.add_column("ID", style="cyan", justify="center")
	table.add_column("Website", style="green")
	table.add_column("Username")
	table.add_column("Password")
	for record in records:
		decrypted_password = aes_decrypt(record[3], key)
		table.add_row(str(record[0]), record[1], record[2], decrypted_password)
	console.print()
	console.print(table)
	console.print()

# ----- Password Generation -------------------------------------- #

def generate_password():
	length = int(console.input(f"[#C6ECE3][?] Enter the minimum length of the Password: "))
	if length < 16:
		console.print(f"[bold red][!] Password must be atleast 16 Characters.")
		return None
	upper = secrets.choice(string.ascii_uppercase)
	lower = secrets.choice(string.ascii_lowercase)
	digit = secrets.choice(string.digits)
	symbol = secrets.choice(string.punctuation)
	remaining_length = length - 4
	all_chars = string.ascii_letters + string.digits + string.punctuation
	remaining = [secrets.choice(all_chars) for _ in range(remaining_length)]
	password_list = list(upper + lower + digit + symbol) + remaining
	secrets.SystemRandom().shuffle(password_list)
	return ''.join(password_list)

# ----- Banner --------------------------------------------------- #

def ascii():
	console.print(rf"""[#C6ECE3]
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                     │
│    oooooo     oooo                       oooo      .   ooooooooo.                                   │ 
│     `888.     .8'                        `888    .o8   `888   `Y88.                                 │     
│      `888.   .8'    .oooo.   oooo  oooo   888  .o888oo  888   .d88'  .oooo.    .oooo.o  .oooo.o     │
│       `888. .8'    `P  )88b  `888  `888   888    888    888ooo88P'  `P  )88b  d88(  "8 d88(  "8     │
│        `888.8'      .oP"888   888   888   888    888    888          .oP"888  `"Y88b.  `"Y88b.      │
│         `888'      d8(  888   888   888   888    888 .  888         d8(  888  o.  )88b o.  )88b     │
│          `8'       `Y888""8o  `V88V"V8P' o888o   "888" o888o        `Y888""8o 8""888P' 8""888P'     │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
	""")
	console.print(rf"[#C6ECE3]+--------------------------------------------------------------+")
	console.print(rf"[#C6ECE3]  VaultPass - Offline Security. Encrypted by Design. Yours Forever.")
	console.print(rf"[#C6ECE3]  Created by [bold black]Cursed271")
	console.print(rf"[#C6ECE3]+--------------------------------------------------------------+")

# ----- Main Function -------------------------------------------- #

if __name__ == "__main__":
	key = master_key()
	os.system("cls" if os.name == "nt" else "clear")
	ascii()
	create_database()
	while True:
		console.print(rf"[#C6ECE3][+] Welcome to VaultPass")
		console.print(rf"[#C6ECE3]    [1] Add Accounts")
		console.print(rf"[#C6ECE3]    [2] Edit Accounts")
		console.print(rf"[#C6ECE3]    [3] Delete Accounts")
		console.print(rf"[#C6ECE3]    [4] View Accounts")
		console.print(rf"[#C6ECE3]    [5] Password Generator")
		console.print(rf"[#C6ECE3]    [6] Exit")
		choice = console.input(rf"[#C6ECE3][?] Select an Option: ")
		if choice == "1":
			add_accounts(key)
			refresh()
		elif choice == "2":
			edit_accounts(key)
			refresh()
		elif choice == "3":
			delete_accounts(key)
			refresh()
		elif choice == "4":
			display_accounts(key)
			refresh()
		elif choice == "5":
			password = generate_password()
			if password:
				console.print(f"[bold green][✓] Generated Password: [bold red]{password}")
		elif choice == "6":
			console.print("[bold red][*] Exiting VaultPass.....")
			break
		else:
			console.print("[bold red][!] Invalid Option Entered. Try Again.....")

# ----- End ------------------------------------------------------ #
