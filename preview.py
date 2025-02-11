import fitz
import matplotlib.pyplot as plt
import numpy as np
import sys

def preview_pdf(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Convert PDF page to numpy array for matplotlib
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

    # Create the figure and plot
    fig, ax = plt.subplots()
    ax.imshow(img)

    # Store coordinates
    coords = []

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            coords.append((x, y))
            print(f"Coordinates: ({x}, {y})")
            
            if len(coords) == 2:
                x0, y0 = coords[0]
                x1, y1 = coords[1]
                print(f"\nRectangle coordinates for RECT_COORDS:")
                print(f"({x0}, {y0}, {x1}, {y1})")
                
                # Draw rectangle
                rect = plt.Rectangle((x0, y0), x1-x0, y1-y0, 
                                  fill=False, color='red', linewidth=2)
                ax.add_patch(rect)
                plt.draw()
                coords.clear()

    # Connect the click event
    fig.canvas.mpl_connect('button_press_event', onclick)
    
    plt.title("Click two points to define rectangle (top-left and bottom-right)")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preview.py <pdf_file>")
        sys.exit(1)
    
    preview_pdf(sys.argv[1])
