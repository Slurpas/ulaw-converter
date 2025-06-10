import os
import shutil
from pathlib import Path
import zipfile

def create_release_package():
    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Get the build directory
    build_dir = next(Path("build").glob("exe.win-*"))
    
    # Create a release directory
    release_dir = dist_dir / "AudioConverter"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True)
    
    # Copy the executable and its dependencies
    print("Copying files to release directory...")
    shutil.copytree(build_dir, release_dir, dirs_exist_ok=True)
    
    # Copy additional files
    shutil.copy("README.md", release_dir)
    shutil.copy("LICENSE", release_dir)
    
    # Create ZIP file
    print("Creating ZIP file...")
    zip_path = dist_dir / "AudioConverter.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"Release package created at: {zip_path}")
    return zip_path

if __name__ == "__main__":
    create_release_package() 