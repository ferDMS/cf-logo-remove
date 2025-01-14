import fitz  # PyMuPDF
import os
import re

path_dir = "NOVIEMBRE 2024"
output_dir = f"final/{path_dir}"

# Coordinates for the white rectangle (x0, y0, x1, y1)
rect_coords = (450, 25, 600, 55)

for file in os.listdir(path_dir):
    filename = file.split('.')[0]
    print(f"Processing file: {filename}")
    path_file = os.sep.join([path_dir, f"{filename}.pdf"])
    with fitz.open(path_file) as doc:
        if not filename.endswith('-'):
            print(f"Modifying file: {filename}")
            # Draw a white rectangle on the first page
            first_page = doc[0]
            rect = fitz.Rect(*rect_coords)
            first_page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
        else:
            print(f"Filename ends with '-': {filename}")
            filename = filename.rstrip('-')
        output_path = os.sep.join([output_dir, f"{filename}.pdf"])
        doc.save(output_path)
        print(f"Saved file to: {output_path}")

