"""
Coin counting module for the coin counter application.
"""
import numpy as np
from scipy import ndimage as ndi
from PIL import Image

def count_coins(filtered_image, size_threshold=50):
    """
    Count the number of coins and classify them by size.
    
    Parameters:
    filtered_image: Binary image after filtering (PIL Image)
    size_threshold: Threshold for significant size differences between coins
    
    Returns:
    num_coins: Total number of coins detected
    size_differences: Number of significant size differences detected among coins
    """
    # Convert the PIL Image to a NumPy array
    binary_array = np.array(filtered_image)

    # Label connected components (each coin gets a unique label)
    labeled_array, num_coins = ndi.label(binary_array)

    # Calculate the size of each labeled component (coin area)
    sizes = np.bincount(labeled_array.ravel())

    # Ignore the background (label 0) by setting its size to 0
    sizes[0] = 0

    # Extract coin sizes (excluding the background label)
    coin_sizes = sizes[1:]

    # Initialize the counter for significant size differences
    diff_count = 1

    # Compare sizes of all coin pairs to detect significant differences
    for i in range(len(coin_sizes)):
        for j in range(i + 1, len(coin_sizes)):
            # Calculate the difference between coin sizes
            size_diff = abs(coin_sizes[i] - coin_sizes[j])
            # If the difference exceeds the threshold, increment the counter
            if size_diff >= size_threshold:
                diff_count += 1

    # Apply a rule: if the difference counter exceeds the total number of coins,
    # set the counter to the total number of coins
    if diff_count > num_coins:
        diff_count = num_coins

    # Return the total number of coins detected and the number of significant differences
    return num_coins, diff_count

def visualize_coins(original_image, processed_image, labeled_image=None, title="Coin Detection"):
    """
    Visualize the original image alongside the processed image with detected coins.
    
    Parameters:
    original_image: The original input image
    processed_image: The processed binary image showing detected coins
    labeled_image: Optional labeled image showing different coins with different colors
    title: Title for the visualization
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2 if labeled_image is None else 3, figsize=(12, 4))
    
    # Display original image
    axes[0].imshow(original_image)
    axes[0].set_title("Original Image")
    axes[0].axis('off')
    
    # Display processed binary image
    axes[1].imshow(processed_image, cmap='gray')
    axes[1].set_title("Processed Image")
    axes[1].axis('off')
    
    # Display labeled image if provided
    if labeled_image is not None:
        axes[2].imshow(labeled_image, cmap='nipy_spectral')
        axes[2].set_title("Labeled Coins")
        axes[2].axis('off')
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()
    
def create_labeled_visualization(binary_image):
    """
    Create a visualization where each coin is labeled with a different color.
    
    Parameters:
    binary_image: Binary image with detected coins
    
    Returns:
    labeled_image: Image with each coin colored differently
    """
    # Convert to numpy array if it's a PIL Image
    if isinstance(binary_image, Image.Image):
        binary_array = np.array(binary_image)
    else:
        binary_array = binary_image
        
    # Label connected components
    labeled_array, _ = ndi.label(binary_array)
    
    return labeled_array