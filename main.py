from pathlib import Path
import hashlib

dir_path = './target/'

directory = Path(dir_path)

def calculate_hash(file_path, file_size):
    chunk_size = 4096
    try:
        with open(file_path, 'rb') as file:
            hash_obj = hashlib.sha256()

            while True:
                chunk = file.read(chunk_size)

                if not chunk:
                    break
                
                hash_obj.update(chunk)

        current_size = Path(file_path).stat().st_size

        if current_size == file_size:
            return hash_obj.hexdigest()
        else:
            return False

    except (FileNotFoundError, PermissionError):
        return None



if directory.exists():
    # Dictionary used to group files of same size.
    files_dict = {}

    # Recursively iterate through all files and directories.
    for item in directory.rglob("*"):
        # Process only files, directories ignored
        if item.is_file():
            item_size = item.stat().st_size
            # Group files that have same size
            files_dict.setdefault(item_size, []).append(item)

    # Dictionary used to group potential duplicates by their hash.
    hashes_dict = {}
    # Lists to handle some special cases
    not_hashed = []
    files_changed = []

    for size_group in files_dict:
        if len(files_dict[size_group]) > 1:
            for file in files_dict[size_group]:
                file_size = file.stat().st_size
                file_hash = calculate_hash(file, file_size)
                if file_hash is None:
                    not_hashed.append(file)
                elif file_hash is False:
                    files_changed.append(file)
                else:
                    hashes_dict.setdefault(file_hash, []).append(file)

    
    for hash_group in hashes_dict:
        if len(hashes_dict[hash_group]) > 1:
            print("Duplicate Group:")
            for duplicate_file in hashes_dict[hash_group]:
                print(duplicate_file)
            print('\n')

    if not_hashed:
        print("These files can't be accessed.")
        for unhashed_file in not_hashed:
            print(unhashed_file)

    if files_changed:
        print("These files changed while processing.")
        for changed_file in files_changed:
            print(changed_file)
                
else:
    print('Provided path does not exist')
