import os
import shutil


def copy_items_from_source_to_destination(source_path: str, destination_path: str):
    list_of_all_source_dir_items = os.listdir(source_path)
    # print(list_of_all_source_dir_items)
    for item in list_of_all_source_dir_items:
        item_complete_absolute_path_in_source = os.path.normpath(os.path.join(source_path, item))
        if os.path.isdir(item_complete_absolute_path_in_source):
            item_directory_absolute_path_in_destination = os.path.normpath(os.path.join(destination_path, item))
            os.mkdir(item_directory_absolute_path_in_destination)
            copy_items_from_source_to_destination(item_complete_absolute_path_in_source, item_directory_absolute_path_in_destination)
        else:
            shutil.copy(item_complete_absolute_path_in_source, destination_path)


def copy_static_to_public(source_dir: str, destination_dir: str) -> None:

    source_dir_absolute_path = os.path.abspath(source_dir)

    if not os.path.exists(source_dir_absolute_path):
        raise Exception(f"{source_dir_absolute_path} does not exist.")
    if not os.path.isdir(source_dir_absolute_path):
        raise Exception(f"{source_dir_absolute_path} is a file.")
    
    # list_of_all_items = os.listdir()
    # print(list_of_all_items) # ['test.sh', 'tests', '.git', 'main.sh', 'src', 'public', 'static', '.gitignore']

    current_working_directory = os.getcwd()
    # print(current_working_directory) # /home/user/workspace/Static-Site-Generator

    destination_dir_absolute_path = os.path.normpath(os.path.join(current_working_directory, destination_dir))
    # print(destination_dir_absolute_path)

    # Safety check to ensure we never delete directories outside the project root.
    valid_target_dir: bool = os.path.commonpath([current_working_directory, destination_dir_absolute_path]) == current_working_directory

    if not valid_target_dir:
        raise Exception("The destination folder must be in project folder")

    if not os.path.exists(destination_dir_absolute_path):
        print(f"{destination_dir} folder does not exist")
        print(f"Creating {destination_dir}...")
        os.mkdir(destination_dir_absolute_path)
        print("Created!")
    else :
        print(f"{destination_dir} exists, will delete and remake")
        shutil.rmtree(destination_dir_absolute_path)
        os.mkdir(destination_dir_absolute_path)

    copy_items_from_source_to_destination(source_dir_absolute_path, destination_dir_absolute_path)