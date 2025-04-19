import re
import os
import sys

# Verbose mode for debugging
DEBUG = False

# --------------------------
# Style Check Implementations
# --------------------------


def check_block_comments(lines, filename):
    """Verify only single-line comments are used (Rule A4)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    in_block_comment = False
    for i, line in enumerate(lines, 1):
        if '/*' in line:
            in_block_comment = True
            issues.append(f"Line {i}: Block comment started (violates A4)")
        if '*/' in line:
            in_block_comment = False
    return issues

def check_uppercase_filename(lines, filename):
    """Verify file names start with uppercase letter (Rule A5)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    if filename.endswith(('.c', '.h')):  # Only check C/C++ files
        base_name = os.path.splitext(filename)[0]
        if not base_name[0].isupper():
            issues.append(f"Filename {filename} does not start with uppercase letter (violates A5)")
    return issues

def check_function_length(lines, filename):
    """Check that functions are not longer than 40 lines (Rule A6)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    if not filename.endswith(('.c', '.cpp')):
        return issues  # Only check C/C++ implementation files
        
    in_function = False
    function_start_line = 0
    function_name = ""
    brace_count = 0
    
    # Function signature detection regex
    func_signature = re.compile(r'^\s*\w+\s+(\w+)\s*\([^)]*\)\s*({?)$')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1  # Increment line counter
        
        # Skip preprocessor directives, comments, and empty lines
        if not line or line.startswith('#') or line.startswith('//'):
            continue
            
        # Function definition detection
        if not in_function:
            match = func_signature.match(line)
            if match:
                function_name = match.group(1)
                function_start_line = i
                
                # If opening brace not on this line, look for it
                if not match.group(2):
                    # Find the opening brace
                    for j in range(i, min(i+5, len(lines))):  # Look ahead a few lines
                        if '{' in lines[j]:
                            in_function = True
                            brace_count = 1
                            break
                else:
                    in_function = True
                    brace_count = 1
                
        # Inside function tracking
        elif in_function:
            brace_count += line.count('{')
            brace_count -= line.count('}')
            
            # End of function detection
            if brace_count == 0:
                function_length = i - function_start_line + 1
                if function_length > 40:
                    issues.append(f"Function '{function_name}' has {function_length} lines (violates A6: 4-40 lines)")
                in_function = False
    
    return issues

def check_file_length(lines, filename):
    """Validate C file line count (Rule A7)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    if filename.endswith('.c') and (len(lines) < 4 or len(lines) > 400):
        issues.append(f"File length {len(lines)} violates A7 (4-400 lines)")
    return issues

def check_file_structure(lines, filename):
    """Verify C file structure follows the required order (Rule A8)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    if not filename.endswith('.c'):
        return []  # Only check C files
        
    issues = []
    
    # Define section markers with their patterns
    section_patterns = {
        'system_headers': re.compile(r'^\s*#include\s*<.*>'),
        'user_headers': re.compile(r'^\s*#include\s*".*"'),
        'data_types': re.compile(r'^\s*(#define|const|enum|struct|union|typedef)'),
        'function_declarations': re.compile(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^{]*\)\s*;'),
        'function_implementations': re.compile(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^;]*\)\s*({|$)')
    }
    
    # Track sections in order of appearance
    section_order = []
    
    # Process the file line by line
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        # Skip empty lines and comments
        if not line or line.startswith('//'):
            continue
            
        # Check which section this line belongs to
        for section, pattern in section_patterns.items():
            if pattern.match(line):
                if section not in section_order:
                    # Debug print section order and line
                    if DEBUG:print(f"Found section '{section}' in {filename} at line {i}")
                    section_order.append(section)
                break
    
    # Check if main is the first implemented function
    main_found = False
    first_func = None
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            continue
            
        match = re.search(r'^\s*(\w+)\s+(\w+)\s*\(', line)
        if match and match.group(2) == 'main':
            main_found = True
            if first_func and first_func != 'main':
                issues.append(f"Main is not the first implemented function (violates A8)")
            break
        elif match and section_patterns['function_implementations'].match(line):
            if first_func is None:
                first_func = match.group(2)
    
    # Expected section order
    expected_order = ['system_headers', 'user_headers', 'data_types', 'globals', 
                     'function_declarations', 'function_implementations']
    
    # Check if sections appear in correct order
    last_section_idx = -1

    # Debug print section order
    if DEBUG:print(f"Section order in {filename}: {section_order}")
    if DEBUG:print(f"Expected order: {expected_order}")

    for section in section_order:
        current_idx = expected_order.index(section)
        if current_idx < last_section_idx:
            issues.append(f"File structure violates A8: {section} appears after {expected_order[last_section_idx]}")
        last_section_idx = current_idx
    
    return issues

def check_brace_placement(lines, filename):
    """Verify proper brace positioning (Rule CL1)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check for opening brace on a new line
        if '{' in stripped and not (stripped.startswith('{') or '=' in stripped):
                issues.append(f"Line {i}: Opening brace are not on a new line (violates CL1)")
    return issues

