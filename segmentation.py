"""
Image segmentation module for the coin counter application.
"""
import numpy as np
from PIL import Image

def otsu_threshold(image):
    """
    Apply Otsu's method to determine the optimal threshold for segmentation.
    """
    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Calculate the histogram and class edges
    histogram, bin_edges = np.histogram(image_array, bins=256, range=(0, 256))

    # Total number of pixels
    total_pixels = image_array.size

    # Variables for Otsu's method
    current_max, threshold = 0, 0
    sum_total = np.dot(np.arange(256), histogram)  # Sum of all pixel intensities
    sum_background, weight_background, weight_foreground = 0, 0, 0

    for i in range(256):
        # Update background weight
        weight_background += histogram[i]
        if weight_background == 0:
            continue

        # Update foreground weight
        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break

        # Update background sum
        sum_background += i * histogram[i]

        # Calculate means and between-class variance
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        between_class_variance = (
            weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
        )

        # Check if this variance is the largest
        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = i
    return threshold

def segment_coins(image):
    """
    Segment an image using Otsu's thresholding method.
    """
    # Calculate Otsu's threshold
    threshold = otsu_threshold(image)

    # Apply thresholding
    binary_image = image.point(lambda p: 255 if p > threshold else 0, mode='1')

    return binary_image

def erode(img, iterations=1):
    """
    Apply erosion to a binary image.
    """
    # Convert the image to a NumPy array
    img = np.array(img)
    height, width = img.shape  # Get image dimensions

    for it in range(iterations):  # Repeat erosion for the specified number of iterations
        delete_i = []  # List to store row indices of pixels to delete
        delete_j = []  # List to store column indices of pixels to delete

        # Iterate through each pixel inside the image borders
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # Check if the current pixel is True and is surrounded by any False pixels
                if (
                    img[i][j] == True and (
                        img[i - 1][j] == False or  # Pixel above
                        img[i][j - 1] == False or  # Pixel to the left
                        img[i][j + 1] == False or  # Pixel to the right
                        img[i + 1][j] == False     # Pixel below
                    )
                ):
                    delete_i.append(i)  # Add row index
                    delete_j.append(j)  # Add column index

        # Update identified pixels to False
        for i in range(len(delete_i)):
            img[delete_i[i]][delete_j[i]] = False

    # Return the eroded image
    return img

def dilate(img, iterations=1):
    """
    Apply dilation to a binary image.
    """
    # Convert the image to a NumPy array
    img = np.array(img)
    height, width = img.shape  # Get image dimensions

    for it in range(iterations):  # Repeat dilation for the specified number of iterations
        add_pixel_i = []  # List to store row indices of pixels to add
        add_pixel_j = []  # List to store column indices of pixels to add

        # Iterate through each pixel inside the image borders
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # Check if the current pixel is False and is adjacent to any True pixels
                if (
                    img[i][j] == False and (
                        img[i - 1][j] == True or  # Pixel above
                        img[i][j - 1] == True or  # Pixel to the left
                        img[i][j + 1] == True or  # Pixel to the right
                        img[i + 1][j] == True     # Pixel below
                    )
                ):
                    add_pixel_i.append(i)  # Add row index
                    add_pixel_j.append(j)  # Add column index

        # Update identified pixels to True
        for i in range(len(add_pixel_i)):
            img[add_pixel_i[i]][add_pixel_j[i]] = True

    # Return the dilated image
    return img

def filter_coins(segmented_image):
    """
    Apply a combination of erosion and dilation to filter segmented coins.
    """
    # Apply erosion to the segmented image to remove small noise
    eroded_image = erode(segmented_image, 5)  # Perform 5 iterations of erosion

    # Apply dilation to restore the size of remaining objects
    dilated_image = dilate(eroded_image, 1)  # Perform a single iteration of dilation

    # Convert the resulting NumPy array to a PIL Image
    filtered_image = Image.fromarray(dilated_image)

    # Return the filtered image
    return filtered_image