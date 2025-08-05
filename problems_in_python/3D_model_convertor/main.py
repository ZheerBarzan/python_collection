import os
import argparse
from pxr import Usd, UsdGeom
import trimesh
import numpy as np

def convert_usdz_to_obj(input_filepath, output_dir):

    print(f"Processing '{input_filepath}'...")

    # Extract base name without extension
    base_name = os.path.splitext(os.path.basename(input_filepath))[0]
    output_obj_filepath = os.path.join(output_dir, f"{base_name}.obj")

    try:
        stage = Usd.Stage.Open(input_filepath)
        if not stage:
            print(f"  Error: Could not open USD stage from '{input_filepath}'. Skipping.")
            return False

        all_meshes = []

        # Traverse the USD stage to find all UsdGeomMesh primitives
        for prim in stage.TraverseAll():
            if prim.IsA(UsdGeom.Mesh):
                mesh_prim = UsdGeom.Mesh(prim)

                points = mesh_prim.GetPointsAttr().Get()
                face_vertex_counts = mesh_prim.GetFaceVertexCountsAttr().Get()
                face_vertex_indices = mesh_prim.GetFaceVertexIndicesAttr().Get()

                if points is None or face_vertex_counts is None or face_vertex_indices is None:
                    print(f"    Warning: Skipping mesh '{prim.GetPath()}' due to missing geometry data.")
                    continue

                vertices_np = np.array(points, dtype=np.float32)


                trimesh_faces = []
                current_index = 0
                for count in face_vertex_counts:
                    polygon_indices = face_vertex_indices[current_index : current_index + count]
                    # Simple fan triangulation for polygons with more than 3 vertices
                    if count >= 3:
                        for i in range(1, count - 1):
                            trimesh_faces.append([polygon_indices[0], polygon_indices[i], polygon_indices[i+1]])
                    current_index += count

                if len(trimesh_faces) == 0:
                    print(f"    Warning: No triangulated faces found for mesh '{prim.GetPath()}'. Skipping.")
                    continue

                # Create a trimesh object
                mesh = trimesh.Trimesh(vertices=vertices_np, faces=np.array(trimesh_faces, dtype=np.int32))
                all_meshes.append(mesh)

        if not all_meshes:
            print(f"  No mesh geometry found in '{input_filepath}' to convert to OBJ. Skipping.")
            return False

        # Combine all tri-meshes into a single scene and then export as one OBJ
        # This handles USD files that contain multiple root meshes
        if len(all_meshes) > 1:
            combined_scene = trimesh.Scene(all_meshes)
            # dump(concatenate=True) will merge all meshes into a single Trimesh object
            combined_mesh = combined_scene.dump(concatenate=True)
        else:
            combined_mesh = all_meshes[0]

        # Export to OBJ
        combined_mesh.export(output_obj_filepath)
        print(f"  Successfully converted '{os.path.basename(input_filepath)}' to '{os.path.basename(output_obj_filepath)}'.")
        return True

    except Exception as e:
        print(f"  Error converting '{input_filepath}' to OBJ: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert USDZ files from an input directory to OBJ files in a new output directory.')
    parser.add_argument('input_directory', help='Path to the directory containing USDZ files.')
    parser.add_argument('--output_directory', '-o', default='converted_objs',
                        help='Name of the new directory to store OBJ files. Default is "converted_objs". '
                             'This directory will be created if it does not exist.')

    args = parser.parse_args()

    # Ensure input directory exists
    if not os.path.isdir(args.input_directory):
        print(f"Error: Input directory '{args.input_directory}' does not exist.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_directory, exist_ok=True)
    print(f"Output files will be saved to: '{os.path.abspath(args.output_directory)}'")

    converted_count = 0
    skipped_count = 0

    # Iterate through files in the input directory
    for filename in os.listdir(args.input_directory):
        if filename.lower().endswith('.usdz'):
            input_filepath = os.path.join(args.input_directory, filename)
            if convert_usdz_to_obj(input_filepath, args.output_directory):
                converted_count += 1
            else:
                skipped_count += 1
        else:
            print(f"Skipping non-USDZ file: '{filename}'")

    print("\n--- Conversion Summary ---")
    print(f"Converted: {converted_count} file(s)")
    print(f"Skipped:   {skipped_count} file(s)")
    print(f"Output directory: '{os.path.abspath(args.output_directory)}'")


if __name__ == '__main__':
    main()

