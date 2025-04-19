import re
import os
import sys

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



# --------------------------
# Main Program Logic
# --------------------------

# Map rule IDs to check functions
CHECKS = {
    'A4': check_block_comments,
    'A7': check_file_length,
    'CL1': check_brace_placement,
    'CL5': check_operator_spacing
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
        print("Available checks:")
        for check in CHECKS:
            print(f"  - {check}: {CHECKS[check].__doc__.strip().splitlines()[0]}")
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
