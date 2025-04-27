# Tesseract OCR Installation Instructions

Tesseract OCR is an open-source Optical Character Recognition (OCR) engine that will be used to extract text from prescription images in this project. To ensure that the pipeline runs correctly, you need to install Tesseract OCR and make sure it’s accessible in your system’s PATH.

Follow the instructions below to install Tesseract on your system.

## Installation for Windows

1. **Download the Tesseract Installer**:
   - Go to the Tesseract official GitHub releases page: [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract/releases)
   - Download the latest `.exe` installer for Windows.

2. **Run the Installer**:
   - Launch the `.exe` installer and follow the prompts to install Tesseract.
   - By default, Tesseract is installed in `C:\Program Files\Tesseract-OCR\`.

3. **Add Tesseract to the PATH**:
   - Go to the start menu, search for **Environment Variables**, and click on **Edit the system environment variables**.
   - In the **System Properties** window, click on the **Environment Variables** button.
   - Under **System variables**, find and select the `Path` variable, then click **Edit**.
   - Click **New** and add the path to your Tesseract installation, e.g., `C:\Program Files\Tesseract-OCR\`.
   - Click **OK** to apply the changes.

4. **Verify the Installation**:
   - Open a new Command Prompt window and type:
     ```bash
     tesseract --version
     ```
   - If the installation is successful, you should see the version of Tesseract printed.

## Installation for macOS

1. **Install via Homebrew**:
   - If you don't have Homebrew installed, you can install it by running the following command in your terminal:
     ```bash
     /bin/bash -

