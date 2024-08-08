#Tests Connection to eGauge energy meters
#Replace URI with other meter names to test different meters


import sys

from egauge import webapi

URI = "https://egauge20975.egaug.es"      # replace DEV with meter name
USR = "USER"                      # replace USER with user name
PWD = "PASS"                      # replace PASS with password

dev = webapi.device.Device(URI, webapi.JWTAuth(USR,PWD))

print("hostname is " + dev.get("/config/net/hostname")["result"])


# verify we can talk to the meter:
try:
    rights = dev.get("/auth/rights").get("rights", [])
except webapi.Error as e:
    print(f"Sorry, failed to connect to {URI}: {e}")
    sys.exit(1)

print(f"Using meter {URI} (user {USR}, rights={rights})")


