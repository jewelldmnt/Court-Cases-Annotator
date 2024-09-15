for i in range(126, 186):  # Loop from 36 to 100 inclusive
    file_name = f"annotations\{i}.txt"  # Create the file name, e.g., "36.txt"
    with open(file_name, 'w') as file:
        file.write("")  # Create an empty file or add content if needed
    print(f"Created: {file_name}")