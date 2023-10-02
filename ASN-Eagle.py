import requests
import socket
import argparse
from termcolor import colored
import os

# Define your banner text
banner_text = """
 _______  _______  __    _         _______  _______  _______  ___      _______
|   _   ||       ||  |  | |       |       ||   _   ||       ||   |    |       |
|  |_|  ||  _____||   |_| | ____  |    ___||  |_|  ||    ___||   |    |    ___|
|       || |_____ |       ||____| |   |___ |       ||   | __ |   |    |   |___
|       ||_____  ||  _    |       |    ___||       ||   ||  ||   |___ |    ___|
|   _   | _____| || | |   |       |   |___ |   _   ||   |_| ||       ||   |___
|__| |__||_______||_|  |__|       |_______||__| |__||_______||_______||_______|

Version 2.0

Developer: Lucky Samant
"""

# Print Banner for ASN-Eagle
print(colored(banner_text, 'green'))

# Prompt the user for the domain name
domain = input("Enter the domain name to analyze: ")

# Fetch IP address of the website using socket and save it to a variable
ip_addr = socket.gethostbyname(domain)

print(colored("Fetching AS Number for {}..\n".format(domain), 'white'))

# Extract ASN using the ipinfo API.
asn_fetch = requests.get('https://ipinfo.io/' + ip_addr + '/org?token=92eddbd3bbdc0d')

# Fetch the desired result and store it
discovered_asn = asn_fetch.text

print(colored("[+] ASN Details found for {}!!\n".format(domain), 'magenta'))  # Print ASN details
print(colored(discovered_asn, 'yellow'))
access_rights = 0o755  # Defining access rights for creating the output directory.

path = "./output"

# Ask the user if they want to discover IP ranges
ip_ranges = input("Do you want to discover Netblocks/IP ranges (y/n)? ").lower() == 'y'

if ip_ranges:

    # Fetch the AS Number from the previous output
    new_asn = discovered_asn.split(' ')[0]

    print(colored("Fetching IP ranges belonging to AS {}..\n".format(new_asn), 'white'))

    try:
        result = requests.get('https://api.hackertarget.com/aslookup/?q=' + new_asn)  # Makes a request to fetch IP RANGE LIST.
        print(colored("[+] IP ranges found for AS {}!!\n".format(new_asn), 'magenta'))
        print(result.text + '\n')

    except Exception:
        print("There is something wrong.")

# Ask the user if they want to specify an output file
output_file = input("Do you want to specify an output file (y/n)? ").lower() == 'y'

if output_file:
    filename = input("Enter the output file name: ")

    try:  # Creates 'output/' directory and file to save the result containing IP ranges.
        os.mkdir(path, access_rights)

    except OSError:
        print(colored("Output directory already exists, creating a file with IP ranges!", 'green'))

    file = open("./output/" + filename, "w")

    try:
        if ip_ranges:
            file.write(result.text + '\n')  # Write the result with IP ranges in the file
        else:
            file.write(discovered_asn + '\n')  # Write the result without IP ranges in the file
        print(colored("\nResults saved in output/" + filename + '\n', 'blue'))

    except Exception:
        print(colored("Task failed! Try again!", 'red'))
