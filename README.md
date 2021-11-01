# 1. Introduction

Moving Target Defence (MTD) is an active defence principle that is focued on dynamic attack surface modifications.

The following project is a POC that shows how the MTD could be applied.

# 2. How does it work?
Implementation of MTD based mechanism consists of the following questions' answers:
- What?
- How?
- When?

First answer specifies what part of attack surface will be dymanicaly modified. \
Second answer specifies how the dynamic modifications will be applied. \
Third answer specifies when the dynamic modification will be applied.

Presented solution consists of the following answers:
- What? - services` location (port numbers).
- How? - nftables rules application that properly redirect network traffic. 
- When? - every T seconds, where ```L <= T <= U```, L and U are passed at program startup.


# 3. Program startup

To test the solution two virtual machine are required. First machine is the one that uses MTD solution. \
The latter one is the attacker machine. First machine configuration requires the attacker machine ip address, so it is good to setup attacker machine first.

## 3.1 First machine - MTD solution

First machine should perform following:
- clone repo,
- install nftables, pip and python requirements,
- setup config file, 
- run redis,
- run MTD solution,
- run proactive MTD launcher. 

### 3.1.1 Install nftables, pip and python requirements

Open terminal and run:
```
apt-get update &&
    apt-get install python3-pip && 
    apt-get install nftables &&
    apt-get install python3-nftables
```

Then run the following:
```
pip3 install -r requirements.txt
```
### 3.1.2 Setup config file
Change ip address in config file (/src/configs/setup/configuration.json, path: mtd_controller_configuration/watched_addresses/address) to the attacker machine ip address.
Then specify all currently open ports (for now tcp only and port number <= 1050 - as in the config file) in mtd_controller_configuration/all_used_ports. Lastly in mtd_controller_configuration/watched_addresses/ports_to_ignore specify the ports that should not be moved.

### 3.1.3 Run redis
Open terminal and run:
```
docker-compose up -d
```

### 3.1.4 Run MTD solution
Open terminal and run:
```
python3 -m src.main
```
### 3.1.5 Run proactive MTD launcher
Open terminal and run:
```
python3 -m proactive-launcher.main -l 5 -u 10
```
Flags "-l" and "-u" mean the lower and upper boundary for next nftables rules generation delay. Above 5 and 10 values mean that the port moves every T seconds, where T is randomly chosen from [5,10].

## 3.2 Second machine - attacker

Second machine requires the nmap tool installed.

Open terminal and run:
```
apt-get update && apt-get install nmap
```

# 4. Test solution
Run test scan against the target machine, i.e. MTD solution machine. Simple SYN Scan looks like this:
```
nmap <first_machine_ip> -sS -p1-10000
```
Execute SYN scan few times and see, that not ignored ports are moving.
It should work as well for Connect (-sT), XMAS (-sX), FIN (-sF) and NULL (-sN) scans as well.
It is also possible that the scan results will show less open ports than currently open on the target machine.