def check_operator_spacing(lines, filename):
    """Check operator spacing consistency (Rule CL5)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    operator_pattern = re.compile(r'(\S)(==|!=|<=|>=|=|\+|-|\*|/|&&|\|\|)(\S)')
    for i, line in enumerate(lines, 1):
        for match in operator_pattern.finditer(line):
            left_space = match.start(1) > 0 and line[match.start(1)-1] != ' '
            right_space = match.end(3) < len(line) and line[match.end(3)] != ' '
            # Check for spaces around the operator
            if left_space or right_space:
                # Check if its in a string
                if not (line[:match.start(1)].count('"') % 2 == 0 and line[:match.start(1)].count("'") % 2 == 0):
                    continue
                # Check if its in a comment
                if not (line[:match.start(1)].count('//') % 2 == 0 and line[:match.start(1)].count('/*') % 2 == 0):
                    continue
                # Check if its in a preprocessor directive
                if not (line[:match.start(1)].count('#') % 2 == 0):
                    continue
                # Check if its a pointer
                if not (line[:match.start(1)].count('*') % 2 == 0):
                    continue
                # Check if its a primary expression
                if not (line[:match.start(1)].count('(') % 2 == 0 and line[:match.start(1)].count(')') % 2 == 0):
                    continue
                # Check if its an unary expression
                if not (line[:match.start(1)].count('!') % 2 == 0 and line[:match.start(1)].count('&') % 2 == 0):
                    continue
                issues.append(f"Line {i}: Missing spaces around operator '{match.group(2)}' (violates CL5)")
    return issues

def check_hungarian_notation(lines, filename):
    """Check that variable names use Hungarian notation (Rule DV3 II)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    if not (filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.cpp')):
        return []
        
    issues = []
    
    # Define Hungarian notation prefixes
    type_prefixes = {
        'short': 'si',
        'signed char': 'c',
        'unsigned short int': 'usi',
        'unsigned char': 'uc',
        'int': 'i',
        'float': 'f',
        'unsigned int': 'ui',
        'double': 'd',
        'long int': 'li',
        'long double': 'ld',
        'unsigned long int': 'uli',
        '_Bool': 'b',
        'long long int': 'lli',
        'unsigned long long int': 'ulli'
    }
    
    # Check for prefix in variable name and then checks if it is declared 
    # if variable is declared without the prefix in its name than it is a violation
    for i, line in enumerate(lines, 1):
        line = line.strip()
        # Skip empty lines and comments
        if not line or line.startswith('//') or line.startswith('#') or line.startswith('/*') or line.startswith('*'):
            continue
        # Skip lines that are not variable declarations
        if not '=' in line:
            continue
        # Check if the line contains a variable declaration
        if any(line.startswith(prefix) for prefix in type_prefixes.keys()):
            # Split the line to get the variable declaration part
            declaration = line.split('=')[0]
            declaration = re.sub(r'\s+', ' ', declaration)
            declaration = declaration.strip()
            parts = declaration.split(' ')
            if len(parts) < 2:
                continue
            var_type = ' '.join(parts[:-1])
            var_name = parts[-1]
            # Check if the type is in the Hungarian notation prefixes
            if var_type in type_prefixes:
                prefix = type_prefixes[var_type]
                # Check if the variable name starts with the prefix
                if not var_name.startswith(prefix):
                    issues.append(f"Line {i}: Variable '{var_name}' does not follow Hungarian notation for '{var_type}' (violates DV3 II)")
            else:
                issues.append(f"Line {i}: Unknown type '{var_type}' (violates DV3 II)")

    return issues


# --------------------------
# Main Program Logic
# --------------------------

# Map rule IDs to check functions
CHECKS = {
    'A4': check_block_comments,
    'A5': check_uppercase_filename,
    'A6': check_function_length,
    'A7': check_file_length,
    'A8': check_file_structure,
    'CL1': check_brace_placement,
    'CL5': check_operator_spacing,
    'DV3': check_hungarian_notation
}


def process_file(file_path, enabled_checks):
    """Run enabled style checks on a single file
    Args:
        file_path: Path to source file
        enabled_checks: List of check IDs to execute
    Returns:
        List of all detected issues
    """
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
            filename = os.path.basename(file_path)
            
            for check_id in enabled_checks:
                if check_id in CHECKS:
                    issues += CHECKS[check_id](lines, filename)
    except UnicodeDecodeError:
        issues.append("File encoding error - unable to process")
    return issues

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

def main():
    """Main entry point for style checker"""
    if len(sys.argv) < 2:
        print("Usage: python style_checker.py <directory> [CHECKS...]")
        print_checks()
        print("If no checks are specified, all checks will be run.")
        sys.exit(1)

    target_dir = sys.argv[1]
    requested_checks = sys.argv[2:] if len(sys.argv) > 2 else CHECKS.keys()
    
    # Validate requested checks
    invalid = [c for c in requested_checks if c not in CHECKS]
    if invalid:
        print(f"Invalid check IDs: {', '.join(invalid)}")
        print(f"Available checks: {', '.join(CHECKS.keys())}")
        sys.exit(1)

    # Validate target directory
    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a valid directory.")
        sys.exit(1)
    if not os.access(target_dir, os.R_OK):
        print(f"Error: {target_dir} is not readable.")
        sys.exit(1)

    # Process files
    print(f"Target directory: {target_dir}")
    print_checks(requested_checks)
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h')):
                print(f"\nProcessing {file}...")
                file_path = os.path.join(root, file)
                issues = process_file(file_path, requested_checks)
                if issues:
                    print(f"Issues in {file_path}:")
                    for issue in issues:
                        print(f"  - {issue}")
                else:
                    print(f"No issues found in {file_path}")
    print("\nStyle check completed.")

if __name__ == "__main__":
    main()
