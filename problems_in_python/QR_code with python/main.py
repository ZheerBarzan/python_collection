import pyqrcode
import png
from pyqrcode import QRCode

# String which represent the QR code
name = "www.google.com"

# Generate QR code
url = pyqrcode.create(name)


# create it as a svg file
url.svg("myqr.svg", scale = 8)

# create it as a png file
url.png("myqr.png", scale = 6)

