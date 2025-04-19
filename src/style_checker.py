import re
import os
import sys

# --------------------------
# Style Check Implementations
# --------------------------

def check_tabs(lines, filename):
    """Check for tab characters in source code (Rule A1)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    for i, line in enumerate(lines, 1):
        if '\t' in line:
            issues.append(f"Line {i}: Tab character found (violates A1)")
    return issues

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
        if stripped == '{' and i > 1:
            prev_line = lines[i-2].strip()
            if not (prev_line.endswith(')') or prev_line.endswith('{') or prev_line.endswith('}')):
                issues.append(f"Line {i}: Opening brace on new line (violates CL1)")
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
        if operator_pattern.search(line):
            issues.append(f"Line {i}: Missing spaces around operator (violates CL5)")
    return issues

def check_variable_naming(lines, filename):
    """Validate variable prefix conventions (Rule DV1)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    type_prefixes = {
        'int': 'i', 'float': 'f', 'double': 'd', 'char': 'c',
        'short': 's', 'long': 'l', 'uint32_t': 'u32', 'int32_t': 's32'
    }
    var_decl_pattern = re.compile(
        r'\b(int|float|double|char|short|long|uint32_t|int32_t)\s+(?:const\s+)?(\w+)\b'
    )
    for i, line in enumerate(lines, 1):
        match = var_decl_pattern.search(line)
        if match:
            var_type, var_name = match.groups()
            prefix = type_prefixes.get(var_type, '')
            if not var_name.startswith(prefix):
                issues.append(f"Line {i}: Variable '{var_name}' should start with '{prefix}' (violates DV1)")
    return issues

def check_header_guards(lines, filename):
    """Verify proper header guard usage (Rule P1)
    Args:
        lines: List of source code lines
        filename: Name of current file
    Returns:
        List of violation messages
    """
    issues = []
    if filename.endswith('.h'):
        expected_guard = filename.upper().replace('.', '_')
        if len(lines) < 2 or not lines[0].startswith(f'#ifndef {expected_guard}') or not lines[1].startswith(f'#define {expected_guard}'):
            issues.append("Missing or incorrect header guard (violates P1)")
    return issues

# --------------------------
# Main Program Logic
# --------------------------

# Map rule IDs to check functions
CHECKS = {
    'A1': check_tabs,
    'A4': check_block_comments,
    'A7': check_file_length,
    'CL1': check_brace_placement,
    'CL5': check_operator_spacing,
    'DV1': check_variable_naming,
    'P1': check_header_guards
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

def main():
    """Main entry point for style checker"""
    if len(sys.argv) < 2:
        print("Usage: python style_checker.py <directory> [CHECKS...]")
        print("Available checks: " + ", ".join(CHECKS.keys()))
        sys.exit(1)

    target_dir = sys.argv[1]
    requested_checks = sys.argv[2:] if len(sys.argv) > 2 else CHECKS.keys()
    
    # Validate requested checks
    invalid = [c for c in requested_checks if c not in CHECKS]
    if invalid:
        print(f"Invalid check IDs: {', '.join(invalid)}")
        print(f"Available checks: {', '.join(CHECKS.keys())}")
        sys.exit(1)

    # Process files
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h')):
                file_path = os.path.join(root, file)
                issues = process_file(file_path, requested_checks)
                if issues:
                    print(f"\nIssues in {file_path}:")
                    for issue in issues:
                        print(f"  - {issue}")

if __name__ == "__main__":
    main()
