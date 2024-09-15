import re

def remove_references_and_patterns(input_file, output_file):
    # Open the input file with utf-8 encoding and read its content
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Remove occurrences of [N] where N is a number
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    
    # Remove occurrences of '© 2024 - batas.org | N' where N is a number
    cleaned_text = re.sub(r'© 2024 - batas\.org \|\s*\d+', '', cleaned_text)
    
    # Remove occurrences of 'Id.' followed by anything (e.g., 'Id. at 393-394.')
    cleaned_text = re.sub(r'Id\.\s?.*', '', cleaned_text)
    
    # Write the cleaned text to the output file with utf-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"References, patterns, and 'Id.' phrases removed. Cleaned text saved to {output_file}")

file = r'annotations\163.txt'  # Update with your actual file path

remove_references_and_patterns(file, file)