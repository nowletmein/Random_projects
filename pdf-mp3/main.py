
from gtts import gTTS
import PyPDF2


def pdf_reader(pdf, language):
    path = f'{pdf}.pdf'
    pdfreader = PyPDF2.PdfReader(path)
    clean_text = ''
    for i in range(len(pdfreader.pages)):
        page = pdfreader.pages[i]
        text = page.extract_text()
        clean_text += text.strip().replace('\n', ' ').replace("?", " ")

    print(clean_text)

    # Create a gTTS object with the specified language
    tts = gTTS(clean_text, lang=language)

    # Save to MP3 file
    tts.save(f'{pdf}.mp3')


if __name__ == '__main__':
    PDF = input("PDF: ")
    # Specify the language code for Hungarian (hu)
    pdf_reader(PDF, language='hu')

