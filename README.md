# File Compression Tool
This is a file compression tool that can compress and decompress a file, based on the LZW algorithm

## Motivation
This is meant to be a project for the Algorithm Design and Analysis subject 

## How to use?
The only prerequisite for this program to work is to have a python interpreter installed  
You can use this tool by typing the following in a terminal
```sh
python compression_tool.py mode input_file output_file
```
* mode:
  * -c = compression
  * -d = decompression
* input_file: the input file given by the user that is going to be compressed/decompressed
* output_file: the output file given by the user (if it doesn't exist, it will be created)

## Further information
Based on what I tested this tool with up until now, it works with files with the extensions **.txt, .pdf, .ppt, .png**  
