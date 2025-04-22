import re
import os
import sys

# Verbose mode for debugging
DEBUG = True

def convert_filename_to_uppercase(filename):
    """Convert first letter of filename to uppercase (Rule A5)
    Args:
        filename: Name of current file
    Returns:
        filename: Converted filename
    """
    if filename[0].islower():
        filename = filename[0].upper() + filename[1:]
    return filename

def convert_block_comments_to_single_line(lines):
    """Convert block comments to single-line comments (Rule A4)
    Args:
        lines: List of source code lines
    Returns:
        lines: All lines including conrrected lines
    """
    for i, line in enumerate(lines):
        if line.strip().startswith("/*"):
            if(DEBUG):print(f"Converting block comment to single-line comment at line {i + 1}")
            lines[i] = line.replace("/*", "//")
            while i + 1 < len(lines) and not lines[i + 1].strip().endswith("*/"):
                lines[i + 1] = lines[i + 1].replace("*", "").strip()
                lines[i] = lines[i] + " " + lines[i + 1]
                lines.pop(i + 1)
            lines[i+1] = lines[i+1].replace("*/", "").strip()    
    return lines

def place_braces_on_new_lines(lines):
    """Place braces on new lines (Rule CL1)
    Args:
        lines: List of source code lines
    Returns:
        lines: All lines including conrrected lines
    """
    for i, line in enumerate(lines):
        # ToDo: Does not check if it contains { with text after it
        if ('{' in line.strip() and len(line.strip()) > 1) and not '}' in line.strip():
            if(DEBUG):print(f"Removing brace from line {i}, and placing it on line {i + 1}")
            # Check if there is there is text after the brace
            if line.strip().endswith("{"):
                # Remove the brace from the current line
                lines[i] = line.replace("{", "")
            else:
                # Remove the brace from the current line
                temp = line.split("{")
                lines[i] = temp[0]
                lines[i] = line.replace("{", "")
                lines.insert(i+1, temp[1])
            # get the indentation of the current line
            indentation = re.match(r"^\s*", line).group(0)
            # Place the brace on the next line with indentation
            lines.insert(i+1, indentation + "{")
    return lines

def convert_variable_names_to_hungarian_notation(lines):
    """Convert variable names to Hungarian notation (Rule DV3)
    Args:
        lines: List of source code lines
    Returns:
        lines: All lines including conrrected lines
    """

    # Define Hungarian notation prefixes
    type_prefixes = {
        'int': 'i',
        'float': 'f',
        'double': 'd',
        '_Bool': 'b',
        'short': 'si',
        'signed char': 'c',
        'char': 'c',
        'short int': 'si',
        'long int': 'li',
        'long long int': 'lli',
        'long double': 'ld',
        'unsigned short int': 'usi',
        'unsigned char': 'uc',
        'unsigned int': 'ui',
        'unsigned long int': 'uli',
        'unsigned long long int': 'ulli',
    }

    sorted_types = sorted(type_prefixes.keys(), key=lambda x: len(x), reverse=True)
    # Define regex pattern for variable declarations
    var_decl_pattern = re.compile(r'(\b(?:' + '|'.join(sorted_types) + r')\s*\**?\s+)(\w+)\s*=')
    # Patterns to compare after variable declaration pattern is compared to determine extra declarations
    # Define regex pattern for pointer declarations
    pointer_decl_pattern = re.compile(r'(\b(?:' + '|'.join(type_prefixes.keys()) + r')\*+)')
    # Define regex pattern for array declarations
    array_decl_pattern = re.compile(r'(\b(?:' + '|'.join(type_prefixes.keys()) + r')\s+\w+\s*\[\s*\d+\s*\])')
    # if wrongly declared variable is found, it will be added to this dict with the correct name to find all occurrences of them later to replace with correct names
    wrong_var_names = {}
    for i, line in enumerate(lines):
        # Check for variable declarations
        match = var_decl_pattern.search(line)
        if match:
            if(DEBUG):print(f"Checking line {i + 1}: {line.strip()}\tMatch: {match}")
            # Check for pointer or array declarations
            pointer_match = pointer_decl_pattern.search(line)
            array_match = array_decl_pattern.search(line)
            # Extract the variable type and name
            var_type = match.group(1).strip()
            var_name = match.group(2).strip()
            if(DEBUG):print(f"Variable type: {var_type}, Variable name: {var_name}")
            # Expected prefix for the variable type
            expected_prefix = type_prefixes.get(var_type, '')
            if array_match:
                # If it's an array, add 'a' prefix
                expected_prefix = 'a' + expected_prefix
            if pointer_match:
                # If it's a pointer, add 'p' prefix
                expected_prefix = 'p' + expected_prefix
            # Check if the variable name is already in Hungarian notation
            if not var_name.startswith(expected_prefix):
                # Convert to Hungarian notation
                new_var_name = type_prefixes[var_type.replace('*','')] + var_name[0].upper() + var_name[1:]
                if array_match:
                    new_var_name = 'a' + new_var_name
                if pointer_match:
                    new_var_name = 'p' + new_var_name
                wrong_var_names[var_name] = new_var_name
                lines[i] = line.replace(var_name, new_var_name)
                if(DEBUG):print(f"Converting variable name '{var_name}' to '{new_var_name}' at line {i + 1}")
    # Replace all occurrences of the wrong variable names with the correct ones
    for i, line in enumerate(lines):
        for wrong_name, correct_name in wrong_var_names.items():
            if wrong_name in line:
                lines[i] = line.replace(wrong_name, correct_name)
                if(DEBUG):print(f"Replacing '{wrong_name}' with '{correct_name}' at line {i + 1}")

    return lines

