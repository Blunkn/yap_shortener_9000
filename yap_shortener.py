# native libraries
import os, sys, datetime, io
from pathlib import Path

# 3rd party libraries
import pytesseract, docx, PyPDF2
from PIL import Image, ImageEnhance

# main class
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
    def enhance_image(self, img):
        """
        enhance image for better OCR results

        args:
        img - the image

        returns:
        img - the image(enhanced)
        """
        # this converts image to grayscale
        img = img.convert('L')
        # increase contrast then enhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        return img

    def extract_image(self, imgpath):
        """
        uses pytesseract to extract text from images
        use for screenshots

        args:
        imgpath - filepath to the image

        returns:
        txt - pytesseract's output for the image
        """
        try:
            img = Image.open(imgpath)
            enimg = self.enhance_image(img)
            txt = pytesseract.image_to_string(enimg)
            return txt
        except Exception as e:
            return f"Error: {str(Exception)}"
        
    def extract_image_from_bytes(self, image_bytes):
        """
        extract text from image bytes using pytesseract

        args:
        image_bytes - the image, but in bytes

        returns:
        txt - text extracted from input image
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            # Optional: Enhance image quality for better OCR
            img = self.enhance_image(img)
            txt = pytesseract.image_to_string(img)
            return txt
        except Exception as e:
            return f"Error processing embedded image: {str(e)}"
                
    def extract_doc(self, docpath):
        """
        uses python-docx to extract text & embedded images from a .docx file

        args:
        docpath - file path to the .docx file

        returns:
        final_txt - all text that can be extracted from the .docx file
        """
        try:
            doc = docx.Document(docpath)
            # base func: extract text
            txt = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            image_txt = []
            image_count = 0

            # print(f"\nScanning document: {docpath.name}")
            # print(f"Document has {len(doc.inline_shapes)} inline shapes")
            
            
            for idx, shape in enumerate(doc.inline_shapes):
                # print(f"Shape {idx}: type={shape.type}")
                
                # check if image
                if shape.type == 3:  # WD_INLINE_SHAPE_TYPE.PICTURE
                    
                    # determine .xml structure
                    try:
                        xml_str = str(shape._inline.xml)[:200]
                        print(f"Shape XML snippet: {xml_str}...")
                    except:
                        print("Couldn't get shape XML")
            
            # shoutout to claude again for helping me explain the ways documents are made & processed in different platforms
            # this uses the direct relationship extraction
            # this primarily ensures compatibility with the way google docs does their documents
            # may not work with documents done using actual microsoft word
            # who the fuck writes out drama on m365 anyway? lol
            try:
                rels = doc.part.rels
                # print(f"Document has {len(rels)} relationships")
                
                for rel_id, rel in rels.items():
                    # print(f"Checking relationship: {rel_id} -> {rel.reltype} -> {rel.target_ref}")
                    
                    # check if got image relationship
                    if "image" in rel.reltype.lower() or "image" in rel.target_ref.lower():
                        # print(f"Found image relationship: {rel_id}")
                        try:
                            image_count += 1
                            image_part = rel.target_part
                            image_bytes = image_part.blob
                            
                            res = self.extract_image_from_bytes(image_bytes)
                            
                            if res.strip():
                                image_txt.append(f"Embedded Image Text {image_count}:\n{res}\n")
                            else:
                                image_txt.append(f"Embedded Image {image_count} (no text detected):\n")
                        except Exception as e:
                            print(f"Error extracting relationship image: {str(e)}")
            except Exception as e:
                print(f"Error in relationship extraction: {str(e)}")
                
            print(f"Total images found: {image_count}")
            
            # combine base text & text in images
            final_txt = txt
            if image_txt:
                final_txt += "\n\n" + "\n".join(image_txt)
            return final_txt
        except Exception as e:
            print(f"Document extraction error: {str(e)}")
            return f"Error: {str(e)}"
            
    def extract_pdf(self, pdfpath):
        """
        uses pypdf2 to extract text from a .pdf file
        ! not able to extract embedded images yet

        args:
        pdfpath - file path to the .pdf file

        returns:
        txt - text extracted from the .pdf
        """
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
        """
        saves extracted text to the output dir
        
        args:
        text - text from extractor functions
        filename - input file's name

        returns:
        output_file - the file this function wrote to
        """
        # writes to the created output file
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"From {filename}:\n")
            f.write(text)
        return self.output_file
    
    def process_files(self):
        """
        processes all files in input dir
        
        args:
        N/A

        returns:
        processed - a counter of the number of files processed
        """
        ext = ['.png', '.jpg', '.jpeg', '.docx', '.doc', '.pdf']
        
        processed = 0
        
        # iteratively goes thru input folder to process each file(if supported)
        for file in self.input.iterdir(): 
            # 1st check to see if file is supported; added ignore function lol
            if file.suffix.lower() in ext: 
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
    print("1.0.0")
    print("Please choose an option:")
    print("1 - Process files")
    print('2 - Help')
    print('3 - Exit')
    return input('Select an option (1-3): ')

def help():
    tldr = YapShortener()

    print("\nProgram Summary")
    print("""
          When drama comes up, communities like to write long-winded,
          convoluted texts no one has the time or energy to read up on.
          The Yap Shortener 9000 serves to extract all known forms of written drama text
          into a simple .txt file to be fed to a generative AI for summarisation prompts.
          I wrote this program because:
          1. I was bored.
          2. It would be funny feeding dirty laundry to an AI.
          3. It may save people time.
          Be warned that the program is not infallible; texts may be extracted wrongly or incompletely.
          Generative AI may not have the full context, so they may also respond with inaccurate summaries.
          Have fun.
          """)
    print("\n")
    print("\nProgram Usage")
    print("""
          1. Ensure you have everything placed in the input folder. Sort them in order if you can.
          2. Press Option 1 to automatically process everything into an output .txt file.
          3. Upload the file to a genAI. Type your own prompt to ask it for a summary.
          """)

def main():
    tldr = YapShortener()

    while True:
        choice = menu().strip()
        if choice == '1':
            res = tldr.process_files() # res returns number of files processed
            if res == 0:
                print(f"\nThe input directory is empty, file types inside are not supported, or files inside cannot be detected.")
            else:
                print(f"\nProcessed {res} files")
        elif choice == '2':
            help()
        elif choice == '3':
            print("\nExiting program...")
            break
        else:
            print('\nInvalid option.')

if __name__ == "__main__":
    main()
