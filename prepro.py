import requests


file_paths = [
    "C1.csv",
    "C2.txt"
]


username = "bolphine"
repository = "datasets"
branch = "main"

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

        qa_list = []

        with open('C1.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                qa_list.append(row[1])

        for qa in qa_list:
            print(qa)

    elif file_extension == "txt":
        with open('C2.txt', 'r', encoding='utf-8-sig') as file:
            for line in file:
                if ':' in line:
                    qa = line.split(':')[-1].strip()
                    print(qa)

    else:
        print(f"Unsupported file format: {file_extension}")
