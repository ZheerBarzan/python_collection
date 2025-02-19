from rembg import remove
from PIL import Image

def removeBackground(imagePath, outputPath):
    input_image = Image.open(imagePath).convert("RGBA")  # Ensure correct format
    output = remove(input_image)
    output.save(outputPath, "PNG")
    Image.open(outputPath).show()

removeBackground("nyar.jpeg", "nyar.png")
