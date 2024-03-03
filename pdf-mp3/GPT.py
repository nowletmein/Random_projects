import os
from gtts import gTTS
import PyPDF2

def pdf_reader(pdf_path, language):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    pdfreader = PyPDF2.PdfReader(pdf_path)
    clean_text = ''
    for i in range(len(pdfreader.pages)):
        page = pdfreader.pages[i]
        text = page.extract_text()
        clean_text += text.strip().replace('\n', ' ').replace("?", " ")

    print(clean_text)

    # Create a gTTS object with the specified language
    tts = gTTS(clean_text, lang=language)

    # Save to MP3 file
    mp3_path = os.path.splitext(pdf_path)[0] + ".mp3"
    tts.save(mp3_path)

if __name__ == '__main__':
    PDF_PATH = input("Enter the full path to the PDF file: ")
    LANGUAGE = input("Enter the language code (e.g., 'hu'): ")
    pdf_reader(PDF_PATH, language=LANGUAGE)