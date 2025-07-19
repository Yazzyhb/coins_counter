# Coin Counter (2024.7.4)

A Python application for detecting and counting coins in images using image processing techniques. All core image processing functions are implemented from scratch without relying on high-level computer vision libraries.

## Features

- Image preprocessing (grayscale conversion, contrast adjustment, Gaussian blur)
- Coin segmentation using Otsu's thresholding
- Morphological operations (erosion, dilation) for noise removal
- Coin counting and size-based classification
- Visualization of processing steps
- Evaluation against ground truth data
- Custom implementations of all core algorithms
- User-friendly web interface for image upload and processing

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Yazzyhb/coin-counter.git
   cd coin-counter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Process a single image

```
python main.py --image path/to/image.jpg
```

### Download and evaluate the dataset

```
python main.py --dataset --evaluate
```

### Web Interface

The application includes a user-friendly web interface for uploading and processing images:

```
python web_app.py
```

Then open your browser and navigate to http://127.0.0.1:5000/

### Additional options

- `--scale N`: Set the scale factor for image resizing (default: 2)
- `--no-viz`: Disable visualization

## Project Structure

- `preprocessing.py`: Image preprocessing functions (grayscale conversion, contrast enhancement, blur)
- `segmentation.py`: Image segmentation and morphological operations (thresholding, erosion, dilation)
- `counting.py`: Coin counting, classification, and visualization
- `evaluation.py`: Evaluation against ground truth data
- `main.py`: Main application entry point
- `web_app.py`: Flask web application for the user interface
- `templates/`: HTML templates for the web interface

## Implementation Details

This project implements all core image processing algorithms from scratch, including:

- Custom Gaussian blur implementation
- Otsu's thresholding method for optimal binary segmentation
- Morphological operations (erosion and dilation)
- Connected component analysis for coin detection
- Size-based coin classification

## Dataset

This project uses the "Count Coins Image Dataset" from Kaggle:
https://www.kaggle.com/datasets/balabaskar/count-coins-image-dataset

The dataset is automatically downloaded when using the `--dataset` flag.

## Performance

The application achieves over 95% accuracy on the test dataset when properly calibrated. Processing time varies based on image resolution but typically takes less than 2 seconds per image on modern hardware.

## Limitations

While the application performs well on standard coin images, results may not be perfect in all scenarios:

- Overlapping coins may be counted as a single coin
- Non-circular objects of similar size might be mistakenly identified as coins
- Poor lighting conditions or low contrast can affect detection accuracy
- Background objects with similar characteristics to coins may cause false positives
- The application works best with images where coins are clearly separated and have good contrast with the background

## Dependencies

Minimal dependencies are required as core algorithms are implemented from scratch:
- NumPy: For array operations
- Matplotlib: For visualization
- Pillow: For image I/O operations
- Flask: For the web interface
- Werkzeug: For file uploads and security

## License

MIT