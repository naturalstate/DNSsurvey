import dns
import dns.resolver
import socket

domains = {}
subdomains = "dns_servers.txt"

res = dns.resolver.Resolver()
res.nameservers = ['1.1.1.1']
res.port = 53

print(r"""\
    ____  _   _______    _____                            
   / __ \/ | / / ___/   / ___/__  ________   _____  __  __
  / / / /  |/ /\__ \    \__ \/ / / / ___/ | / / _ \/ / / /
 / /_/ / /|  /___/ /   ___/ / /_/ / /   | |/ /  __/ /_/ / 
/_____/_/ |_//____/   /____/\__,_/_/    |___/\___/\__, /  
                                                 /____/  

""")

domain = input("Enter the domain to scan: ")
nums = True

def ReverseDNS(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return []

def DNSLookup(domain):
    ips = []
    try:
        result = res.resolve(domain)
        if result:
            addresses = [a.to_text() for a in result]
            if domain in domains:
                domains[domain] = list(set(domains[domain]+addresses))
            else:
                domains[domain] = addresses
            for a in addresses:
                rd = ReverseDNS(a)
                for d in rd:
                    if d not in domains:
                        domains[d] = [a]
                        DNSLookup(d)
                    else:
                        domains[d] = [a]
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips

def HostSearch(domain, dictionary,nums):
    successes = []
    for word in dictionary:
        d = word+"."+domain
        DNSLookup(d)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSLookup(s)

#use subdomains.txt as base domains to search
dictionary = []
with open(subdomains,"r") as f:
    dictionary = f.read().splitlines()
HostSearch(domain,dictionary,nums)
for domain in domains:
    print("%s: %s" % (domain, domains[domain]))

