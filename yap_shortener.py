import os, sys, pytesseract, docx, PyPDF2, datetime
from PIL import Image
from pathlib import Path

class YapShortener:
    def __init__(self):
        self.input = Path("input")
        self.output = Path("output")

        # create folders if missing
        # mkdir is from Path
        # exist_ok stops it from freaking out if folders already exist
        self.input.mkdir(exist_ok=True)
        self.output.mkdir(exist_ok=True)

        # this creates a new output file before anything
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = self.output / f"{timestamp}_results.txt"

    # --- EXTRACTORS ---
    def extract_image(self, imgpath):
        """Uses Pytesseract to extract text from images."""
        try:
            img = Image.open(imgpath)
            txt = pytesseract.image_to_string(img)
            return txt
        except Exception:
            return f"Error: {str(Exception)}"
        
    def extract_doc(self, docpath):
        """Uses python-docx to extract text from .docx file"""
        try:
            doc = docx.Document(docpath)
            txt = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return txt
        except Exception:
            return f"Error: {str(Exception)}"
        
    def extract_pdf(self, pdfpath):
        """Uses PyPDF2 to extract text from a .pdf file"""
        try:
            txt = ""
            with open(pdfpath, 'rb') as f: # b means binary; .pdf files are binary files
                reader = PyPDF2.PdfReader(f)
                for pg in reader.pages:
                    txt += pg.extract_text() + "\n"
            return txt
        except Exception:
            return f"Error: {str(Exception)}"
        
    # --- PROCESSORS ---
    def save_text(self, text, filename): # text takes in output from extractors; filename is taken from files in input dir
        """Saves extracted text to the output dir"""
        # writes to the created output file
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"From {filename}:\n")
            f.write(text)
        return self.output_file
    
    def process_files(self):
        """Processes all files in input dir"""
        ext = ['.png', '.jpg', '.jpeg', '.docx', '.doc', '.pdf']
        
        processed = 0

        for file in self.input.iterdir(): # iteratively goes thru input folder to process each file(if supported)
            if file.suffix.lower() in ext and file.name != "pad.txt": # 1st check to see if file is supported; added ignore function lol
                if file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    text = self.extract_image(file)
                    output_path = self.save_text(text, file.name)
                    processed += 1
                    print(f"Processed {file}; saved to {output_path}")
                    print(f"Files processed: {processed}")
                if file.suffix.lower() in ['.docx', '.doc']:
                    text = self.extract_doc(file)
                    output_path = self.save_text(text, file.name)
                    processed += 1
                    print(f"Processed {file}; saved to {output_path}")
                    print(f"Files processed: {processed}")
                if file.suffix.lower() == '.pdf':
                    text = self.extract_pdf(file)
                    output_path = self.save_text(text, file.name)
                    processed += 1
                    print(f"Processed {file}; saved to {output_path}")
                    print(f"Files processed: {processed}")

        return processed
    
def menu():
    print("\nThe Yap Shortener 9000")
    print("Please choose an option:")
    print("1 - Process all files in input folder")
    print('2 - Help')
    print('3 - Exit')
    return input('Select an option (1-3): ')

def help():
    tldr = YapShortener()

    print("\nProgram Summary")
    print("""When drama comes up, communities like to write long-winded,
          convoluted texts no one has the time or energy to read up on.
          The Yap Shortener 9000 serves to extract all known forms of written drama text
          into a simple .txt file to be fed to a generative AI for summarisation prompts.
          I wrote this program because:
          1. I was bored.
          2. It would be funny feeding dirty laundry to an AI.
          3. It may save people time.
          Be warned that the program is not infallible; texts may be extracted wrongly or incompletely.
          Generative AI may not have the full context, so they may respond with inaccurate summaries.
          Have fun.""")

def main():
    tldr = YapShortener()

    while True:
        choice = menu()
        if choice == '1':
            res = tldr.process_files()
            print(f"\nProcessed {res} files")
        if choice == '2':
            help()
        if choice == '3':
            print("\nExiting program...")
            break
        else:
            print('\nInvalid option.')

if __name__ == "__main__":
    main()
