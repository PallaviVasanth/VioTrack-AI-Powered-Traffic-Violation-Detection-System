import shutil

def create_proof_image(input_image_path, output_image_path):
    """Fast: Just copies original image without drawing."""
    try:
        shutil.copy(input_image_path, output_image_path)
        print(f"[PROOF] Copied → {output_image_path}")
    except Exception as e:
        print("Proof copy error:", e)
