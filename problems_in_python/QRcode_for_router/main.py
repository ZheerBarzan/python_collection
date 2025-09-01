# save as make_wifi_qr.py
# pip install qrcode[pil]

import qrcode

# Given data:
USERNAME = "WiFi-A6-45"      # SSID
PASSWORD = "c3f9vv4mrt"      # Wi-Fi password
SECURITY = "WPA"             # or "WPA2" (use "nopass" if the network is open)
HIDDEN = False               # set True if SSID is hidden

# Wi-Fi QR payload format:
# WIFI:T:<auth>;S:<ssid>;P:<password>;H:<hidden>;;
payload = f"WIFI:T:{SECURITY};S:{USERNAME};P:{PASSWORD};H:{str(HIDDEN).lower()};;"

img = qrcode.make(payload)
img.save("wifi_qr.png")
print("Created wifi_qr.png")
