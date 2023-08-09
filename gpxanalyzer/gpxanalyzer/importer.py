import gpxpy
import os

def read_gpx(file_path):
    with open(file_path, 'r') as file:
        gpx = gpxpy.parse(file)
    return gpx


def load_gpx_files_from_directory(directory):
    """
    Load all GPX files from a specified directory.

    Parameters:
    - directory: The directory containing the GPX files.

    Returns:
    - List of GPX objects.
    """
    gpx_objects = []

    for filename in os.listdir(directory):
        if filename.endswith(".gpx"):
            with open(os.path.join(directory, filename), 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                gpx_objects.append(gpx)

    return gpx_objects