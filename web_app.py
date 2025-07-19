"""
Web interface for the Coin Counter application.
"""
import os
import uuid
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

from preprocessing import preprocess_image
from segmentation import segment_coins, filter_coins
from counting import count_coins, create_labeled_visualization

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'coin_counter_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path, scale=2):
    """Process an image and return the results."""
    # Load the image
    original_image = Image.open(image_path)
    
    # Preprocess the image
    preprocessed_image = preprocess_image(original_image, scale)
    
    # Segment the image
    segmented_image = segment_coins(preprocessed_image)
    
    # Filter the segmented image
    filtered_image = filter_coins(segmented_image)
    
    # Count the coins
    num_coins, size_differences = count_coins(filtered_image)
    
    # Create visualization
    labeled_image = create_labeled_visualization(filtered_image)
    
    # Convert NumPy array to PIL Image for saving
    labeled_pil = Image.fromarray(np.uint8(labeled_image * 255 / np.max(labeled_image)))
    
    # Convert images to base64 for display
    buffered = io.BytesIO()
    labeled_pil.save(buffered, format="PNG")
    labeled_image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    buffered = io.BytesIO()
    original_image.save(buffered, format="PNG")
    original_image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return {
        'num_coins': num_coins,
        'size_differences': size_differences,
        'original_image': original_image_b64,
        'labeled_image': labeled_image_b64
    }

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process the image."""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a unique filename
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image
        scale = int(request.form.get('scale', 2))
        results = process_image(filepath, scale)
        
        return render_template('results.html', 
                              num_coins=results['num_coins'],
                              size_differences=results['size_differences'],
                              original_image=results['original_image'],
                              labeled_image=results['labeled_image'])
    
    flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif).')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)