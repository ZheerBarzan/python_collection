import pyqrcode
import png
from pyqrcode import QRCode

# String which represent the QR code
name = "https://www.youtube.com/watch?v=QjgpkW2hZyg&list=PLQH2Tb3p5KiI7Ve38Zk_9VOiRacR85k-v&index=1"
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