import fitz
import os
import sys

# x0, y0, x1, y1

# Helper function to convert hex to RGB tuple (values from 0 to 1)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return (
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255
    )

# Map different file_types to coordinates
BOUNDING_BOXES = {
    'default': [
        {"pages": [0], "coords": (392, 17, 590, 53), "color": "#FFFFFF"}
    ],
    'pagos': [
        {"pages": [0], "coords": (425, 17, 590, 50), "color": "#FFFFFF"}, # Esquina
    ],
    'morosidad': [
        {"pages": [0], "coords": (425, 17, 590, 46), "color": "#FFFFFF"}, # Esquina
        {"pages": [0], "coords": (200, 105, 400, 125), "color": "#4CBF8C"} # Morosidad
    ]
}

def parseFromDirectory(input_dir, output_dir, file_type='default'):
    
    # print(f"\n\nInput: {input_dir}\nOutput: {output_dir}\n\n")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get bounding boxes for the specified file type, defaulting to 'default' if not found
    box_configs = BOUNDING_BOXES.get(file_type, BOUNDING_BOXES['default'])
    
    for file in os.listdir(input_dir):
        print(f"{file}")
        if not file.endswith('.pdf'):
            continue
        filename = file.split('.')[0]
        print(f"Processing file: {filename}")
        path_file = os.sep.join([input_dir, f"{filename}.pdf"])
        with fitz.open(path_file) as doc:
            if not filename.endswith('-'):
                print(f"Modifying file: {filename}")
                
                # Apply each bounding box configuration
                for box_config in box_configs:
                    pages = box_config["pages"]
                    coords = box_config["coords"]
                    # Convert hex color to RGB tuple
                    color = hex_to_rgb(box_config["color"])
                    
                    # Handle both single integer and list of page indices
                    page_indices = [pages] if isinstance(pages, int) else pages
                    
                    for page_idx in page_indices:
                        if 0 <= page_idx < len(doc):
                            page = doc[page_idx]
                            rect = fitz.Rect(*coords)
                            page.draw_rect(rect, color=color, fill=color)
            else:
                print(f"Filename ends with '-': {filename}")
                filename = filename.rstrip('-')
                
            output_path = os.sep.join([output_dir, f"{filename}.pdf"])
            doc.save(output_path)
            print(f"Saved file to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python helper.py <input_directory> [file_type]")
        print("Available file types:", ", ".join(BOUNDING_BOXES.keys()))
        sys.exit(1)

    input_dir = sys.argv[1]
    
    # Get file_type if specified, otherwise use default
    file_type = 'default'
    if len(sys.argv) == 3:
        file_type = sys.argv[2]
        if file_type not in BOUNDING_BOXES:
            print(f"Warning: Unknown file type '{file_type}'. Using 'default' instead.")
            print("Available file types:", ", ".join(BOUNDING_BOXES.keys()))
            file_type = 'default'
    
    output_dir = os.sep.join(["final", input_dir])

    if os.path.exists(output_dir):
        counter = 1
        new_output_dir = output_dir
        while os.path.exists(new_output_dir):
            new_output_dir = f"{output_dir} ({counter})"
            counter += 1
        output_dir = new_output_dir
    
    os.makedirs(output_dir)

    print(f"Processing directory '{input_dir}' with file type '{file_type}'")
    parseFromDirectory(input_dir, output_dir, file_type)