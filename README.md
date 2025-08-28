# Alf
Primitive Claude Code interactive voice chat wrapper

## Features
- Real-time voice recording with spacebar controls
- Automatic speech-to-text using Whisper model
- CUDA/CPU optimization for model performance
- Simple keyboard interface (hold spacebar to record, ESC to exit)

## Dependencies
- `torch` - PyTorch for ML backend
- `faster-whisper` - Optimized Whisper implementation  
- `pynput` - Keyboard input handling

## Installation
```bash
pip install torch faster-whisper pynput
```

## Usage
```bash
python main.py
```

Hold SPACEBAR to record audio, release to stop. Press ESC to exit.

## Project Structure
```
Alf/
├── main.py     # Voice recording interface with keyboard controls
├── model.py    # Whisper model setup with CUDA/CPU detection
└── README.md   # This file
```
