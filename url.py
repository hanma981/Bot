import os
import re
import socket
import requests
import base64
import urllib3

# Warning များကို ပိတ်ထားရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

g = "\033[1;32m"
y = "\033[1;33m"
r = "\033[1;31m"
w = "\033[1;00m"
c = "\033[1;36m"

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def get_gateway_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        parts = ip.split('.')
        parts[-1] = '1'
        return '.'.join(parts)
    except:
        return "192.168.110.1"

def fetch_portal():
    clear()
    print(f"{g}======================================{w}")
    print(f"{c}  Ruijie Auto-Catcher (API Version)   {w}")
    print(f"{g}======================================{w}\n")

    print(f"{y}[*] ကျေးဇူးပြု၍ Ruijie Wi-Fi နှင့် ချိတ်ဆက်ထားပါ။{w}")
    print(f"{y}[*] အင်တာနက် မပွင့်သေးကြောင်း သေချာပါစေ။{w}\n")

    gateways = [get_gateway_ip(), "192.168.110.1", "192.168.0.1", "10.44.77.254"]
    gateways = list(dict.fromkeys(gateways)) 

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        'Accept': '*/*'
    }

    portal_url = None

    for gw in gateways:
        target = f"http://{gw}"
        print(f"{c}[*] Intercepting Router Gateway: {target}...{w}")
        try:
            res = requests.get(target, headers=headers, timeout=5, allow_redirects=True)

            if "portal-as.ruijienetworks.com" in res.url:
                portal_url = res.url
                break

            match = re.search(r"href=['\"](.*?)['\"]", res.text)
            if match and "portal-as.ruijienetworks.com" in match.group(1):
                extracted = match.group(1)
                if extracted.startswith("http"):
                    portal_url = extracted
                else:
                    portal_url = "https://portal-as.ruijienetworks.com" + extracted
                break

        except requests.exceptions.RequestException:
            print(f"{r}[-] No response from {gw}{w}")

    if not portal_url:
        print(f"{c}[*] Trying global HTTP Intercept...{w}")
        try:
            res = requests.get("http://httpbin.org/get", headers=headers, timeout=5)
            if "portal-as.ruijienetworks.com" in res.url:
                portal_url = res.url
            else:
                match = re.search(r"href=['\"](.*?)['\"]", res.text)
                if match and "portal-as.ruijienetworks.com" in match.group(1):
                    portal_url = match.group(1)
        except:
            pass

    if portal_url:
        api_url = portal_url.replace("/auth/wifidogAuth/login/?", "/api/auth/wifidog?stage=portal&")
        api_url = api_url.replace("/auth/wifidogAuth/login?", "/api/auth/wifidog?stage=portal&")

        print(f"\n{g}[✓] PORTAL URL အောင်မြင်စွာ ဖမ်းယူရရှိပါပြီ!{w}")
        print(f"{g}[✓] API လမ်းကြောင်းသို့ အလိုအလျောက် ပြောင်းလဲပြီးပါပြီ!{w}")
        print(f"{y}-{w}"*50)
        print(f"{w}{api_url}{w}")
        print(f"{y}-{w}"*50)

        b64_url = base64.b64encode(api_url.encode()).decode()
        print(f"\n{c}[*] Script ထဲထည့်ရန် API Base64 Code:{w}")
        print(f"{g}{b64_url}{w}\n")
    else:
        print(f"\n{r}[❌] Portal URL ကို ဖမ်းမမိပါ။ အင်တာနက် ပွင့်နေသလား ပြန်စစ်ပါ။{w}")

if __name__ == '__main__':
    try:
        fetch_portal()
    except KeyboardInterrupt:
        print(f"\n\n{r}[!] Exiting...{w}")