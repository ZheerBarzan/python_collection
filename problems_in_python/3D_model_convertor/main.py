import os
import argparse
from pxr import Usd, UsdGeom

# For FBX export
try:
    from pxr import UsdFbx
except ImportError:
    print("Warning: UsdFbx module not found. FBX export will not be available.")

# For STL export
try:
    import trimesh

    stl_export_available = True
except ImportError:
    print("Warning: trimesh module not found. STL export will not be available.")
    stl_export_available = False


def convert_usdz_to_obj(input_file, output_file):
    """Convert USDZ file to OBJ format"""
    # The USD library has built-in OBJ export
    stage = Usd.Stage.Open(input_file)

    # Export to OBJ
    UsdGeom.PointInstancer.ExportPointInstancerToOBJ(stage, output_file)
    print(f"Exported to OBJ: {output_file}")


def convert_usdz_to_fbx(input_file, output_file):
    """Convert USDZ file to FBX format"""
    # Check if UsdFbx is available
    if "UsdFbx" not in globals():
        print("FBX export not available. Please install the USD FBX plugin.")
        return False

    # Open the USD stage
    stage = Usd.Stage.Open(input_file)

    # Export to FBX
    UsdFbx.WriteFbx(output_file, stage)
    print(f"Exported to FBX: {output_file}")
    return True


def convert_usdz_to_stl(input_file, output_file):
    """Convert USDZ file to STL format using trimesh"""
    if not stl_export_available:
        print("STL export not available. Please install trimesh.")
        return False

    # First, convert to OBJ as an intermediate format
    temp_obj = os.path.splitext(output_file)[0] + "_temp.obj"
    convert_usdz_to_obj(input_file, temp_obj)

    # Load the OBJ with trimesh and export to STL
    mesh = trimesh.load(temp_obj)
    mesh.export(output_file)

    # Clean up the temporary file
    os.remove(temp_obj)
    print(f"Exported to STL: {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Convert USDZ files to OBJ, FBX, or STL formats')
    parser.add_argument('input_file', help='Input USDZ file')
    parser.add_argument('output_format', choices=['obj', 'fbx', 'stl'], help='Output format')
    parser.add_argument('--output', '-o', help='Output file name (optional)')

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} does not exist")
        return

    if not args.input_file.lower().endswith('.usdz'):
        print(f"Warning: Input file {args.input_file} does not have .usdz extension")

    # Determine output file name
    if args.output:
        output_file = args.output
    else:
        base_name = os.path.splitext(args.input_file)[0]
        output_file = f"{base_name}.{args.output_format}"

    # Perform conversion
    if args.output_format == 'obj':
        convert_usdz_to_obj(args.input_file, output_file)
    elif args.output_format == 'fbx':
        convert_usdz_to_fbx(args.input_file, output_file)
    elif args.output_format == 'stl':
        convert_usdz_to_stl(args.input_file, output_file)


if __name__ == '__main__':
    main()