import csv
import os

import numpy as np


def _next_available_filename(filename):
    base, extension = os.path.splitext(filename)
    candidate = filename
    counter = 0
    while os.path.exists(candidate):
        counter += 1
        candidate = f"{base}_{counter}{extension}"
    return candidate


def writeDataToCSV(data, filename):
    filename = _next_available_filename(filename)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['duration_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def statistics(data, frameNmb, duration):
    """
    Calculate and save basic statistics for a list of numerical data.

    Args:
        data (list): A list of numerical values.
        frameNmb (int): The number of frames sent.
        duration (float): The total measurement duration in seconds.
    """
    if not data:
        print("No data provided for statistics.")
        return

    filename = _next_available_filename('measures/hand_landmarker_statistics.txt')
    mean = np.mean(data)
    median = np.median(data)
    min_val = np.min(data)
    max_val = np.max(data)
    percentile_95 = np.percentile(data, 95)
    with open(filename, 'w') as f:
        f.write("Statistics:\n")
        f.write(f"Mean: {mean:.2f} ms\n")
        f.write(f"Median: {median:.2f} ms\n")
        f.write(f"Min: {min_val:.2f} ms\n")
        f.write(f"Max: {max_val:.2f} ms\n")
        f.write(f"95th Percentile: {percentile_95:.2f} ms\n")
        f.write(f"Number of Frames sent: {frameNmb}\n")
        f.write(f"Number of Frames received: {len(data)}\n")
        f.write(f"Number of Frames lost: {frameNmb - len(data)}\n")
        f.write(f"Total Duration: {duration:.2f} s\n")
        f.write(f"Average FPS: {frameNmb / duration:.2f} fps\n")


def delete_measurement_files():
    """Delete all files in the 'measures' directory."""
    measures_dir = 'measures'
    if os.path.exists(measures_dir):
        for filename in os.listdir(measures_dir):
            file_path = os.path.join(measures_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
