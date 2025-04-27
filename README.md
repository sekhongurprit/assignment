# Medical Prescription Extraction Pipeline

This repository was created with the help of **ChatGPT**.

## Project Overview

The **Medical Prescription Extraction Pipeline** aims to extract structured data from illegible medical prescription images. The project uses advanced image preprocessing techniques to enhance image quality and deploys machine learning models to parse the text and structure it into a usable format.

### Key Features:
- Preprocessing of prescription images to improve OCR accuracy.
- Use of **Google Gemini 1.5 Pro** to extract structured data from the preprocessed images.
- Evaluation of model accuracy and performance.
- Results stored in structured JSON format for easy querying.

## Preprocessing Improvements

The preprocessing step is crucial in improving the performance of Optical Character Recognition (OCR) models. Some improvements included in the pipeline are:

1. **Denoising**: Using advanced denoising techniques to remove noise and enhance the clarity of prescription images.
2. **Contrast Enhancement**: Applying Contrast Limited Adaptive Histogram Equalization (CLAHE) to improve contrast for better OCR performance.
3. **Sharpening**: Using kernel-based sharpening techniques to enhance the details of the image, making the text clearer for OCR.
4. **Resizing**: Scaling the image to a consistent size to ensure uniformity for model processing.

### Preprocessed Image Comparisons

The preprocessing step has resulted in a noticeable improvement in the OCR accuracy. The graph below shows the improvement in OCR performance after applying preprocessing techniques to the images:

![OCR Improvement Histogram](comparison_figures/improvement_histogram.png)

## Running Google Gemini on Preprocessed Data

Once the images are preprocessed, we send them to the **Google Gemini 1.5 Pro** model for structured data extraction. The **Gemini model** generates structured output, extracting key fields such as:

- Patient Name
- Doctor Name
- Date
- Medications
- Special Instructions

This structured output is then saved in JSON format for easy further processing and querying. 

## Future Evaluation Strategy

The current pipeline uses the **Google Gemini 1.5 Pro model** for extracting structured data from prescription images. However, in the future, we plan to evaluate the performance of the pipeline using **three different models** to ensure better extraction accuracy and reliability:

1. **OpenAI GPT-4 Vision**: A multimodal model capable of analyzing images and generating structured output.
2. **Google Gemini 1.5 Pro**: A state-of-the-art model we are currently using in this pipeline.
3. **Anthropic Claude 3 Opus**: Another high-performance multimodal model to compare results.

Each model's output will be compared for **field-level agreement**, **prescription-level agreement**, and **fuzzy matching** to assess consistency across different models.

## Setup Instructions

To get started, please follow these instructions to set up the environment:

1. **Install the required dependencies** by running:
    ```bash
    pip install -r requirements.txt
    ```

2. **Install Tesseract OCR**:
    - Follow the instructions in `install_tesseract_instructions.md` to install Tesseract OCR on your system.

3. **Run Preprocessing Script**:
    - Execute `preprocessing.py` to preprocess the prescription images in your input folder.

4. **Run Google Gemini Modeling Script**:
    - Execute `modelling_gemini.py` to send the preprocessed images to the **Google Gemini 1.5 Pro model** and get structured JSON output.

5. **View Structured Output**:
    - Use `structured_output.py` to load and search through the extracted structured data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
