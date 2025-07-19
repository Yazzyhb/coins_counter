"""
Image preprocessing module for the coin counter application.
"""
import numpy as np
from PIL import Image

def convert_to_grayscale(img, scale=2):
    """Convert an image to grayscale and resize it according to a given factor."""
    img = np.array(img)  # Convert the image to a NumPy array
    height, width, channels = img.shape

    # Resize the image
    height, width = height // scale, width // scale
    img = np.array(Image.fromarray(img).resize((width, height), Image.Resampling.LANCZOS))

    # Initialize an empty array for the grayscale image
    gray_array = np.zeros([height, width], dtype=np.uint8)

    # Convert each pixel to grayscale by averaging the RGB values
    for i in range(height):
        for j in range(width):
            gray_array[i][j] = int(sum(img[i][j]) / 3)

    # Create a grayscale image from the array
    gray_image = Image.fromarray(gray_array)
    return gray_image

def adjust_contrast(image, factor=1.5):
    """Adjust the contrast of an image using the given factor."""
    # Define the contrast adjustment formula
    def adjust_pixel(value):
        return max(0, min(255, int(128 + factor * (value - 128))))
    
    # Apply the adjustment to each pixel
    return image.point(adjust_pixel)

def apply_gaussian_blur(img):
    """Apply a Gaussian blur filter to a grayscale image."""
    img = np.array(img)  # Convert the image to a NumPy array

    # Check if the image is grayscale; convert if not
    if len(img.shape) > 2:
        height, width, _ = img.shape
        # Convert to grayscale
        gray_array = np.zeros([height, width], dtype=np.uint8)
        for i in range(height):
            for j in range(width):
                gray_array[i][j] = int(sum(img[i][j]) / 3)
        img = gray_array
    
    height, width = img.shape

    # Initialize an empty array for the blurred image
    blurred = np.zeros([height, width], dtype=np.uint8)

    # Apply the Gaussian kernel manually
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            pixel = int(img[i - 1][j - 1] * 1)
            pixel += int(img[i - 1][j] * 2)
            pixel += int(img[i - 1][j + 1] * 1)
            pixel += int(img[i][j - 1] * 2)
            pixel += int(img[i][j] * 4)
            pixel += int(img[i][j + 1] * 2)
            pixel += int(img[i + 1][j - 1] * 1)
            pixel += int(img[i + 1][j] * 2)
            pixel += int(img[i + 1][j + 1] * 1)

            # Normalize the pixel value and ensure it's in the valid range
            blurred[i][j] = check_overflow(int(pixel / 16))

    # Create a blurred image from the array
    blurred_image = Image.fromarray(blurred)
    return blurred_image

def check_overflow(pixel):
    """Ensure pixel values are within the range [0, 255]."""
    if pixel < 0:
        pixel = 0
    if pixel > 255:
        pixel = 255
    return pixel

def equalize_histogram(img, bins=256):
    """Apply histogram equalization to enhance image contrast."""
    img = np.array(img)
    img_flat = img.flatten()

    histogram = np.zeros(bins)

    # Histogram: count occurrences of each pixel value
    for pixel in img_flat:
        histogram[pixel] += 1

    # Cumulative sum of the histogram
    cs = np.cumsum(histogram)

    # Normalize the cumulative sum
    nj = (cs - cs.min()) * 255
    N = cs.max() - cs.min()
    cs = nj / N
    cs = cs.astype('uint8')

    # Apply the transformation to the image pixels
    img_new = cs[img_flat]

    # Reshape the transformed image
    img_new = np.reshape(img_new, img.shape)

    # Add borders to the image for visualization
    img_new[0, :] = 200
    img_new[:, 0] = 200
    img_new[:, -1] = 200
    img_new[-1, :] = 200

    # Convert to PIL Image
    img_new = Image.fromarray(img_new)
    return img_new

def preprocess_image(image, scale=2):
    """Apply the complete preprocessing pipeline to an image."""
    # Convert to grayscale and resize
    gray_image = convert_to_grayscale(image, scale)
    
    # Adjust contrast
    adjusted_image = adjust_contrast(gray_image, 1.5)
    
    # Apply Gaussian blur
    blurred_image = apply_gaussian_blur(adjusted_image)
    
    # Apply histogram equalization
    equalized_image = equalize_histogram(blurred_image, 256)
    
    # Return the preprocessed image
    return blurred_image  # Using blurred image as the final result