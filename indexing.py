import requests
import re

file_paths = [
    "C1.csv",
    "C2.txt"
]

username = "bolphine"
repository = "datasets"
branch = "main"

word_index = 1  # Initialize word index

word_index_mapping = {}  # Dictionary to store word-index mapping

for file_path in file_paths:
    url = f"https://raw.githubusercontent.com/{username}/{repository}/{branch}/{file_path}"

    response = requests.get(url)
    response.raise_for_status()

    file_extension = file_path.split(".")[-1]

    file_name = file_path.split("/")[-1]
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response.text)

    if file_extension == "csv":
        import csv

        # Open the CSV file
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if it exists

            indexed_rows = []  # List to store indexed rows
            unique_words = set()

            for row in reader:
                line_num = int(row[0])
                speaker = f"Speaker {line_num % 2 + 1}"
                dialogue = row[1]

                print(f"{speaker}: {dialogue}")

                cleaned_dialogue = re.sub(r"[^\w\s]", "", dialogue)  # Remove punctuation and non-word characters

                # Replace words with their respective index numbers
                indexed_dialogue = []
                for word in cleaned_dialogue.split():
                    if word not in word_index_mapping:
                        word_index_mapping[word] = word_index
                        word_index += 1

                    indexed_dialogue.append(str(word_index_mapping[word]))

                indexed_rows.append(indexed_dialogue)
                unique_words.update(cleaned_dialogue.split())

            unique_words_file = f"{file_name}_unique_words.txt"
            with open(unique_words_file, 'w', encoding='utf-8') as unique_file:
                for word, index in word_index_mapping.items():
                    unique_file.write(f"{index}: {word}\n")

            print("Unique Words saved to:", unique_words_file)
            print()

            # Save indexed dialogue to a new file
            indexed_file = f"{file_name}_indexed.{file_extension}"
            with open(indexed_file, 'w', encoding='utf-8') as indexed_dialogue_file:
                for indexed_dialogue in indexed_rows:
                    indexed_dialogue_file.write(" ".join(indexed_dialogue) + '\n')

            print("Indexed dialogue saved to:", indexed_file)

    elif file_extension == "txt":
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            indexed_lines = []  # List to store indexed lines
            unique_words = set()

            for line in file:
                line = line.strip().replace("\n", "")
                if line:
                    print(line)
                    cleaned_line = re.sub(r"[^\w\s]", "", line)  # Remove punctuation and non-word characters

                    # Replace words with their respective index numbers
                    indexed_line = []
                    for word in cleaned_line.split():
                        if word not in word_index_mapping:
                            word_index_mapping[word] = word_index
                            word_index += 1

                        indexed_line.append(str(word_index_mapping[word]))

                    indexed_lines.append(indexed_line)
                    unique_words.update(cleaned_line.split())

            unique_words_file = f"{file_name}_unique_words.txt"
            with open(unique_words_file, 'w', encoding='utf-8') as unique_file:
                for word, index in word_index_mapping.items():
                    unique_file.write(f"{index}: {word}\n")

            print("Unique Words saved to:", unique_words_file)
            print()

            # Save indexed lines to a new file
            indexed_file = f"{file_name}_indexed.{file_extension}"
            with open(indexed_file, 'w', encoding='utf-8') as indexed_lines_file:
                for indexed_line in indexed_lines:
                    indexed_lines_file.write(" ".join(indexed_line) + '\n')

            print("Indexed lines saved to:", indexed_file)

    else:
        print(f"Unsupported file format: {file_extension}")
