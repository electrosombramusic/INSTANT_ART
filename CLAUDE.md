# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Instant Art is an automated image processing pipeline with three independent Python scripts that form a complete workflow: monitoring, processing, and displaying images with artistic RGB channel manipulations.

## System Architecture

The system operates as a **three-stage pipeline** with independent processes:

```
fotos/ → [monitor_fotos.py] → proceso/ → [procesa.py] → carrusel/ → [carrusel.py]
```

### Pipeline Components

1. **monitor_fotos.py** - File system watcher
   - Monitors `fotos/` directory every 15 seconds
   - Uses `st_ctime` (Linux) or `st_birthtime` (other OS) for timestamp tracking
   - Copies new files to `proceso/` using `shutil.copy2` to preserve metadata
   - Tracks changes via timestamp comparison, not file hashes

2. **procesa.py** - Image processor
   - Monitors `proceso/` directory every 15 seconds
   - Applies random RGB channel permutations using NumPy array manipulation
   - Converts all images to RGB mode before processing (handles RGBA, grayscale, etc.)
   - Outputs to `carrusel/` with `_rgb` suffix added to filenames
   - Uses PIL/Pillow for image I/O, NumPy for channel manipulation

3. **carrusel.py** - Interactive slideshow viewer
   - Pygame-based full-screen slideshow (starts in fullscreen by default)
   - Dynamically loads images every 5 seconds, detecting new additions
   - Displays images chronologically based on `st_ctime`
   - Scales images to 90% of screen size maintaining aspect ratio using LANCZOS resampling
   - Shows filename, timestamp, and position counter overlays

### Key Design Patterns

- **Timestamp-based detection**: All scripts use file creation timestamps (`st_ctime` on Linux) rather than maintaining processed file lists
- **Independent processes**: Each script runs autonomously with its own monitoring loop
- **Graceful degradation**: Scripts continue running and log errors if directories are temporarily unavailable
- **No inter-process communication**: Scripts coordinate solely through the file system

## Development Commands

### Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Running the System

The three scripts should run **simultaneously in separate terminals**:

```bash
# Terminal 1 - Monitor
source venv/bin/activate
python monitor_fotos.py

# Terminal 2 - Processor
source venv/bin/activate
python procesa.py

# Terminal 3 - Slideshow
source venv/bin/activate
python carrusel.py
```

### Testing Individual Components

```bash
# Test file monitoring only
python monitor_fotos.py

# Test image processing only (requires images in proceso/)
python procesa.py

# Test slideshow only (requires images in carrusel/)
python carrusel.py
```

### Modifying Timing Constants

- **Monitor/Processor intervals**: Edit `time.sleep(15)` in monitor_fotos.py:66 and procesa.py:118
- **Slideshow transition time**: Edit `PAUSA_SEGUNDOS = 5` in carrusel.py:21
- **Slideshow frame rate**: Edit `clock.tick(30)` in carrusel.py:277

## Important Implementation Details

### Image Processing Algorithm

The RGB channel swap in procesa.py:24-52 works by:
1. Converting image to RGB mode (strips alpha channels)
2. Loading into NumPy array with shape (height, width, 3)
3. Using `random.shuffle()` on `[0, 1, 2]` to create channel permutation
4. Indexing array with `img_array[:, :, permutacion]` to reorder channels
5. Converting back to PIL Image and saving with quality=95

### Directory Structure Requirements

Required directories (create if missing):
- `fotos/` - Input directory for original images
- `proceso/` - Intermediate directory for copied images
- `carrusel/` - Output directory for processed images
- `venv/` - Python virtual environment (gitignored)

### Pygame Display System

carrusel.py implements a custom Pygame display with:
- Dynamic resolution detection (uses `pygame.display.Info()` in fullscreen)
- Bi-directional navigation (forward/backward through images)
- Aspect ratio preservation during scaling
- Semi-transparent overlay rendering for text (alpha=180)
- Fullscreen toggle support (F key)

### Error Handling Pattern

All scripts follow this pattern:
- Outer `while True` loop for continuous operation
- Inner try-except catching `KeyboardInterrupt` for clean shutdown
- Directory existence checks on every iteration
- Per-file error handling that logs but doesn't crash the process

## Dependencies

- **Pillow** (12.0.0): Image I/O and format conversion
- **NumPy** (2.3.5): Array manipulation for channel swapping
- **Pygame** (2.6.1): Display rendering and event handling

## Supported Image Formats

JPG, JPEG, PNG, BMP, GIF, TIFF, WebP (defined in `EXTENSIONES_IMAGEN` constant)

## Carrusel Controls

- **ESC** or **Q**: Exit
- **F**: Toggle fullscreen/windowed mode
- **SPACE**: Advance to next image immediately
- **LEFT ARROW**: Go to previous image
