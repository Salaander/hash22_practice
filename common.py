import os

def get_file(file_name: str) -> str:
    abs_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(abs_path, file_name)