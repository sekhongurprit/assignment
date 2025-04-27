import shutil

if shutil.which('tesseract') is None:
    raise EnvironmentError('Tesseract OCR is not installed or not in PATH.')
