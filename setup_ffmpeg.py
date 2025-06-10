import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_ffmpeg():
    # Create a bin directory if it doesn't exist
    bin_dir = Path("bin")
    bin_dir.mkdir(exist_ok=True)
    
    # FFmpeg download URL for Windows
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    print("Downloading FFmpeg...")
    zip_path = bin_dir / "ffmpeg.zip"
    
    # Download the file
    urllib.request.urlretrieve(url, zip_path)
    
    print("Extracting FFmpeg...")
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(bin_dir)
    
    # Find the ffmpeg.exe in the extracted files
    ffmpeg_dir = next(bin_dir.glob("ffmpeg-master-latest-win64-gpl"))
    ffmpeg_exe = next(ffmpeg_dir.glob("**/ffmpeg.exe"))
    
    # Move ffmpeg.exe to the bin directory
    shutil.copy2(ffmpeg_exe, bin_dir / "ffmpeg.exe")
    
    # Clean up
    shutil.rmtree(ffmpeg_dir)
    zip_path.unlink()
    
    print("FFmpeg has been installed successfully!")
    print(f"FFmpeg is located at: {bin_dir.absolute() / 'ffmpeg.exe'}")
    
    # Add the bin directory to PATH
    os.environ["PATH"] = str(bin_dir.absolute()) + os.pathsep + os.environ["PATH"]
    
    return str(bin_dir.absolute())

if __name__ == "__main__":
    download_ffmpeg() 