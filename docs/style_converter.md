# C-Style-Converter
C-Style-Converter ist ein Tool, das den C-Code automatisch dem in den C-Style-Check definierten Stil anpasst.

## Usage
### Run the style converter on a directory
```bash
python style_converter.py <directory> [CHECKS...]
```
### Example: Run all checks on the "src" directory
```bash
python style_converter.py src
```
### Example: Run specific checks (A4 and CL1) on the "src" directory
``` bash
python style_converter.py src A4 CL1
```
### Example: Run all checks on a single file
```bash
python style_converter.py src/example.c
```
### Get Information about the available checks
```bash
python style_converter.py
```

## Converter Checks
- [x] A4: Convert block comments to single-line comments
- [x] A5: Convert file names to start with a capital letter
- [x] CL1: Place braces on new lines
- [x] DV3: Convert variable names to Hungarian notation
