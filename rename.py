import os

def rename_files_in_directory(directory, new_name_template):
    """
    Rename all files in the specified directory to a new name template.
    
    Args:
        directory (str): The path to the directory containing the files.
        new_name_template (str): The template for the new names, e.g., 'file_{}.txt'.
    
    Returns:
        None
    """
    # List all files in the directory
    files = os.listdir(directory)
    # Filter out directories, only keep files
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]

    for index, filename in enumerate(files):
        # Get the file extension
        file_extension = os.path.splitext(filename)[1]
        # Generate the new name using the template and index
        new_name = new_name_template.format(index) + file_extension
        # Create the full paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)
        # Rename the file
        os.rename(old_file, new_file)

# Example usage
directory_path = 'data/Images/Maps'
new_name_template = 'block_{}'
rename_files_in_directory(directory_path, new_name_template)
