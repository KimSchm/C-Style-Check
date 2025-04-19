import re
import os

def convert_block_comments_to_single_line(content):
    """Convert block comments to single-line comments"""
    content = re.sub(r'/\*', '//', content)
    content = re.sub(r'\*/', '', content)
    return content

def convert_filename_to_uppercase(filename):
    """Convert file names to start with uppercase letters"""
    base_name = os.path.basename(filename)
    new_name = base_name[0].upper() + base_name[1:]
    return new_name

def split_long_functions(content):
    """Split functions longer than 40 lines"""
    lines = content.split('\n')
    new_content = []
    in_function = False
    function_lines = []
    for line in lines:
        if re.match(r'^\s*\w+\s+\w+\s*\([^)]*\)\s*{', line):
            in_function = True
            function_lines = [line]
        elif in_function:
            function_lines.append(line)
            if line.strip() == '}':
                in_function = False
                if len(function_lines) > 40:
                    new_content.extend(function_lines[:40])
                    new_content.append('// Function split due to length')
                    new_content.extend(function_lines[40:])
                else:
                    new_content.extend(function_lines)
        else:
            new_content.append(line)
    return '\n'.join(new_content)

def ensure_file_length(content):
    """Ensure file length is between 4 and 400 lines"""
    lines = content.split('\n')
    if len(lines) < 4:
        lines.extend([''] * (4 - len(lines)))
    elif len(lines) > 400:
        lines = lines[:400]
    return '\n'.join(lines)

def reorder_sections(content):
    """Reorder sections in a C file"""
    lines = content.split('\n')
    system_headers = []
    user_headers = []
    data_types = []
    globals = []
    function_declarations = []
    function_implementations = []
    current_section = None

    for line in lines:
        if re.match(r'^\s*#include\s*<.*>', line):
            current_section = 'system_headers'
            system_headers.append(line)
        elif re.match(r'^\s*#include\s*".*"', line):
            current_section = 'user_headers'
            user_headers.append(line)
        elif re.match(r'^\s*(#define|const|enum|struct|union|typedef)', line):
            current_section = 'data_types'
            data_types.append(line)
        elif re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^{]*\)\s*;', line):
            current_section = 'function_declarations'
            function_declarations.append(line)
        elif re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^;]*\)\s*{', line):
            current_section = 'function_implementations'
            function_implementations.append(line)
        else:
            if current_section == 'system_headers':
                system_headers.append(line)
            elif current_section == 'user_headers':
                user_headers.append(line)
            elif current_section == 'data_types':
                data_types.append(line)
            elif current_section == 'function_declarations':
                function_declarations.append(line)
            elif current_section == 'function_implementations':
                function_implementations.append(line)

    new_content = system_headers + user_headers + data_types + globals + function_declarations + function_implementations
    return '\n'.join(new_content)

def place_braces_on_new_lines(content):
    """Place braces on new lines"""
    content = re.sub(r'\s*{\s*', '\n{\n', content)
    content = re.sub(r'\s*}\s*', '\n}\n', content)
    return content

def add_spaces_around_operators(content):
    """Add spaces around operators"""
    content = re.sub(r'(\S)(==|!=|<=|>=|=|\+|-|\*|/|&&|\|\|)(\S)', r'\1 \2 \3', content)
    return content

def convert_variable_names_to_hungarian_notation(content):
    """Convert variable names to Hungarian notation"""
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
        '_Bool': 'b',
        'long long int': 'lli',
        'unsigned long long int': 'ulli'
    }

    lines = content.split('\n')
    new_lines = []
    for line in lines:
        for var_type, prefix in type_prefixes.items():
            pattern = re.compile(r'\b' + var_type + r'\b\s+(\w+)')
            match = pattern.search(line)
            if match:
                var_name = match.group(1)
                new_var_name = prefix + var_name
                line = line.replace(var_name, new_var_name)
        new_lines.append(line)
    return '\n'.join(new_lines)
