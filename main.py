"""
Main module for the coin counter application.
"""
import os
import argparse
from PIL import Image
import kagglehub

from preprocessing import preprocess_image
from segmentation import segment_coins, filter_coins
from counting import count_coins, visualize_coins, create_labeled_visualization
from evaluation import evaluate_image, batch_evaluate

def download_dataset():
    """Download the coin dataset from Kaggle."""
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("balabaskar/count-coins-image-dataset")
    print(f"Dataset downloaded to: {path}")
    return path

def process_single_image(image_path, scale=2, visualize=True):
    """
    Process a single image and count the coins.
    
    Parameters:
    image_path: Path to the image file
    scale: Scale factor for image resizing
    visualize: Whether to display visualization
    
    Returns:
    tuple: (number of coins, number of size differences)
    """
    # Load the image
    original_image = Image.open(image_path)
    print(f"Processing image: {os.path.basename(image_path)}")
    
    # Preprocess the image
    preprocessed_image = preprocess_image(original_image, scale)
    
    # Segment the image
    segmented_image = segment_coins(preprocessed_image)
    
    # Filter the segmented image
    filtered_image = filter_coins(segmented_image)
    
    # Count the coins
    num_coins, size_differences = count_coins(filtered_image)
    
    print(f"Detected {num_coins} coins with {size_differences} size categories")
    
    # Visualize if requested
    if visualize:
        labeled_image = create_labeled_visualization(filtered_image)
        visualize_coins(original_image, filtered_image, labeled_image, 
                       f"Detected {num_coins} coins with {size_differences} size categories")
    
    return num_coins, size_differences

def main():
    """Main function to run the coin counter application."""
    parser = argparse.ArgumentParser(description='Coin Counter Application')
    parser.add_argument('--image', type=str, help='Path to a single image to process')
    parser.add_argument('--dataset', action='store_true', help='Download and process the entire dataset')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate accuracy on the dataset')
    parser.add_argument('--scale', type=int, default=2, help='Scale factor for image resizing')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    
    args = parser.parse_args()
    
    if args.dataset:
        # Download the dataset
        dataset_path = download_dataset()
        base_folder = os.path.join(dataset_path, 'coins_images', 'coins_images')
        csv_path = os.path.join(dataset_path, 'coins_count_values.csv')
        
        if args.evaluate:
            # Evaluate the entire dataset
            batch_evaluate(base_folder, csv_path)
        else:
            print(f"Dataset downloaded to {dataset_path}")
            print(f"To evaluate, use --evaluate flag")
    
    elif args.image:
        # Process a single image
        process_single_image(args.image, args.scale, not args.no_viz)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()