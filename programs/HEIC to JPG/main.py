import os
import zipfile
import tempfile
import shutil
from pathlib import Path
import re
import json


def extract_usdz(usdz_path, temp_dir):
    """Extract USDZ file to temporary directory"""
    try:
        with zipfile.ZipFile(usdz_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return True
    except Exception as e:
        print(f"Error extracting USDZ file: {e}")
        return False


def find_usd_files(temp_dir):
    """Find all USD files in extracted directory"""
    usd_files = []
    for ext in ['*.usd', '*.usda', '*.usdc']:
        usd_files.extend(list(Path(temp_dir).glob(ext)))
    return usd_files


def parse_usda_file(usda_path):
    """Parse ASCII USD file to extract basic geometry data"""
    vertices = []
    faces = []
    normals = []
    uvs = []

    try:
        with open(usda_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract points (vertices)
        points_pattern = r'point3f\[\]\s+points\s*=\s*\[(.*?)\]'
        points_match = re.search(points_pattern, content, re.DOTALL)
        if points_match:
            points_str = points_match.group(1)
            # Parse coordinate tuples
            coord_pattern = r'\(([-\d.e+\-]+),\s*([-\d.e+\-]+),\s*([-\d.e+\-]+)\)'
            coords = re.findall(coord_pattern, points_str)
            for x, y, z in coords:
                vertices.append(f"v {float(x)} {float(y)} {float(z)}")

        # Extract face vertex indices
        face_indices_pattern = r'int\[\]\s+faceVertexIndices\s*=\s*\[(.*?)\]'
        face_indices_match = re.search(face_indices_pattern, content, re.DOTALL)

        face_counts_pattern = r'int\[\]\s+faceVertexCounts\s*=\s*\[(.*?)\]'
        face_counts_match = re.search(face_counts_pattern, content, re.DOTALL)

        if face_indices_match and face_counts_match:
            # Parse face indices
            indices_str = face_indices_match.group(1)
            indices = [int(x.strip()) for x in indices_str.split(',') if x.strip().isdigit()]

            # Parse face counts
            counts_str = face_counts_match.group(1)
            counts = [int(x.strip()) for x in counts_str.split(',') if x.strip().isdigit()]

            # Build faces
            idx = 0
            for count in counts:
                if count >= 3 and idx + count <= len(indices):
                    face_verts = []
                    for i in range(count):
                        face_verts.append(str(indices[idx] + 1))  # OBJ is 1-indexed
                        idx += 1
                    faces.append(f"f {' '.join(face_verts)}")
                else:
                    idx += count

        # Try to extract normals
        normals_pattern = r'normal3f\[\]\s+normals\s*=\s*\[(.*?)\]'
        normals_match = re.search(normals_pattern, content, re.DOTALL)
        if normals_match:
            normals_str = normals_match.group(1)
            normal_coords = re.findall(coord_pattern, normals_str)
            for x, y, z in normal_coords:
                normals.append(f"vn {float(x)} {float(y)} {float(z)}")

        # Try to extract UV coordinates
        uv_pattern = r'texCoord2f\[\]\s+(?:st|primvars:st)\s*=\s*\[(.*?)\]'
        uv_match = re.search(uv_pattern, content, re.DOTALL)
        if uv_match:
            uv_str = uv_match.group(1)
            uv_coord_pattern = r'\(([-\d.e+\-]+),\s*([-\d.e+\-]+)\)'
            uv_coords = re.findall(uv_coord_pattern, uv_str)
            for u, v in uv_coords:
                uvs.append(f"vt {float(u)} {float(v)}")

        return vertices, faces, normals, uvs

    except Exception as e:
        print(f"Error parsing USD file: {e}")
        return [], [], [], []


def convert_usd_to_obj_simple(usd_files, obj_output_path):
    """Convert USD files to OBJ using simple text parsing"""
    all_vertices = []
    all_faces = []
    all_normals = []
    all_uvs = []
    vertex_offset = 0

    for usd_file in usd_files:
        if usd_file.suffix.lower() == '.usda':  # ASCII format
            vertices, faces, normals, uvs = parse_usda_file(usd_file)

            # Add vertices
            all_vertices.extend(vertices)

            # Add faces with vertex offset
            for face in faces:
                face_parts = face.split()
                if len(face_parts) > 1:
                    adjusted_indices = []
                    for i in range(1, len(face_parts)):  # Skip 'f'
                        try:
                            old_idx = int(face_parts[i])
                            new_idx = old_idx + vertex_offset
                            adjusted_indices.append(str(new_idx))
                        except ValueError:
                            adjusted_indices.append(face_parts[i])
                    all_faces.append(f"f {' '.join(adjusted_indices)}")

            # Add normals and UVs
            all_normals.extend(normals)
            all_uvs.extend(uvs)

            vertex_offset += len(vertices)

    # Write OBJ file
    try:
        with open(obj_output_path, 'w') as obj_file:
            obj_file.write("# Converted from USDZ\n")
            obj_file.write("# Generated by Simple USDZ to OBJ Converter\n\n")

            # Write vertices
            for vertex in all_vertices:
                obj_file.write(vertex + '\n')

            # Write normals
            if all_normals:
                obj_file.write('\n')
                for normal in all_normals:
                    obj_file.write(normal + '\n')

            # Write UV coordinates
            if all_uvs:
                obj_file.write('\n')
                for uv in all_uvs:
                    obj_file.write(uv + '\n')

            # Write faces
            if all_faces:
                obj_file.write('\n')
                for face in all_faces:
                    obj_file.write(face + '\n')

        return len(all_vertices) > 0 and len(all_faces) > 0

    except Exception as e:
        print(f"Error writing OBJ file: {e}")
        return False


def convert_usdz_to_obj(input_folder, output_folder):
    """Convert all USDZ files in input folder to OBJ format"""

    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Get all USDZ files
    input_path = Path(input_folder)
    usdz_files = list(input_path.glob('*.usdz')) + list(input_path.glob('*.USDZ'))

    if not usdz_files:
        print(f"No USDZ files found in {input_folder}")
        return

    print(f"Found {len(usdz_files)} USDZ files to convert...")
    print("Using simple text-based parser (no USD library required)")
    print("-" * 60)

    converted_count = 0
    failed_count = 0

    for usdz_file in usdz_files:
        try:
            print(f"Converting: {usdz_file.name}")

            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract USDZ
                if not extract_usdz(usdz_file, temp_dir):
                    print(f"✗ Failed to extract {usdz_file.name}")
                    failed_count += 1
                    continue

                # Find USD files
                usd_files = find_usd_files(temp_dir)
                if not usd_files:
                    print(f"✗ No USD files found in {usdz_file.name}")
                    failed_count += 1
                    continue

                print(f"  Found {len(usd_files)} USD files inside")

                # Generate output filename
                obj_filename = usdz_file.stem + '.obj'
                obj_output_path = Path(output_folder) / obj_filename

                # Convert USD to OBJ
                if convert_usd_to_obj_simple(usd_files, str(obj_output_path)):
                    print(f"✓ Converted: {usdz_file.name} -> {obj_filename}")
                    converted_count += 1
                else:
                    print(f"✗ Failed to convert {usdz_file.name} (no geometry found)")
                    failed_count += 1

        except Exception as e:
            print(f"✗ Error processing {usdz_file.name}: {str(e)}")
            failed_count += 1

    print(f"\nConversion complete!")
    print(f"Successfully converted: {converted_count} files")
    if failed_count > 0:
        print(f"Failed to convert: {failed_count} files")

    if converted_count > 0:
        print(f"\nOBJ files saved to: {output_folder}")
        print("\nNote: This converter extracts basic geometry only.")
        print("Materials and textures are not converted.")


def main():
    print("Simple USDZ to OBJ Converter")
    print("=" * 35)
    print("This version works without USD libraries!")
    print()

    # Configure your paths here
    input_folder = input("Enter the path to your USDZ files folder: ").strip()
    output_folder = input("Enter the path to your output folder: ").strip()

    # Validate input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist!")
        return

    print(f"\nStarting conversion...")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print("-" * 50)

    convert_usdz_to_obj(input_folder, output_folder)


if __name__ == "__main__":
    main()