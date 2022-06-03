import threading
import requests
import random
import os, sys, time
import json
import random
import names
import time as t
from colorama import Fore, Back, Style
from twocaptcha import TwoCaptcha
from colorama import init
init()

solver = TwoCaptcha("YOUR API NEEDS TO GO HERE")

def check(username):
	while True:
		head = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'none',
			'Sec-Fetch-User': '?1',
			'TE': 'trailers'
		}
		try:
			request = requests.get(url="https://solo.to/" + username, headers=head, timeout=5)
			if not request.text:
				pass
			else:
				return request.status_code
		except:
			pass

def logtofile(file, text):
	f = open(file, "a")
	f.write(str(text)+"\n") 
	f.close()
	return text

def fetchemail():
	emails = ["@gmail.com", "@yahoo.com", "@msn.com"]
	return names.get_first_name().replace(" ", "").lower() + str(random.randint(1,999)) + names.get_last_name().replace(" ", "").lower() + str(random.randint(1,999)) + random.choice(emails)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getheaders(clear, token):
	head = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'TE': 'trailers',
		'Cookie': '_fbp=fb.1.1647730101149.1582414763; cf_clearance=PLACE_YOUR_CF_CLEARANCE_COOKIE_HERE;' + token
	}
	return head

def solve_captcha():
	try:
	    result = solver.recaptcha(
	        sitekey='6LfGz78ZAAAAAH4KtC8CyehsHB3TjNjo0dLXdUAY',
	        url='https://solo.to/register',
	        invisible=1
	    )
	except Exception as e:
	    return "none"
	else:
	    string = str(result)
	    string = string.replace("\'", "\"")
	    y = json.loads(string)
	    print(f"[{Fore.GREEN}+{Fore.WHITE}] Solved Captcha: " + y["code"])
	    return y["code"]

def create(username, password, email):
	attempts = 0
	while True:
		if attempts >= 2:
			print(f"[{Fore.RED}!{Fore.WHITE}] 3 failed attempts, skipping {Fore.CYAN}{username}{Fore.WHITE}")
			break
		else:
			pass

		# Makes first request to obtain: token, valid, name
		req = requests.get(url="https://solo.to/register", headers=getheaders("", ""))
		token = find_between(req.text, 'name="_token" value="', '"')
		valid = find_between(req.text, 'name="valid_from" value="', '"')
		name = "my_name_" + find_between(req.text, '<div id="my_name_', '_wrap')

		if not token:
			print("Could not grab info, make sure your cf_clearance token is correct")
			break
		else:
			# Check if new XSRF Token is needed
			xsrf = find_between(str(req.headers), "XSRF-TOKEN=", ";")
			soloto_session = find_between(str(req.headers), "soloto_session=", "0%3D")

			# Grab new data if needed
			if not xsrf:
				head = getheaders("", "")
			else:
				#print(f"[{Fore.YELLOW}-{Fore.WHITE}] New XSRF-TOKEN: " + xsrf)
				#print(f"[{Fore.YELLOW}-{Fore.WHITE}] New soloto_session: " + soloto_session)

				head = getheaders("", "XSRF-TOKEN=" + xsrf + ";soloto_session=" + soloto_session + "0%3D;")
				req = requests.get(url="https://solo.to/register", headers=head)
				token = find_between(req.text, 'name="_token" value="', '"')
				valid = find_between(req.text, 'name="valid_from" value="', '"')
				name = "my_name_" + find_between(req.text, '<div id="my_name_', '_wrap')
			
			# Output, feel free to delete if yo uwant
			#print(f"[{Fore.YELLOW}-{Fore.WHITE}] Token: " + token)
			#print(f"[{Fore.YELLOW}-{Fore.WHITE}] Valid Code: " + valid)
			#print(f"[{Fore.YELLOW}-{Fore.WHITE}] Name: " + name)

			# Solve captcha woo
			captcha = solve_captcha()

			# Make request to obtain username
			postdata = {
				'_token': token,
				'valid_from': valid,
				name: '',
				'username': username,
				'email': email,
				'password': password,
				'password_confirmation': password,
				'g-recaptcha-response': captcha
			}
			claim = requests.post(url="https://solo.to/register", headers=head, data=postdata, allow_redirects=True)
			#print(claim.text)

			if "The form you're trying to submit has timed out due to inactivity." in claim.text:
				print(f"[{Fore.YELLOW}!{Fore.WHITE}] Captcha failure, form went inactive for some reason")
				attempts += 1
			elif "This process is automatic. Your browser will redirect to your requested content shortly." in claim.text:
				print(f"[{Fore.YELLOW}!{Fore.WHITE}] Cloudflare blocked the request #1 | Delaying 1 minute")
				time.sleep(60)
				attempts += 1
			elif "Checking your browser before accessing" in claim.text:
				print(f"[{Fore.YELLOW}!{Fore.WHITE}] Cloudflare blocked the request #2 | Delaying 1 minute")
				time.sleep(60)
				attempts += 1
			elif "You must wait a few minutes before creating another account." in claim.text:
				print(f"[{Fore.YELLOW}!{Fore.WHITE}] You must wait before creating another account")
				time.sleep(200)
				attempts += 1
			elif "This username is already taken" in claim.text:
				print(f"[{Fore.RED}!{Fore.WHITE}] {Fore.CYAN}{username}{Fore.WHITE} is already taken")
				logtofile("claimed_taken.txt", username)
				break
			elif username == find_between(claim.text, '<div class="dashboard-nav-username">', '</div>'):
				print(f"[{Fore.GREEN}+{Fore.WHITE}] {Fore.CYAN}{username}{Fore.WHITE} created successfully")
				logtofile("claimed.txt", username + "|" + password + "|" + email)
				print(f"[{Fore.GREEN}-{Fore.WHITE}] Waiting 3 minutes before getting another account...")
				time.sleep(180)
				break
			else:
				print(f"[{Fore.RED}+{Fore.WHITE}] Error has occurred [STATUS CODE: {claim.status_code}]")
				break

print(f"{Fore.MAGENTA}SOLO.TO Account Creator{Fore.WHITE}")

with open('available.txt', 'r') as accountfile:
	for username in accountfile:
		username = username.strip().replace("\n", "")
		if check(username) == 404:
			email = fetchemail()
			print(f"{Fore.YELLOW}--------------------------------------------------------------------------{Fore.WHITE}")
			print(f"[{Fore.GREEN}+{Fore.WHITE}] Attemping claim -> {Fore.CYAN}{username}{Fore.WHITE} with {Fore.CYAN}{email}:{username}{username}{Fore.WHITE}")
			create(username, username + username, email)
		else:
			print(f"[{Fore.GREEN}!{Fore.WHITE}] {username} is already taken.")
