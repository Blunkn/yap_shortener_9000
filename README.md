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
- Python 3.1.3 or above.
- Google Tesseract-OCR.
- Both in your system PATH.

## How to Use
---
- Clone the repository into a folder.
- When your File Explorer is on the directory the .py program is on, click on the directory bar and type "cmd".
- Type in the command "py yap_shortener.py" to run it.
- Place files in input folder, run the program on Command Prompt, and it will extract text in output folder.
- Now copy the output .txt file or just copy the text, dump it into a genAI prompt, and ask it for a summary.

## Issues
---
- External tool Tesseract-OCR had to be manually downloaded and added to PATH for this to properly work. I'm looking to increasing accessibility such that non-tech-savvy people can run it without minimal dependency installation.
- .docx and .pdf features untested. Currently finding test data.
- Program keeps outputting "Invalid option." from the menu() code no matter what is pressed.

## Version Control
---

v1.1 - 
- fixed image processing feature 
- tweaked code to write into a single output file every session
- removed pad.txt, replaced with .gitignore and .gitkeep files for cleaner file structure

v1.0 - initial commit
