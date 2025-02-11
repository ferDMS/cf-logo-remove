import fitz
import os
import sys

# Coordinates for the white rectangle (x0, y0, x1, y1)
RECT_COORDS = (392, 17, 590, 53)

def parseFromDirectory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file in os.listdir(input_dir):
        if not file.endswith('.pdf'):
            continue
        filename = file.split('.')[0]
        print(f"Processing file: {filename}")
        path_file = os.sep.join([input_dir, f"{filename}.pdf"])
        with fitz.open(path_file) as doc:
            if not filename.endswith('-'):
                print(f"Modifying file: {filename}")
                # Draw a white rectangle on the first page
                first_page = doc[0]
                rect = fitz.Rect(*RECT_COORDS)
                first_page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            else:
                print(f"Filename ends with '-': {filename}")
                filename = filename.rstrip('-')
            output_path = os.sep.join([output_dir, f"{filename}.pdf"])
            doc.save(output_path)
            print(f"Saved file to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = os.sep.join(["final", input_dir])

    if os.path.exists(output_dir):
        counter = 1
        new_output_dir = output_dir
        while os.path.exists(new_output_dir):
            new_output_dir = f"{output_dir} ({counter})"
            counter += 1
        output_dir = new_output_dir
    
    os.makedirs(output_dir)

    parseFromDirectory(input_dir, output_dir)