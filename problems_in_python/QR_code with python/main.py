import pyqrcode
import png
from pyqrcode import QRCode

# String which represent the QR code
name = "https://itd.auis.edu.krd/reset-password/"
try:
    # Generate QR code
    url = pyqrcode.create(name)
    # create it as a svg file
    url.svg("myqr.svg", scale = 8)
    # create it as a png file
    url.png("myqr.png", scale = 6)
    print("QR code generated successfully")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please try again")