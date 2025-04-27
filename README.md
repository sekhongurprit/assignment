# Medical Prescription Extraction Pipeline

This project focuses on the extraction of structured data from illegible medical prescription images. The pipeline utilizes Optical Character Recognition (OCR) and machine learning models to parse prescription images, extract essential details, and output them in a structured format (JSON).

## Project Workflow

The main steps involved in the pipeline are:

1. **Preprocessing**: The input prescription images are processed to enhance readability, which includes operations such as:
   - Image denoising
   - Contrast enhancement
   - Sharpening
   - Resizing

2. **Text Extraction (OCR)**: The preprocessed images are then fed into an OCR engine (Tesseract) to extract raw text from the image.

3. **Model Evaluation**: In the future, the pipeline will integrate multiple state-of-the-art multimodal Large Language Models (LLMs), including:
   - OpenAI GPT-4 Vision
   - Google Gemini 1.5 Pro
   - Anthropic Claude 3 Opus
   The output from each model will be compared using fuzzy and exact matching techniques to evaluate agreement and accuracy in extracted fields.

4. **Data Structuring**: The extracted text is parsed and structured into a standardized JSON format, containing fields such as:
   - Patient Name
   - Doctor Name
   - Date of Prescription
   - Medications (including name, dosage, frequency, and duration)
   - Special Instructions

5. **Evaluation and Reporting**: The agreement between models is evaluated, and reports are generated to highlight any discrepancies or areas needing manual review.

## Installation Instructions

### Dependencies

The pipeline requires the following Python libraries:

- OpenCV (`opencv-python`)
- Tesseract OCR (`pytesseract`)
- NumPy (`numpy`)
- Pandas (`pandas`)
- Matplotlib (`matplotlib`)
- tqdm
- Requests (`requests`)
- Pillow (`Pillow`)
- python-Levenshtein

