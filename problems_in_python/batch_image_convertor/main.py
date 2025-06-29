#!/usr/bin/env python3
"""
Image Format Converter to PNG
Converts AVIF, WebP, JPG, JPEG, and other image formats to PNG
"""

import os
from PIL import Image
import argparse
from pathlib import Path
import subprocess
import sys

# Try to import pillow-avif-plugin for AVIF support
try:
    import pillow_avif

    AVIF_SUPPORTED = True
except ImportError:
    AVIF_SUPPORTED = False


def convert_avif_with_ffmpeg(input_file, output_file):
    """
    Convert AVIF to PNG using ffmpeg as fallback
    """
    try:
        subprocess.run([
            'ffmpeg', '-i', str(input_file), '-y', str(output_file)
        ], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_to_png(input_folder, output_folder=None, keep_originals=True):
    """
    Convert all supported image formats in a folder to PNG

    Args:
        input_folder (str): Path to folder containing images
        output_folder (str): Path to output folder (optional, defaults to input_folder + "_png")
        keep_originals (bool): Whether to keep original files
    """

    # Supported formats
    supported_formats = {'.avif', '.webp', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}

    if not AVIF_SUPPORTED:
        print("Warning: AVIF support not available. Will attempt to use ffmpeg as fallback for AVIF files.")

    input_path = Path(input_folder)

    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Set output folder - default to input folder name + "_png"
    if output_folder:
        output_path = Path(output_folder)
    else:
        output_path = input_path.parent / (input_path.name + "_png")

    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Output folder: {output_path}")

    # Get all image files
    image_files = []
    for ext in supported_formats:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))

    if not image_files:
        print("No supported image files found in the specified folder.")
        return

    print(f"Found {len(image_files)} image files to convert.")
    converted_count = 0
    error_count = 0

    for img_file in image_files:
        try:
            # Create output filename
            output_filename = img_file.stem + '.png'
            output_file = output_path / output_filename

            # Skip if file already exists in output folder
            if output_file.exists():
                print(f"Skipping {img_file.name} (PNG already exists in output folder)")
                continue

            # Special handling for AVIF files if Pillow doesn't support them
            if img_file.suffix.lower() == '.avif' and not AVIF_SUPPORTED:
                if convert_avif_with_ffmpeg(img_file, output_file):
                    print(f"✓ Converted (ffmpeg): {img_file.name} → {output_filename}")
                    converted_count += 1

                    # Remove original file if requested
                    if not keep_originals:
                        img_file.unlink()
                        print(f"  Removed original: {img_file.name}")
                else:
                    print(f"✗ Error converting {img_file.name}: AVIF not supported and ffmpeg not available")
                    error_count += 1
                continue

            # Open and convert image with Pillow
            with Image.open(img_file) as img:
                # Convert RGBA or P mode images properly
                if img.mode in ('RGBA', 'LA'):
                    # Keep transparency
                    pass
                elif img.mode == 'P':
                    # Convert palette mode to RGBA to preserve transparency if present
                    if 'transparency' in img.info:
                        img = img.convert('RGBA')
                    else:
                        img = img.convert('RGB')
                elif img.mode not in ('RGB', 'L'):
                    # Convert other modes to RGB
                    img = img.convert('RGB')

                # Save as PNG
                img.save(output_file, 'PNG', optimize=True)

                print(f"✓ Converted: {img_file.name} → {output_filename}")
                converted_count += 1

                # Remove original file if requested
                if not keep_originals:
                    img_file.unlink()
                    print(f"  Removed original: {img_file.name}")

        except Exception as e:
            print(f"✗ Error converting {img_file.name}: {str(e)}")
            error_count += 1

    print(f"\nConversion complete!")
    print(f"Successfully converted: {converted_count} files")
    if error_count > 0:
        print(f"Errors encountered: {error_count} files")


def main():
    parser = argparse.ArgumentParser(description='Convert images to PNG format')
    parser.add_argument('input_folder', help='Path to folder containing images')
    parser.add_argument('-o', '--output', help='Output folder (optional)')
    parser.add_argument('--remove-originals', action='store_true',
                        help='Remove original files after conversion')

    args = parser.parse_args()

    convert_to_png(
        input_folder=args.input_folder,
        output_folder=args.output,
        keep_originals=not args.remove_originals
    )


if __name__ == "__main__":
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow library is required. Install it with:")
        print("pip install Pillow")
        print("For AVIF support, also run:")
        print("pip install pillow-avif-plugin")
        exit(1)

    # If running directly without command line args, ask for folder path
    if len(os.sys.argv) == 1:
        folder_path = input("Enter the path to your image folder: ").strip()
        if folder_path:
            convert_to_png(folder_path)
    else:
        main()