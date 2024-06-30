import os



def read_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    return file_data


def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension in ['.pdf']:
        return 'pdf'
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return 'image'
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")