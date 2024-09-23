import re

# Updated regex patterns
patterns = {
    'a': r"^- \([a-z]\)",                # Matches - (a), - (b), ..., - (z)
    '1': r"^- \([0-9]{1,3}\)",           # Matches - (1), - (2), ..., up to (999)
    'roman_i': r"^- \([i]\)",            # Matches - (i)
    'roman_v': r"^- \([v]\)",            # Matches - (v)
    'roman_x': r"^- \([x]\)",            # Matches - (x)
    '*1*': r"^- \(\*[0-9]{1,3}\*\)",     # Matches - (*1*), (*2*), ..., up to (*999*)
    '*roman*': r"^- \(\*[ivxl]+\*\)",    # Matches - (*i*), (*ii*), (*iii*), etc.
    '*a*': r"^- \(\*[a-z]\*\)",          # Matches - (*a*), (*b*), etc.
    'roman_higher': r"^- \([ivxlcdm]{2,}\)",  # Matches Roman numerals with 2 or more letters
    'roman': r"^- \([ivx]+\)",           # Matches any Roman numeral
    'first_letter_uppercase': r"^- \*[A-Z].*",  # Matches lines starting with '- *' and uppercase letter
    'A': r"^- \([A-Z]\)",                # Matches - (A), - (B), ..., - (Z)
    'neither_w_nor_1': r"^- \([^1w][^\)]*\)",  # neither 1 nor w
    'neither_x_nor_1': r"^- \([^1x][^\)]*\)",  # neither 1 nor x
    'line_starts_with_uppercase': r"^- [A-Z].*"  # Matches lines starting with - and an uppercase letter
}

def is_a_pattern_found_before(lines, current_index):
    for i in range(current_index - 1, -1, -1):
        previous_line = lines[i].strip()
        if re.match(patterns['a'], previous_line):
            return True
        elif re.match(patterns['A'], previous_line) or re.match(patterns['1'], previous_line):
            # If we hit an upper-level pattern, stop searching
            return False
    return False

def get_indent_level(line, previous_line, next_line, lines, current_index):
    line = line.strip()

    # Uppercase letters (A-Z)
    if re.match(patterns['A'], line):
        return 12

    # Numbers (1-999)
    elif re.match(patterns['1'], line):
        return 4

    elif re.match(patterns['*1*'], line):
        return 16

    elif re.match(patterns['*roman*'], line):
        return 20

    elif re.match(patterns['*a*'], line):
        return 12

    # Lines starting with '- *' and uppercase letter
    elif re.match(patterns['first_letter_uppercase'], line):
        if is_a_pattern_found_before(lines, current_index):
            return 4  # Indent under '- (a)'
        else:
            return 0  # No indentation

    # Line starts with (i)
    elif re.match(patterns['roman_i'], line):
        # Combined condition: if previous line is a number and next line is Roman numeral (i)
        if re.match(patterns['1'], previous_line) and re.match(patterns['roman_i'], next_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['1'], previous_line) and re.match(patterns['A'], next_line):
            return 8
        elif re.match(patterns['1'], previous_line) and re.match(patterns['roman'], next_line):
            return 8
        elif re.match(patterns['1'], previous_line) and re.match(patterns['*a*'], next_line):
            return 8
        elif re.match(patterns['first_letter_uppercase'], previous_line) and re.match(patterns['roman'], next_line):
            return 8
        else:
            return 0  # Treat as letter

     # Line starts with (v)
    elif re.match(patterns['roman_v'], line):
        # Combined condition: if previous line is a number and next line is Roman numeral (v)
        if re.match(patterns['roman'], previous_line) and re.match(patterns['roman'], next_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['roman'], previous_line) and re.match(patterns['A'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['roman'], previous_line) and re.match(patterns['1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['A'], previous_line) and re.match(patterns['neither_w_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*a*'], previous_line) and re.match(patterns['neither_w_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*1*'], previous_line) and re.match(patterns['neither_w_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*roman*'], previous_line) and re.match(patterns['neither_w_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['roman_higher'], previous_line) and re.match(patterns['neither_w_nor_1'], next_line):
            return 8  # roman numeral
        else:
            return 0  # Treat as letter

    # Line starts with (x)
    elif re.match(patterns['roman_x'], line):
        # Combined condition: if previous line is a number and next line is Roman numeral (v)
        if re.match(patterns['roman_higher'], previous_line) and re.match(patterns['roman_higher'], next_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['roman_higher'], previous_line) and re.match(patterns['A'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['roman_higher'], previous_line) and re.match(patterns['1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['A'], previous_line) and re.match(patterns['neither_x_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*a*'], previous_line) and re.match(patterns['neither_x_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*1*'], previous_line) and re.match(patterns['neither_x_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['*roman*'], previous_line) and re.match(patterns['neither_x_nor_1'], next_line):
            return 8  # roman numeral
        elif re.match(patterns['roman_higher'], previous_line):
            return 8  # roman numeral
        else:
            return 0  # Treat as letter

    # Other Roman numerals (ii, iii, etc.)
    elif re.match(patterns['roman_higher'], line):
        # Indent if previous line is a Roman numeral
        if re.match(patterns['roman'], previous_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['A'], previous_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['*a*'], previous_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['*1*'], previous_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['*roman*'], previous_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['line_starts_with_uppercase'], previous_line) and re.match(patterns['A'], next_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['line_starts_with_uppercase'], previous_line) and re.match(patterns['roman_higher'], next_line):
            return 8  # Indent as Roman numeral
        elif re.match(patterns['line_starts_with_uppercase'], previous_line) and re.match(patterns['*a*'], next_line):
            return 8  # Indent as Roman numeral
        else:
            return 0  # Treat as letter

    # Lowercase letters (a-z), excluding (i)
    elif re.match(patterns['a'], line):
        return 0

    else:
        return 0

def indent_text(text):
    indented_text = []
    lines = text.strip().splitlines()
    num_lines = len(lines)

    for index, line in enumerate(lines):
        line = line.strip()
        previous_line = lines[index - 1].strip() if index >= 1 else ""
        next_line = lines[index + 1].strip() if index + 1 < num_lines else ""
        indent_level = get_indent_level(line, previous_line, next_line, lines, index)
        indented_text.append(' ' * indent_level + line)

    return "\n".join(indented_text)

# Function to allow user to input multiple lines and stop on double Enter
def get_multiline_input():
    print("Please enter the text to be indented (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            if len(lines) > 0 and lines[-1] == "":
                break
            lines.append(line)
        else:
            lines.append(line)
    return "\n".join(lines)

# Get multi-line input from user
user_input = get_multiline_input()

# Process the user's input text
indented_output = indent_text(user_input)
print("\nIndented Output:\n")
print(indented_output)
