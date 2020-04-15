from mitmproxy import http
from Crypto.Cipher import AES
import json
import requests
import winreg
import base64
import zlib

KEY = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
    0,
    winreg.KEY_WRITE
)

def enable_proxy():
    winreg.SetValueEx(KEY, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(KEY, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8080")

def disable_proxy():
    winreg.SetValueEx(KEY, "ProxyEnable", 0, winreg.REG_DWORD, 0)

def verify_session(session):
    print(requests.post(
        "https://latest.live.dbd.bhvronline.com/api/v1/clientVersion/check",
        json={
        	"shortVersion": "gABAC7ps70O7AIQpTyDat2oXiesXt9MfXTwF4N+JuJ2bPtVLgUTNoScQqOCPG6t5YuQKkwfPeT6wT38PgeSZneZYeWtbfLVugRnnL/TbeS69utpJ6LXRYfX++4/AYQZ/6vurmRBop30Ss+QhizqLsZ0p7t3p7C6mAbULpI8MWkLu/NwmwgBKCg6Q6RzvjL+yUJWZNwZCOobiFwCLtla7yLjfXs93NJqny8UkFeIHbM4HOiUw19+aERrCvkYRgiOAfl7UVT3hISabVjj9I3XXOki+Ax45FT/mIygwrOwj3RpKPCx8a7/N4rEULj17etYFZWxAK6gi02gtgctP01G0Kg==",
        	"longVersion": "fdNyatrP2l9g4EtW6S/FPsymfTGs6AjtgJi0vdLc3eCFLBBVd20gaTSC2JgKVsmx+r8sphoAraxWYT5hkMylKAlmC+7o2ZXILhLWSdOrFWqhs7gYlSXc/+6gaLOZ4fYC4m42hRLekInZL1ikIdzab6cvdbVdvmCNSWeaR9fXSRM+KKNFl9RagD5ZKOh2vFCDV1xquol2Wq+y5Q7LCBpqtvppQ59YimbtjZoaFHPVVIbaxFyhueelqe02IOOC4OWD9Kmtj7WmbGpekcMJRhdjz/NDmnJc1tmy4U5VvgnVwmC8o+plQtcLIFvpFKpKm6bkAnyiXCdy9puQe/X8S2kV6Q=="
        },
        headers={
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Accept-Encoding": "deflate, gzip"
        },
        cookies={
            "bhvrSession": session
        },
        verify=False
    ).json())

def request(flow: http.HTTPFlow) -> None:
    """print(f"===================== START: {flow.request.url}")
    print(flow.request.headers)
    print(flow.request.content.decode())
    print(f"===================== END:   {flow.request.url}")"""

    if "bhvr" in flow.request.host:
        print(f"===================== START: {flow.request.url}")
        print(flow.request.headers)
        print(flow.request.content.decode())
        print(f"===================== END:   {flow.request.url}")

        if "steam/login" in flow.request.url:
            print(flow.request.url)
            """flow.request.text = json.dumps({
                "clientData": {
                    "catalogId": "3.6.0_281460live",
                    "consentId": "3.6.0_281460live"
                }
            })"""
            print(flow.request.headers)
            print(flow.request.cookies)
            print(flow.request.content)
        
        if "FullProfile/binary" in flow.request.url:
            print(flow.request.url)
            print(flow.request.headers)
            print(flow.request.cookies)
            print(flow.request.content)
        
        if "/store/getAvailableBundles" in flow.request.url:
            print(flow.request.url)
            print(flow.request.headers)
            print(flow.request.cookies)
            print(flow.request.content)
            """disable_proxy()
            verify_session(flow.request.cookies["bhvrSession"])
            enable_proxy()"""

def response(flow: http.HTTPFlow) -> None:
    """print(flow.request.url)
    print(f"===================== START: {flow.request.url}")
    print(flow.response.headers)
    print(flow.response.content.decode())
    print(f"===================== END:   {flow.request.url}")"""

    if "bhvr" in flow.request.host:
        print(flow.request.url)
        print(f"===================== START: {flow.request.url}")
        print(flow.response.headers)
        print(flow.response.content.decode())
        print(f"===================== END:   {flow.request.url}")

        if "contentVersion/version" in flow.request.url:
            print(flow.request.url)
            """response = json.loads(flow.response.content.decode())
            response["availableVersions"]["3.0.0.13"] = "3.0.0.13-1561474922"
            response["availableVersions"]["3.0.0.16"] = "3.0.0.16-1562079672"
            response["availableVersions"]["3.0.0.4"] = "3.0.0.4-1560778720"
            flow.response.text = json.dumps(response)"""
            print(json.loads(flow.response.content.decode()))
            print(flow.response.headers)
            print(flow.response.content)
        
        if "steam/login" in flow.request.url:
            print(flow.request.url)
            print(flow.response.headers)
            print(flow.response.content)
            bhvrSession = flow.response.headers["Set-Cookie"].split("bhvrSession=")[1].split(";")[0]
            print(f"bhvrSession: {bhvrSession}")

            with open("session.json", "w") as file:
                json.dump({
                    "bhvrSession": bhvrSession
                }, file)
        
        if "FullProfile/binary" in flow.request.url:
            print(flow.request.url)
            print(flow.response.headers)
            print(flow.response.content.decode())

            cipher = AES.new(b"5BCC2D6A95D4DF04A005504E59A9B36E", AES.MODE_ECB)
            profile = flow.response.content.decode()[8:]
            profile = base64.b64decode(profile)
            profile = cipher.decrypt(profile)
            profile = "".join([chr(c + 1) for c in profile]).replace("\u0001", "")
            profile = base64.b64decode(profile[8:])
            profile = profile[4:len(profile)]
            profile = zlib.decompress(profile).decode("utf16")
            profile = json.loads(profile)
            print(profile)

            with open("profile.json", "w") as file:
                json.dump(profile, file)

        if "/getUrl" in flow.request.url:
            print(flow.request.url)
            print(flow.response.headers)
            print(flow.response.content.decode())

            response = json.loads(flow.response.content.decode())
            print(f"RTM: {response['url']}")

            with open("rtm.json", "w") as file:
                json.dump({
                    "url": response["url"]
                }, file)


enable_proxy()