import os


def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def update_step_place(step_path: str, new_place: int, ignore_unexists: bool = False):
    if not step_path or not isinstance(step_path, str):
        raise ValueError('Path must be a not empty string')
    if not os.path.exists(step_path) and ignore_unexists:
        raise FileNotFoundError('File not found')

    lesson_path, filename = os.path.split(step_path)
    first_index = filename.find('_')
    new_path = os.path.join(
        lesson_path,
        f'{filename[:first_index]}_{new_place}{filename[filename.find('_', first_index+1):]}',
    )
    os.rename(step_path, new_path)

    return new_path


