import cv2
import numpy as np

def detect_patterns(image_path, template_paths):
    # Read the main image
    image = cv2.imread(image_path)

    # Convert the main image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize a counter for detected patterns
    pattern_count = 0

    for template_path in template_paths:
        # Read and convert each template to grayscale
        template = cv2.imread(template_path)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Apply template matching
        result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)

        # Set a threshold for detection
        threshold = 0.8  # Adjust this value based on your needs
        yloc, xloc = np.where(result >= threshold)

        # Draw rectangles around detected patterns
        h, w = gray_template.shape
        detected_coordinates = []  # List to store coordinates

        for (x, y) in zip(xloc, yloc):
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            detected_coordinates.append((x, y, w, h))  # Store coordinates for further processing

        # Use non-maximum suppression to filter overlapping boxes
        if detected_coordinates:
            boxes = np.array(detected_coordinates)
            x1 = boxes[:, 0]
            y1 = boxes[:, 1]
            x2 = boxes[:, 0] + boxes[:, 2]
            y2 = boxes[:, 1] + boxes[:, 3]

            areas = (x2 - x1) * (y2 - y1)
            indices = cv2.dnn.NMSBoxes(boxes.tolist(), [1]*len(boxes), score_threshold=0.8, nms_threshold=0.3)

            unique_detections = len(indices) if indices is not None else 0
            pattern_count += unique_detections

    # Show the result and print the pattern count
    # cv2.imshow('Detected Patterns', image)
    print(f"Number of unique detected patterns in {image_path}: {pattern_count}")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

templates = [
    'images\\test1\\template1.PNG',
    'images\\test1\\template2.PNG',
    'images\\test1\\template3.PNG',
    'images\\test1\\template4.PNG',
    'images\\test1\\template5.PNG',
    # Add more templates as needed
]

# Example usage
detect_patterns('images\\test1\\1.PNG', templates)
detect_patterns('images\\test1\\2.PNG', templates)
detect_patterns('images\\test1\\3.PNG', templates)
detect_patterns('images\\test1\\4.PNG', templates)
detect_patterns('images\\test1\\5.PNG', templates)
