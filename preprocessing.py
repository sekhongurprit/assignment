import cv2
import pytesseract
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

# Input and output folders
input_folder = 'dohee/'
output_folder = 'dohee_preprocessed/'
comparison_folder = 'comparison_figures/'

# Create output folders if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(comparison_folder, exist_ok=True)

# Lists to store results
improvement_scores = []
processed_filenames = []

# Preprocessing function
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, sharpen_kernel)
    resized = cv2.resize(sharpened, (800, int(800 * sharpened.shape[0] / sharpened.shape[1])))
    return resized

# OCR extraction function
def extract_text(img):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

# Processing each image
for filename in tqdm(os.listdir(input_folder)):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(input_folder, filename)
        
        try:
            original_img = cv2.imread(image_path)
            if original_img is None:
                print(f"⚠️ Warning: Unable to load image {filename}. Skipping.")
                continue

            preprocessed_img = preprocess_image(original_img)

            # Save the preprocessed image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, preprocessed_img)

            original_text = extract_text(original_img)
            preprocessed_text = extract_text(preprocessed_img)

            original_count = len(original_text.strip())
            preprocessed_count = len(preprocessed_text.strip())

            if original_count > 0:
                improvement_percent = ((preprocessed_count - original_count) / original_count) * 100
                improvement_scores.append(improvement_percent)
                processed_filenames.append(filename)
            else:
                print(f"⚠️ Warning: No text detected in original image {filename}. Skipping.")

        except Exception as e:
            print(f"⚠️ Warning: Error processing {filename}: {str(e)}. Skipping.")

# Plotting histogram of improvements
if improvement_scores:
    plt.figure(figsize=(10,6))
    plt.hist(improvement_scores, bins=20, color='skyblue', edgecolor='black')
    plt.title('OCR Improvement Percentage After Preprocessing')
    plt.xlabel('Improvement (%)')
    plt.ylabel('Number of Images')
    plt.grid(True)
    plt.savefig(os.path.join(comparison_folder, 'improvement_histogram.png'))  # Save histogram
    plt.show()

    average_improvement = np.mean(improvement_scores)
    print(f'✅ Average OCR Improvement: {average_improvement:.2f}%')
else:
    print("❌ No valid images processed.")

# Visualization function to show and save side-by-side comparisons
def show_comparisons(image_info_list, input_folder, output_folder, comparison_folder):
    num_images = len(image_info_list)
    fig, axes = plt.subplots(num_images, 2, figsize=(12, 4 * num_images))

    if num_images == 1:
        axes = np.expand_dims(axes, axis=0)

    for idx, (filename, improvement) in enumerate(image_info_list):
        original_path = os.path.join(input_folder, filename)
        preprocessed_path = os.path.join(output_folder, filename)

        original_img = cv2.cvtColor(cv2.imread(original_path), cv2.COLOR_BGR2RGB)
        preprocessed_img = cv2.cvtColor(cv2.imread(preprocessed_path), cv2.COLOR_BGR2RGB)

        axes[idx, 0].imshow(original_img)
        axes[idx, 0].set_title(f"Original\n{filename}", fontsize=10)
        axes[idx, 0].axis('off')

        axes[idx, 1].imshow(preprocessed_img)
        axes[idx, 1].set_title(f"Preprocessed\n{improvement:.2f}% Improvement", fontsize=10)
        axes[idx, 1].axis('off')

    plt.tight_layout()
    save_path = os.path.join(comparison_folder, 'side_by_side_comparison.png')
    plt

