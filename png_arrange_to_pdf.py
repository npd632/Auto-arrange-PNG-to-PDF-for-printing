from PIL import Image
from reportlab.lib.pagesizes import A0 #modify based on your needs, preferably A0 for maximum image quality
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import math
import io

# === CONFIGURATION ===
images_folder = r"folder_path_here"   # Path to the folder containing images
output_pdf = "final.pdf"              # Output PDF file name
images_per_page = 16                  # Number of images per page
columns = 4                           # Number of columns
rows = 4                              # Number of rows
padding = 5                           # space between images in points

# === PAGE SETUP ===
page_width, page_height = A0
image_area_width = (page_width - (columns + 1) * padding) / columns
image_area_height = (page_height - (rows + 1) * padding) / rows

# === LOAD IMAGES ===
image_files = [os.path.join(images_folder, f)
               for f in os.listdir(images_folder)
               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_files.sort()  # Optional: sort alphabetically

# === CREATE PDF ===
c = canvas.Canvas(output_pdf, pagesize=A0)

for idx, image_path in enumerate(image_files):
    page_index = idx // images_per_page
    image_index = idx % images_per_page
    col = image_index % columns
    row = image_index // columns

    # New page every 10 images (but not before the first)
    if image_index == 0 and idx != 0:
        c.showPage()

    # Calculate position
    x = padding + col * (image_area_width + padding)
    y = page_height - padding - (row + 1) * (image_area_height + padding)

    # Load and scale image
    img = Image.open(image_path)
    img.thumbnail((image_area_width, image_area_height), resample=Image.LANCZOS)

    # Convert to RGB if needed (for transparency handling)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    img_reader = ImageReader(img_buffer)
    c.drawImage(img_reader, x, y, width=img.width, height=img.height, mask='auto')


# Finalize PDF
c.save()
print(f"PDF created successfully: {output_pdf}")
