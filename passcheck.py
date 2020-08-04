import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_char)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the api and try again")
    return res

def get_password_leaks_count(hashs, hash_to_check):
    hashs_count_split = (line.split(':') for line in hashs.text.splitlines())
    for h, count in hashs_count_split:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password: str) -> str:
    sha256password = hashlib.sha1(password.encode('UTF_8')).hexdigest().upper()
    # unpacking pass
    first5character, tail = sha256password[:5], sha256password[5:]
    response = request_api_data(first5character)
    return get_password_leaks_count(response, tail)


def main(args):
    file_with_passwords = args[0]
    try:
        with open(file_with_passwords, 'r') as f:
            passwords_list = f.readlines()
            for password in passwords_list:
                count = pwned_api_check(password.strip())
                if count:
                    print(f"Your password {password.strip()} was hacked {count} time{'' if count == 1 else 's'}")
                else:
                    print("Password was not hached")
        return "done"

    except FileNotFoundError as er:
            print('Second try -> file does not exist in this funny library', er)


    # !!!!!!! ================== DANGER NOT SAFETY METHOD ==================== Use this for writes passwords in script arguent 
    # for password in args:
    #     count = pwned_api_check(password)
    #     if count:
    #         print(f"Your password {password} was hacked {count} time{'' if count == 1 else 's'}")
    #     else:
    #         print("Password was not hached")
    # return "done"

if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))