import os
from PIL import Image, ImageOps

# === CONFIGURATION ===
input_folder = "C:\\Users\\FPT\\Downloads\\drive-download-20250807T123851Z-1-001"
output_folder = "C:\\Users\\FPT\\Documents\\Python\\VIT\\output"
logo_path = "C:\\Users\\FPT\\Documents\\Python\\VIT\\logo.png"

# Load the logo once
logo_original = Image.open(logo_path).convert("RGBA")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each JPG in the folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".jpg"):
        img_path = os.path.join(input_folder, filename)
        image = Image.open(img_path).convert("RGBA")
        image = ImageOps.exif_transpose(image)  # ✅ Fix orientation

        width, height = image.size

        # Determine shorter side
        shorter_side = min(width, height)

        # Get original logo dimensions
        logo_w, logo_h = logo_original.size
        logo_ratio = logo_w / logo_h

        # Calculate shorter side of photo and target logo height
        shorter_side = min(width, height)
        target_logo_h = int(shorter_side / 7)
        target_logo_w = int(target_logo_h * logo_ratio)

        # Resize the logo proportionally
        logo_resized = logo_original.resize((target_logo_w, target_logo_h), Image.LANCZOS)
        margin = int(target_logo_w / 7)


        # Paste logo onto image
        image.paste(logo_resized, (margin, margin), logo_resized)

        # Save final image as JPG (remove alpha channel)
        final_image = image.convert("RGB")
        output_path = os.path.join(output_folder, filename)
        final_image.save(output_path, "JPEG", quality=95)

print("✅ All images processed and saved.")
