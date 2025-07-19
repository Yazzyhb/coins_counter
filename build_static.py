"""
Script to build static files for Netlify deployment.
"""
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Create dist directory
os.makedirs('dist', exist_ok=True)

# Copy static assets
if os.path.exists('static'):
    if os.path.exists('dist/static'):
        shutil.rmtree('dist/static')
    shutil.copytree('static', 'dist/static')

# Create uploads directory in dist
os.makedirs('dist/uploads', exist_ok=True)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Render index.html
template = env.get_template('index.html')
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(template.render())

# Create a simple results page template that will be populated by JavaScript
template = env.get_template('results.html')
with open('dist/results.html', 'w', encoding='utf-8') as f:
    # Render with placeholder values that will be replaced by JavaScript
    f.write(template.render(
        num_coins=0,
        size_differences=0,
        original_image='',
        labeled_image=''
    ))

print("Static files built successfully in 'dist' directory")