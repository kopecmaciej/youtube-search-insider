import pathlib


def open_or_create(file_path: str, file_mode: str):
    path = pathlib.Path(file_path)
    if path.exists():
        print(f"File {file_path} already exists")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)

    return open(file_path, file_mode)

def write_json(data, file_path):
    with open_or_create(file_path, 'w') as file:
        file.write(data)
