import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFileDialog, QMessageBox,
    QDialog, QComboBox, QSpinBox, QCheckBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class ConversionWorker(QThread):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal(str, bool, str)
    error = pyqtSignal(str, str)

    def __init__(self, input_file: str, output_file: str, settings: Dict):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.settings = settings
        self.is_cancelled = False

    def run(self):
        try:
            # Get the path to ffmpeg
            ffmpeg_path = os.path.join("bin", "ffmpeg.exe")
            if not os.path.exists(ffmpeg_path):
                raise FileNotFoundError("FFmpeg not found. Please run setup_ffmpeg.py first.")

            # Build FFmpeg command
            command = [
                ffmpeg_path,
                '-i', self.input_file,
                '-ar', str(self.settings['sample_rate']),
                '-ac', '1' if self.settings['mono'] else '2',
                '-acodec', 'pcm_mulaw',
                '-f', 'wav',  # Force WAV format
                '-y',  # Overwrite output file if it exists
                self.output_file
            ]

            # Run FFmpeg
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW  # Hide console window
            )

            # Monitor the process
            while process.poll() is None:
                if self.is_cancelled:
                    process.terminate()
                    self.error.emit(self.input_file, "Conversion cancelled")
                    return
                self.progress.emit(self.input_file, 50)

            # Get the output and error messages
            stdout, stderr = process.communicate()

            # Check if the conversion was successful
            if process.returncode == 0:
                self.progress.emit(self.input_file, 100)
                self.finished.emit(self.input_file, True, "Conversion completed successfully")
            else:
                # Extract the relevant error message
                error_lines = stderr.split('\n')
                error_message = next((line for line in error_lines if 'Error' in line), stderr)
                self.error.emit(self.input_file, f"FFmpeg error: {error_message}")

        except Exception as e:
            self.error.emit(self.input_file, str(e))

    def cancel(self):
        self.is_cancelled = True

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conversion Settings")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Sample rate settings
        sample_rate_group = QGroupBox("Sample Rate")
        sample_rate_layout = QFormLayout()
        self.sample_rate = QSpinBox()
        self.sample_rate.setRange(8000, 48000)
        self.sample_rate.setValue(8000)
        self.sample_rate.setSingleStep(1000)
        sample_rate_layout.addRow("Sample Rate (Hz):", self.sample_rate)
        sample_rate_group.setLayout(sample_rate_layout)
        
        # Channel settings
        channel_group = QGroupBox("Channels")
        channel_layout = QFormLayout()
        self.mono = QCheckBox("Convert to Mono")
        self.mono.setChecked(True)
        channel_layout.addRow(self.mono)
        channel_group.setLayout(channel_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addWidget(sample_rate_group)
        layout.addWidget(channel_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_settings(self):
        return {
            'sample_rate': self.sample_rate.value(),
            'mono': self.mono.isChecked()
        }

class AudioConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio to μ-law Converter")
        self.setMinimumSize(600, 400)
        self.files_to_convert = []
        self.workers = {}
        self.settings = {
            'sample_rate': 8000,
            'mono': True
        }
        self.setup_ui()
        self.conversion_results = {"success": [], "errors": []}
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Drop zone
        self.drop_label = QLabel("Drag and drop audio files here")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background: #f0f0f0;
            }
        """)
        self.drop_label.setMinimumHeight(100)
        layout.addWidget(self.drop_label)
        
        # File list and progress
        self.file_list = QWidget()
        self.file_list_layout = QVBoxLayout(self.file_list)
        layout.addWidget(self.file_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.settings_button = QPushButton("Settings")
        self.convert_button = QPushButton("Convert")
        self.clear_button = QPushButton("Clear All")
        
        self.settings_button.clicked.connect(self.show_settings)
        self.convert_button.clicked.connect(self.start_conversion)
        self.clear_button.clicked.connect(self.clear_files)
        
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files(files)
        
    def add_files(self, files: List[str]):
        for file in files:
            if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac')):
                if file not in self.files_to_convert:
                    self.files_to_convert.append(file)
                    self.add_file_to_list(file)
                    
    def add_file_to_list(self, file: str):
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        
        # File name
        file_label = QLabel(os.path.basename(file))
        file_label.setWordWrap(True)
        file_layout.addWidget(file_label)
        
        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        file_layout.addWidget(progress_bar)
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.cancel_conversion(file))
        file_layout.addWidget(cancel_button)
        
        self.file_list_layout.addWidget(file_widget)
        
    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.sample_rate.setValue(self.settings['sample_rate'])
        dialog.mono.setChecked(self.settings['mono'])
        if dialog.exec():
            self.settings = dialog.get_settings()
            
    def start_conversion(self):
        if not self.files_to_convert:
            QMessageBox.warning(self, "Warning", "No files to convert!")
            return
            
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not output_dir:
            return
            
        # Reset conversion results
        self.conversion_results = {"success": [], "errors": []}
        
        for file in self.files_to_convert:
            if file not in self.workers:
                # Keep original filename
                output_file = os.path.join(output_dir, os.path.basename(file))
                
                worker = ConversionWorker(file, output_file, self.settings)
                worker.progress.connect(lambda f, p, file=file: self.update_progress(file, p))
                worker.finished.connect(lambda f, s, m, file=file: self.conversion_finished(file, s, m))
                worker.error.connect(lambda f, e, file=file: self.conversion_error(file, e))
                
                self.workers[file] = worker
                worker.start()
                
    def update_progress(self, file: str, progress: int):
        for i in range(self.file_list_layout.count()):
            widget = self.file_list_layout.itemAt(i).widget()
            if widget and widget.layout().itemAt(0).widget().text() == os.path.basename(file):
                progress_bar = widget.layout().itemAt(1).widget()
                progress_bar.setValue(progress)
                break
                
    def conversion_finished(self, file: str, success: bool, message: str):
        if success:
            self.conversion_results["success"].append(os.path.basename(file))
        self.workers.pop(file, None)
        
        # Check if all conversions are done
        if not self.workers:
            self.show_conversion_summary()
        
    def conversion_error(self, file: str, error: str):
        self.conversion_results["errors"].append((os.path.basename(file), error))
        self.workers.pop(file, None)
        
        # Check if all conversions are done
        if not self.workers:
            self.show_conversion_summary()
            
    def show_conversion_summary(self):
        message = []
        if self.conversion_results["success"]:
            message.append(f"Successfully converted {len(self.conversion_results['success'])} files.")
        if self.conversion_results["errors"]:
            message.append(f"Failed to convert {len(self.conversion_results['errors'])} files:")
            for file, error in self.conversion_results["errors"]:
                message.append(f"- {file}: {error}")
        
        if message:
            QMessageBox.information(self, "Conversion Summary", "\n".join(message))
            
    def cancel_conversion(self, file: str):
        if file in self.workers:
            self.workers[file].cancel()
            self.workers[file].wait()
            self.workers.pop(file)
            
    def clear_files(self):
        for worker in self.workers.values():
            worker.cancel()
            worker.wait()
        self.workers.clear()
        self.files_to_convert.clear()
        
        while self.file_list_layout.count():
            item = self.file_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

if __name__ == '__main__':
    # Check if FFmpeg is installed
    if not os.path.exists(os.path.join("bin", "ffmpeg.exe")):
        print("FFmpeg not found. Running setup...")
        import setup_ffmpeg
        setup_ffmpeg.download_ffmpeg()
    
    app = QApplication(sys.argv)
    window = AudioConverter()
    window.show()
    sys.exit(app.exec()) 