# --------------------------
# Main Program Logic
# --------------------------


# Map rule IDs to check functions (exept for A5 - filename conversion is handled separately)
CHECKS = {
    'A4': convert_block_comments_to_single_line,
    'CL1': place_braces_on_new_lines,
    'DV3': convert_variable_names_to_hungarian_notation
}

def print_checks(requested_checks=None):
    """Print available checks and their descriptions"""
    if requested_checks is None:
        print("Available checks:")
        for check_id, check_func in CHECKS.items():
            print(f"  - {check_id}: {check_func.__doc__.strip().splitlines()[0]}")
        return
    print("Requested checks:")
    for check_id in requested_checks:
        if check_id in CHECKS:
            print(f"  - {check_id}: {CHECKS[check_id].__doc__.strip().splitlines()[0]}")
        else:
            print(f"  - {check_id}: Not a valid check ID")

def convert_file(file_path, filename, checks):
    """Convert a file based on the specified checks"""
    print(f"\nConverting file {filename} in directory: {file_path}")
    with open(os.path.join(file_path, filename), 'r') as file:
        content = file.read()
    lines = content.splitlines()
    for check in checks:
        if check in CHECKS:
            print(f"Running check {check} on file {filename}")
            lines = CHECKS[check](lines)
    
    out = os.path.join(file_path, "output")
    if not os.path.exists(out):
        os.makedirs(out)
    # Convert filename (Rule A5)
    filename = convert_filename_to_uppercase(filename)
    out = os.path.join(out, filename)
    with open(out, 'w') as file:
        file.write("\n".join(lines))
    print(f"Converted file saved as {out}")

def convert_directory(directory, checks):
    """Convert all files in a directory based on the specified checks"""
    print(f"Converting files in directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.c') or file.endswith('.h'):
                convert_file(root, file, checks)

def main():
    if len(sys.argv) < 2:
        print("Usage: python style_converter.py <directory> [CHECKS...]")
        print_checks()
        print("If no checks are specified, all checks will be run.")
        sys.exit(1)

    directory = sys.argv[1]
    checks = sys.argv[2:] if len(sys.argv) > 2 else CHECKS.keys()
    
    # Validate requested checks
    invalid = [c for c in checks if c not in CHECKS]
    if invalid:
        print(f"Invalid check IDs: {', '.join(invalid)}")
        print(f"Available checks: {', '.join(CHECKS.keys())}")
        sys.exit(1)

    isFile = False;

    # Validate target directory
    if not os.path.isdir(directory):
        if not os.path.isfile(directory) and not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory or file.")
            sys.exit(1)
        else:
            isFile = True;
    if not os.access(directory, os.W_OK):
        print(f"Error: {directory} is not writable.")
        sys.exit(1)
    if not os.access(directory, os.R_OK):
        print(f"Error: {directory} is not readable.")
        sys.exit(1)

    if isFile:
        # Convert a single file
        dir = os.path.dirname(directory)
        file = os.path.basename(directory)
        convert_file(dir, file, checks)
        sys.exit(0)
    else:
        # Convert all files in the directory
        convert_directory(directory, checks)
        sys.exit(0)

if __name__ == "__main__":
    main()