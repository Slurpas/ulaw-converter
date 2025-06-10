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

### From Source

1. Ensure you have Python 3.8 or higher installed
2. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ulaw-converter.git
   cd ulaw-converter
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the setup script to install FFmpeg:
   ```bash
   python setup_ffmpeg.py
   ```
5. Run the application:
   ```bash
   python main.py
   ```

### From Executable

1. Download the latest release from the [Releases](https://github.com/YOUR_USERNAME/ulaw-converter/releases) page
2. Extract the ZIP file
3. Run `AudioConverter.exe`

## Usage

1. Launch the application
2. Drag and drop audio files into the application window
3. (Optional) Click "Settings" to customize output parameters
4. Click "Convert" to start the conversion process
5. Select the output directory
6. Monitor progress using individual progress bars
7. Cancel any ongoing conversion if needed
8. Find converted files in the output directory

## Output Format

Default output format:
- Format: WAV
- Encoding: ITU G.711 μ-law
- Channels: Mono
- Sample Rate: 8000 Hz
- Bit Depth: 8 bit

## Development

### Building from Source

To build the executable:
```bash
python setup.py build
```

The executable will be created in the `build` directory.

### Project Structure

```
ulaw-converter/
├── main.py              # Main application code
├── setup_ffmpeg.py      # FFmpeg installation script
├── setup.py            # Executable build script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── LICENSE            # MIT License
└── bin/               # FFmpeg binary (created by setup_ffmpeg.py)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for audio processing
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework 