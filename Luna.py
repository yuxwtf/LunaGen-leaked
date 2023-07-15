import requests
from colorama import Fore
import sys, os
from tls_client import Session
import threading, json
import time, random, colorama, ctypes
from pystyle import Write, Colors, Center

colorama.init(convert=True)
unlocked = 0; locked = 1; captchas = 0; count = 0; gen_start = time.time()

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
xtrack = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
os.system("cls") if os.name == "nt" else os.system("clear")
ctypes.windll.kernel32.SetConsoleTitleW(f'Luna Gen | Unlock Rate: {round(count/(count+locked)*100)}% | unlocked: {unlocked} | locked: 0 | {round(count / ((time.time() - gen_start) / 60))}/m')
lock = threading.Lock()
config = json.load(open('./config/config.json', encoding="utf-8"))

def payload(proxy:str=None, user_agent:str=None) -> None:
    p = {
        "clientKey":config["capsolver_api_key"],
        "task": {
            "websiteURL":"https://discord.com/",
            "websiteKey":"4c672d35-0701-42b2-88c3-78380b0db560",
        }
    }
    p['appId']="855C85D8-89FF-4358-A3A0-3A91AC8D4E5F"
    p['task']['type'] = "HCaptchaTurboTask"
    p['task']['proxy'] = proxy 
    p['task']['userAgent'] = user_agent
    return p

def solve_captcha(proxy,ua):
    r = requests.post(f"https://api.capsolver.com/createTask",json=payload(proxy,ua))
    try:
        if r.json().get("taskId"):
            taskid = r.json()["taskId"]
        else:
            return "failed"
    except:
        return "failed"
    while True:
        try:
            r = requests.post(f"https://api.capsolver.com/getTaskResult",json={"clientKey":config["capsolver_api_key"],"taskId":taskid})
            if r.json()["status"] == "ready":
                key = r.json()["solution"]["gRecaptchaResponse"]
                print(f"({Fore.LIGHTRED_EX}~{Fore.WHITE}) Solved ({Fore.YELLOW}{key[:40]}.{Fore.WHITE})", flush=True)
                return key
            elif r.json()['status'] == "failed":
                return "failed"
        except:
            return "failed"

class Generator:
    def __init__(self, headers=None) -> None:
        self.headers = headers
        self.tls_session = Session(
            client_identifier="chrome_114",
            pseudo_header_order=[":authority",":method",":path",":scheme"],
            header_order=["accept","accept-encoding","accept-language","user-agent"],
            random_tls_extension_order=True
        )
        try:
            self.proxies = random.choice(open('input/proxies.txt', 'r', encoding="utf-8").read().splitlines())
        except:
            print(f"\n  ({Fore.RED}-{Fore.WHITE}) Insufficient proxies.")
            time.sleep(5)
            sys.exit()
        self.proxy = {
            "http": "http://"+self.proxies,
            "https": "http://"+self.proxies
        }
        self.client_build = 198318

    def cprint(self, use_case, content):
        lock.acquire()
        if use_case == 'SUCCESS':
            print(f"({Fore.GREEN}${Fore.WHITE}) {content}", flush=True)
        if use_case == 'INFO':
            print(f"({Fore.BLUE}~{Fore.WHITE}) {content}", flush=True)
        if use_case == 'ERROR':
            print(f"({Fore.RED}-{Fore.WHITE}) {content}", flush=True)
        if use_case == 'WARN':
            print(f"({Fore.YELLOW}!{Fore.WHITE}) {content}", flush=True)
        lock.release()

    def reg_disc(self, invite) -> None:
        global count
        global unlocked
        global locked
        session = self.tls_session

        header = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ua,
            'x-track': xtrack,
        }
        try:
            name = random.choice(open('input/names.txt', 'r', encoding="utf-8").read().splitlines())
        except:
            print(f"\n  ({Fore.RED}-{Fore.WHITE}) Insufficient names.")
            time.sleep(5)
            sys.exit()

        try:
            cookie = requests.get("https://discord.com/", headers=header).cookies.get_dict()
        except:
            self.cprint("ERROR", "Cookie cant be extracted from request http://discord.com/app.")

        try:
            fingerprint = requests.get("https://discord.com/api/v9/experiments", headers=header).json()["fingerprint"]
        except:
            self.cprint("ERROR", "Fingerprint can't be extracted from request.")

        capKey = solve_captcha("http://"+self.proxies,ua)

        if invite == "" or None:
            payload = {
                "fingerprint": fingerprint,
                "consent": True,
                "username": name,
                "captcha_key": capKey,
            }
        else:
            payload = {
                "fingerprint": fingerprint,
                "consent": True,
                "username": name,
                "invite": invite,
                "captcha_key": capKey,
            }
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'Connection': 'keep-alive',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': ua,
            'x-fingerprint': fingerprint,
            'x-track': xtrack,
        }
        try:
            try:
                response = session.post('https://discord.com/api/v9/auth/register', headers=headers, cookies=cookie, json=payload)
                if 'token' not in response.text:
                    self.cprint("ERROR", "Can't generate token")
                    return "failed"
            except Exception as e:
                return self.cprint("WARN", "%s"%e)
        except requests.exceptions.ProxyError as er:
            return self.cprint("ERROR", f"{er}")
        
        token = response.json().get('token')

        checker = requests.get("https://discord.com/api/v10/users/@me/library", headers={"Authorization": token})

        if checker.status_code != 200:
            self.cprint("WARN", f"Locked {token}")
            locked+=1
            return "locked token"
        
        self.cprint("SUCCESS", "Generated {}".format(token))
        unlocked+=1
        count+=1
        ctypes.windll.kernel32.SetConsoleTitleW(f'Luna Gen | Unlock Rate: {round(count/(count+locked)*100)}% | locked {locked} | unlocked {unlocked} | {round(count / ((time.time() - gen_start) / 60))}/m')

        with open("tokens.txt", "a", encoding='utf-8') as f:
            f.write(f"{token}\n")

    def __thread__(self, threads, invite):
        self.tls_session.proxies = "http://"+self.proxies
        if threading.active_count() < int(threads):
            threading.Thread(target=self.reg_disc, args=(invite,)).start()

if __name__ == "__main__":
    auth = "WyI1MzgyMzUyNyIsIjNIbWZGYlh3VUZwKzg1eFk0Z0lEZUljSDRpRVE1YW1JWXd6bzlPVHoiXQ=="
    RSAPubKey = "<RSAKeyValue><Modulus>vQ+uH3kNCEb50QhU6y2VFIfkF+f2AIVNzNPNQyAmlww0OA0gy+6R2HJGHt19fZUz9JAGAn/VDI7xkp4uuEmlmA7bEsYFxAQdfC3+oVdAywr2oPLpyTPztRHSLw/93bm+icGx1o0pgkoft+BCLAjX10TQ27A/3aZnWc+YgWVCh4u9zjUwwMpHKnKQ857LNMDtcAB44JKPgH44dA0E7lQHWzM6XTCcHX1xNr9LInoClhD+zEo3FS0BrMBf+oYqwL2NkwTebPKefltpb4B0nP4/4/Jw+6z0aZ1L4koHbRJG+xt/7uqvHEmwr2Z//sgm6ncZ2ykxBkQRf2LZXv8dfyWN6w==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    logo = """
    ██▓     █    ██  ███▄    █  ▄▄▄           
    ▓██▒     ██  ▓██▒ ██ ▀█   █ ▒████▄        
    ▒██░    ▓██  ▒██░▓██  ▀█ ██▒▒██  ▀█▄    
    ▒██░    ▓▓█  ░██░▓██▒  ▐▌██▒░██▄▄▄▄██    
    ░██████▒▒▒█████▓ ▒██░   ▓██░ ▓█   ▓██▒   
    ░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒▒   ▓▒█░  
    ░ ░ ▒  ░░░▒░ ░ ░ ░ ░░   ░ ▒░  ▒   ▒▒ ░   
    ░ ░    ░░░ ░ ░    ░   ░ ░   ░   ▒     
        ░  ░   ░              ░       ░  ░  

               cracked by @yux
    """
    Write.Print(Center.XCenter(logo), Colors.red_to_blue, interval=0.000)
    max_threads = int(Write.Input("\n   Threads <3 ", Colors.red_to_blue, interval=0.0025))
    os.system("cls") if os.name == "nt" else os.system("clear")
    Write.Print(Center.XCenter(logo), Colors.red_to_blue, interval=0.000)
    invite = Write.Input("\n   Invite <3 ", Colors.red_to_blue, interval=0.0025)
    os.system("cls" if os.name == "nt" else "clear")
    Write.Print(Center.XCenter(logo), Colors.red_to_blue, interval=0.000)

    license_key = "niggerman"

    print("\n")
    try:
        while True:
            Generator().__thread__(max_threads+1, invite)
    except KeyboardInterrupt:
        sys.exit()