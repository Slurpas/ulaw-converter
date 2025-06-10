import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "PyQt6", "subprocess"],
    "excludes": [],
    "include_files": [
        ("bin/ffmpeg.exe", "bin/ffmpeg.exe"),
        "README.md",
        "LICENSE"
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for Windows GUI applications

setup(
    name="Audio to μ-law Converter",
    version="1.0",
    description="Convert audio files to ITU G.711 μ-law format",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="AudioConverter.exe",
            icon="icon.ico"  # You can add an icon file later
        )
    ]
) 