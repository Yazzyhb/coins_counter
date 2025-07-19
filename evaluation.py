"""
Evaluation module for the coin counter application.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image
import numpy as np

from coin_counter.preprocessing import preprocess_image
from coin_counter.segmentation import segment_coins, erode, dilate, filter_coins
from coin_counter.counting import count_coins

def plot_histogram(image, axes, title="Histogram"):
    """
    Plot a histogram on the given axes.
    
    Args:
        image: The image to process, as a NumPy array.
        axes: The matplotlib axes on which to plot the histogram.
        title: The title of the histogram.
    """
    # Convert the image to a 1D array
    image_array = np.array(image).flatten()

    # Plot the histogram on the given axes
    axes.hist(image_array, bins=256, range=(0, 255), color='gray', alpha=0.7, density=False)
    axes.set_title(title)
    axes.set_xlabel('Pixel Value')
    axes.set_ylabel('Frequency')
    axes.grid(axis='y', linestyle='--', alpha=0.6)  # Add a light grid

def evaluate_image(image_path, true_count=None, scale=2):
    """
    Evaluate a single image and display the processing steps and results.
    
    Parameters:
    image_path: Path to the image file
    true_count: Actual number of coins in the image (if known)
    scale: Scale factor for image resizing
    
    Returns:
    dict: Dictionary containing evaluation results
    """
    # Load the image
    original_image = Image.open(image_path)
    
    # Preprocess the image
    gray_image = preprocess_image(original_image, scale)
    
    # Segment the image
    segmented_image = segment_coins(gray_image)
    
    # Filter the segmented image
    eroded_image = erode(segmented_image)
    dilated_image = dilate(eroded_image, 1)
    filtered_image = filter_coins(segmented_image)
    
    # Count the coins
    predicted_count, size_differences = count_coins(filtered_image)
    
    # Create visualization
    fig = plt.figure(figsize=(18, 15))
    gs = gridspec.GridSpec(3, 5, figure=fig, wspace=0.4)
    
    # First row for preprocessing images
    axes1 = fig.add_subplot(gs[0, 0])
    axes2 = fig.add_subplot(gs[0, 1])
    axes3 = fig.add_subplot(gs[0, 2])
    axes4 = fig.add_subplot(gs[0, 3])

    # Second row for histograms
    hist_axes1 = fig.add_subplot(gs[1, 0:2])  # Merge columns 0 and 1
    hist_axes2 = fig.add_subplot(gs[1, 2:4])  # Merge columns 2 and 3

    # Third row for segmentation images
    axes5 = fig.add_subplot(gs[2, 0])
    axes6 = fig.add_subplot(gs[2, 1])
    axes7 = fig.add_subplot(gs[2, 2])

    # First row: preprocessing steps
    axes1.imshow(original_image)
    axes1.set_title('Original Image')
    
    # Convert gray_image to RGB for display if it's grayscale
    if isinstance(gray_image, np.ndarray) and len(gray_image.shape) == 2:
        axes2.imshow(gray_image, cmap='gray')
    else:
        axes2.imshow(gray_image)
    axes2.set_title('Grayscale Image')
    
    axes3.imshow(segmented_image, cmap='gray')
    axes3.set_title('Segmented Image')
    
    axes4.imshow(filtered_image, cmap='gray')
    axes4.set_title('Filtered Image')

    # Second row: histograms
    plot_histogram(original_image, hist_axes1, title="Histogram of Original Image")
    plot_histogram(gray_image, hist_axes2, title="Histogram of Preprocessed Image")

    # Third row: segmentation steps
    axes5.imshow(segmented_image, cmap='gray')
    axes5.set_title('Segmented Image')
    
    axes6.imshow(eroded_image, cmap='gray')
    axes6.set_title('Eroded Image')
    
    axes7.imshow(dilated_image, cmap='gray')
    axes7.set_title('Dilated Image')

    # Turn off axes for image displays
    for ax in [axes1, axes2, axes3, axes4, axes5, axes6, axes7]:
        ax.axis('off')

    # Add a title with the results
    result_title = f"Image: {os.path.basename(image_path)}, Predicted Count: {predicted_count}"
    if true_count is not None:
        result_title += f", Actual Count: {true_count}"
        result_title += f", {'Correct' if predicted_count == true_count else 'Incorrect'}"
    
    plt.suptitle(result_title)
    plt.tight_layout()
    plt.show()
    
    # Return evaluation results
    results = {
        "image_name": os.path.basename(image_path),
        "predicted_count": predicted_count,
        "size_differences": size_differences
    }
    
    if true_count is not None:
        results["true_count"] = true_count
        results["correct"] = predicted_count == true_count
    
    return results

def batch_evaluate(dataset_path, csv_path, output_folder="correct_images"):
    """
    Evaluate multiple images and calculate accuracy metrics.
    
    Parameters:
    dataset_path: Path to the dataset folder
    csv_path: Path to the CSV file with ground truth data
    output_folder: Folder to save correctly evaluated images
    
    Returns:
    dict: Dictionary containing evaluation metrics
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load ground truth data
    truth_data = pd.read_csv(csv_path)
    
    results = []
    total_images = 0
    total_errors = 0
    scale = 8  # Scale factor for image preprocessing
    
    # Process each image in the dataset
    for _, row in truth_data.iterrows():
        folder = row['folder']
        image_name = row['image_name']
        true_count = row['coins_count']
        
        image_path = os.path.join(dataset_path, folder, image_name)
        
        try:
            # Load and process the image
            original_image = Image.open(image_path)
            print(f"Processing image: {image_name}")
            
            # Preprocess the image
            preprocessed_image = preprocess_image(original_image, scale)
            
            # Segment the image
            segmented_image = segment_coins(preprocessed_image)
            
            # Filter the segmented image
            filtered_image = filter_coins(segmented_image)
            
            # Count the coins
            predicted_count, size_differences = count_coins(filtered_image)
            
            # Record the results
            total_images += 1
            is_error = predicted_count != true_count
            
            if is_error:
                total_errors += 1
            else:
                # Save correctly evaluated images
                import shutil
                correct_image_path = os.path.join(output_folder, image_name)
                shutil.copy(image_path, correct_image_path)
            
            # Add results to the list
            results.append({
                "image_name": image_name,
                "true_count": true_count,
                "predicted_count": predicted_count,
                "correct": not is_error,
                "size_differences": size_differences
            })
            
        except Exception as e:
            print(f"Error processing {image_name}: {e}")
    
    # Calculate accuracy
    accuracy = ((total_images - total_errors) / total_images) * 100 if total_images > 0 else 0
    
    # Print evaluation results
    print(f"Evaluation Results:\n"
          f"Total Images Evaluated: {total_images}\n"
          f"Total Errors: {total_errors}\n"
          f"Accuracy: {accuracy:.2f}%")
    
    # Save detailed results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("evaluation_results.csv", index=False)
    print("Detailed results saved to evaluation_results.csv")
    
    return {
        "results": results,
        "total_images": total_images,
        "total_errors": total_errors,
        "accuracy": accuracy
    }