import os
from PIL import Image
import pillow_heif
from pathlib import Path


def convert_heic_to_jpg(input_folder, output_folder, quality=90):
    """
    Convert all HEIC images in input_folder to JPG format in output_folder

    Args:
        input_folder (str): Path to folder containing HEIC images
        output_folder (str): Path to folder where JPG images will be saved
        quality (int): JPG quality (1-100, default 90)
    """

    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()

    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Get all HEIC files
    input_path = Path(input_folder)
    heic_files = list(input_path.glob('*.heic')) + list(input_path.glob('*.HEIC'))

    if not heic_files:
        print(f"No HEIC files found in {input_folder}")
        return

    print(f"Found {len(heic_files)} HEIC files to convert...")

    converted_count = 0
    failed_count = 0

    for heic_file in heic_files:
        try:
            # Open HEIC image
            with Image.open(heic_file) as img:
                # Convert to RGB if necessary (HEIC can have different color modes)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Generate output filename
                jpg_filename = heic_file.stem + '.jpg'
                output_path = Path(output_folder) / jpg_filename

                # Save as JPG
                img.save(output_path, 'JPEG', quality=quality, optimize=True)

                print(f"✓ Converted: {heic_file.name} -> {jpg_filename}")
                converted_count += 1

        except Exception as e:
            print(f"✗ Failed to convert {heic_file.name}: {str(e)}")
            failed_count += 1

    print(f"\nConversion complete!")
    print(f"Successfully converted: {converted_count} files")
    if failed_count > 0:
        print(f"Failed to convert: {failed_count} files")


def main():
    # Configure your paths here
    input_folder = input("Enter the path to your HEIC images folder: ").strip()
    output_folder = input("Enter the path to your output folder: ").strip()

    # Validate input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist!")
        return

    # Optional: Ask for quality setting
    quality_input = input("Enter JPG quality (1-100, default 90): ").strip()
    try:
        quality = int(quality_input) if quality_input else 90
        quality = max(1, min(100, quality))  # Clamp between 1-100
    except ValueError:
        quality = 90
        print("Invalid quality input, using default (90)")

    print(f"\nStarting conversion...")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Quality: {quality}")
    print("-" * 50)

    convert_heic_to_jpg(input_folder, output_folder, quality)


if __name__ == "__main__":
    main()