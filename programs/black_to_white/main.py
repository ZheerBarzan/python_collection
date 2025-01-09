from PIL import Image

# Load the image
image_path = '/Users/zheer/Desktop/medusa.jpg'  # Replace with your image file path
image = Image.open(image_path)

# Convert the image to grayscale (just in case it's not already in black and white)
image = image.convert('L')

# Invert the image
inverted_image = Image.eval(image, lambda x: 255 - x)

# Save the inverted image
inverted_image_path = 'inverted_image.jpg'  # Replace with the desired output file path
inverted_image.save(inverted_image_path)

print(f"Inverted image saved as {inverted_image_path}")
