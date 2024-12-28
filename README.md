# The Yap Shortener 9000
---

The Singaporean cosplay community post-COVID has seen a lot of drama, from petty arguments to full-blown cases with police involvement.
Most messes are also documented with screenshots, documents, and other files with intricate, comprehensive detail and below-average prose.
Unfortunately, no one has the time or energy to sift through all that shit, given most drama is started by petty children(or adult-children) with nothing better to do.

I thus introduce the *Yap Shortener 9000*, a program that automates noise filtering by extracting text from input data and allows you to feed it to a generative AI for a summary.

Yes it's just a text extractor by another name btw.

## Features
---
- Currently supports common image files(.jpg, .png), .docx, and .pdf.
- Takes all files in the input folder, processes them based on the file type they are, and spits out raw text into an output .txt file.
- This output file is meant to be manually fed to a genAI so you can ask it for a summary. I hold no responsibility for any attempted AI self-termination after reading any sort of stupidity you feed into it.
- *No AI API.* That requires additional documentation reading and programming I'm too lazy to do. Most AIs also have limited prompt tokens anyway, so it may hinder my program's functionality.

## Dependencies
---
- Python 3.13 or above.
https://www.python.org/downloads/ Download the latest *stable* version(not pre-release, etc). When installing, check the "add to PATH" option. I'm pretty sure there was one.

- Python Dependencies:
    - Pillow
    - Pytesseract
    - python-docx
    - PyPDF2

To install dependencies, type "pip install" and then the dependency name on Command Prompt.

- Tesseract-OCR.
https://github.com/UB-Mannheim/tesseract/wiki Download the latest x64 installer. When installing, check "install for everyone".

Now do the following magic ritual drawn from ancient tech wizardry knowledge to PATH your OCR installation:
1. Press Win + R, type "sysdm.cpl", press Enter
2. Go to "Advanced" tab
3. Click "Environment Variables" near the bottom
4. Under "System Variables" (bottom section), find "Path"
5. Click "Edit"
6. Click "New"
7. Add the Tesseract installation path (typically C:\Program Files\Tesseract-OCR)
(ps. to get that filepath you need to check "install for everyone" during installation; if wrong, just reinstall)
8. Click "OK" on all windows


## How to Use
---
- Download the repo as a .zip file. Extract all of it out.
- When your File Explorer is on the directory the .py program is on, click on the directory bar and type "cmd".
- Type in the command "py yap_shortener.py" to run it.
- Ensure files you wanna process are in input folder, run the program on Command Prompt, and it will extract text in output folder.
- Now copy the output .txt file or just copy the text, dump it into a genAI prompt, and ask it for a summary.

## Issues
---
- External tool Tesseract-OCR had to be manually downloaded and added to PATH for this to properly work. I'm looking to increasing accessibility such that non-tech-savvy people can run it with minimal dependency installation.
- .docx and .pdf features untested. Currently finding test data.

## Roadmap
---
- Extraction of text from embedded images in .docx and .pdf files.

## Version Control
---
v1.2 -
- fixed code outputting "invalid option" no matter what is pressed
- added additional text to handle if input directory is empty or files inside aren't supported/detected
- changed readme to have a quick demo on how to install dependencies and PATH them; added easier download & use method too

v1.1 - 
- fixed image processing feature 
- tweaked code to write into a single output file every session
- removed pad.txt, replaced with .gitignore and .gitkeep files for cleaner file structure

v1.0 - initial commit
