# Audio to μ-law Converter

A professional GUI application for converting audio files to ITU G.711 μ-law format.

## Features

- Drag and drop interface for easy file selection
- Support for multiple audio formats (WAV, MP3, FLAC, OGG, M4A, AAC)
- Individual progress bars for each file
- Ability to cancel ongoing conversions
- Detailed error handling and messages
- Customizable output parameters
- Default output format: WAV, ITU G.711 μ-law, mono, 8000 Hz

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```
2. Drag and drop audio files into the application window
3. Click "Convert" to start the conversion process
4. Monitor progress using individual progress bars
5. Cancel any ongoing conversion if needed
6. Find converted files in the output directory

## Output Format

Default output format:
- Format: WAV
- Encoding: ITU G.711 μ-law
- Channels: Mono
- Sample Rate: 8000 Hz
- Bit Depth: 8 bit 