# The Yap Shortener 9000
---

The Singaporean cosplay community post-COVID has seen a lot of drama, from petty arguments to full-blown cases with police involvement.
Most messes are also documented with screenshots, documents, and other files with intricate detail and below-average prose.
Unfortunately, no one has the time or energy to sift through all that shit, given most drama is started by petty kids with nothing better to do.

I thus introduce the *Yap Shortener 9000*, a program that automates noise filtering by extracting text from input data and allows you to feed it to a generative AI for a summary.

## Features
---
- Currently supports common image files(.jpg, .png), .docx, and .pdf.
- Place files in input folder, run the program on Command Prompt, and it will extract text in output folder.
- Now upload the output .txt file or just copy the text, dump it into a genAI prompt, and ask it for a summary.

## How to Use
---
- Clone the repository into a folder.
- When your File Explorer is on the directory the .py program is on, click on the directory bar and type "cmd".
- Type in the command "py yap_shortener.py" to run it.

## Issues
---
- Image processing feature currently faulty. It will spit out output files that simply say "class <Exception>".
- Text from multiple files are not concatenated into a single output file. Text still has to be manually compiled together.
- "pad.txt" was an arbitrary file used to include the input & output folders in the repo. Need to tweak code to ignore those files.

## Version Control
---

v1.0 - initial commit
