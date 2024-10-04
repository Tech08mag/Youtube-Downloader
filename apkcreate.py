import subprocess
from pathlib import Path

def convert_py_to_apk(py_file_path: str):
    """
    Converts a Python file to an APK (Android application package) using PyInstaller and Buildozer.

    Parameters:
    - py_file_path: str
        The file path of the Python file that needs to be converted.

    Raises:
    - FileNotFoundError:
        Raises an error if the specified Python file does not exist.
    - subprocess.CalledProcessError:
        Raises an error if there is an error during the conversion process.
    """

    # Checking if the Python file exists
    try:
        with open(py_file_path):
            pass
    except FileNotFoundError:
        raise FileNotFoundError(f"The Python file '{py_file_path}' does not exist.")

    # Running PyInstaller to convert the Python file to an executable
    try:
        subprocess.run(["pyinstaller", "--onefile", py_file_path], check=True)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error during PyInstaller conversion: {e}")

    # Running Buildozer to package the executable as an APK
    try:
        subprocess.run(["buildozer", "android", "debug"], check=True)
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error during Buildozer conversion: {e}")

# Example usage of the convert_py_to_apk function:
py_file_path = "C:\\Users\\tech0\\Desktop\\Coden\\Python\\Youtube-Downloader\\main.py"
try:
    convert_py_to_apk(py_file_path)
    print(f"The Python file '{py_file_path}' has been successfully converted to an APK.")
except FileNotFoundError as e:
    print(f"Error: {e}")
except subprocess.CalledProcessError as e:
    print(f"Error during conversion: {e}")

convert_py_to_apk(py_file_path=f"{Path.cwd()}\\main.py")