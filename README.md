# MOD -> MP4 Converter (macOS)
A simple macOS application and Python script to batch convert `.MOD` video files to high-quality `.MP4` using `ffmpeg`.

Designed for camcorder footage (e.g., JVC, Canon, Panasonic) and optimized for compatibility, quality, and smooth playback.


## Index
- [Features](#features)
- [Output settings](#output-settings)
- [Requirements](#requirements)
- [Usage (Python script)](#usage-python-script)
- [Usage (macOS app)](#usage-macos-app)
- [Building the macOS app](#building-the-macos-app)
- [Project structure](#project-structure)
- [Error Messages and Troubleshooting](#error-messages-and-troubleshooting)
- [Notes](#notes)
- [License](#license)
- [Author](#author)


## Features
- Batch convert multiple `.MOD` files at once
- Native macOS file picker (Finder dialog)
- High-quality H.264 video encoding
- AAC audio conversion
- Automatic output naming
- Clean macOS popup interface
- Loading indicator during conversion
- Summary report when finished
- No Terminal required when using the `.app`

## Output settings
Video is converted using:
- Codec: H.264 (`libx264`)
- Preset: `slow`
- CRF: `16` (high quality)
- Deinterlace filter: `bwdif`
- Pixel format: `yuv420p`
- Audio: AAC, 192 kbps
- Fast start enabled for better playback compatibility

These settings provide excellent quality and compatibility with:
- macOS / QuickTime
- iPhone / iPad
- TVs
- Video editing software
- YouTube / Vimeo

## Requirements
- macOS (Apple Silicon or Intel)
- ffmpeg installed via Homebrew


Install ffmpeg:
```bash
brew install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

## Usage 
### Usage (Python script)

Run:
```bash
python mod-conversor.py
```

Then:
1. Select one or more `.MOD` files
2. Wait for conversion to finish
3. Converted `.mp4` files appear in the same folder

### Usage (macOS app)
If using the `.app` version:
1. Double-click the app
2. Select `.MOD` files
3. Wait for conversion
4. Done

No Terminal required.

## Building the macOS app
If you want to make any changes and create your own .app bundle you will have to do:

Install PyInstaller:
```bash
pip install pyinstaller
```

Build the app:
```bash
pyinstaller --windowed --onedir --name "MOD2MP4" mod2mp4.py
```

The app will be created in:

`dist/MOD2MP4.app`


You can move it to:

`/Applications`


## Error Messages and Troubleshooting

This section explains common error messages and how to resolve them.

### "ffmpeg is not installed"

**Cause:**

The application cannot find `ffmpeg` on your system.

**Solution:**

Install ffmpeg using Homebrew:
```bash
brew install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

If already installed, make sure it exists in one of these locations:
```bash
/opt/homebrew/bin/ffmpeg
/usr/local/bin/ffmpeg
```

### "The file selection was cancelled"

**Cause:**

You clicked "Cancel" in the file selection dialog.

**Solution:**

No action required. Run the app again and select one or more `.MOD` files.

### "The selected file type is not .MOD"

**Cause:**

The selected file is not a `.MOD` video file.

**Solution:**

Select only `.MOD` files. These are typically produced by camcorders.

### "The selected file does not exist"

**Cause:**

The file was moved, deleted, or is no longer accessible.

**Solution:**

Verify the file exists and try again.

### "The file has already been converted or there is another with the same name"

**Cause:**

An `.mp4` file with the same name already exists in the output folder.

**Solution:**

Either:
- Delete or move the existing `.mp4` file, or
- Rename the existing file, or
- Choose a different input file

The converter will not overwrite existing files.

### "ffmpeg failed during conversion"

**Cause:**

ffmpeg encountered an error while processing the video.

Possible reasons:
- Corrupted input file
- Unsupported format
- Insufficient disk space
- Permission issues

**Solution:**
1. Verify the `.MOD` file plays normally
2. Ensure sufficient disk space
3. Try converting the file manually:

```bash
ffmpeg -i input.MOD output.mp4
```

If manual conversion also fails, the file may be corrupted.

### "ffmpeg executable not found"

**Cause:**

ffmpeg is not installed or not accessible.

**Solution:**

Install or reinstall ffmpeg:

```bash
brew install ffmpeg
```

### App does not open or shows "unidentified developer"

**Cause:**

macOS Gatekeeper security.

**Solution:**

Right-click the app -> click *Open* -> click *Open* again.

macOS will remember your choice.

### Conversion is very slow

**Cause:**

High-quality encoding settings are used (`preset slow`, `CRF 16`).

**Solution (optional):**

This is normal. Faster encoding can be achieved by modifying the preset in the source code:

```bash
-preset fast
```

This reduces conversion time at a small quality cost.

### No output file appears

**Cause:**
- Conversion failed, or
- Output file already exists and was skipped

**Solution:**

Check the summary popup for skipped files and reasons.

---

If you encounter an issue not listed here, please open an issue on GitHub and include:
- macOS version
- ffmpeg version (ffmpeg -version)
- description of the problem

## Project structure
```bash
mod2mp4/
│
├── mod2mp4.py
├── icon.icns        (optional)
├── README.md
└── .gitignore
```

## Why this exists

`.MOD` is an older camcorder format that:
is poorly supported by modern players often requires deinterlacing is inconvenient for editing and sharing.

This tool converts `.MOD` into a modern, high-quality `.MP4` format suitable for long-term storage and playback.

## Notes
- Original files are never modified
- Existing .mp4 files are not overwritten
- Conversion uses ffmpeg for maximum reliability

## License

MIT License

You are free to use, modify, and distribute.

## Author
Ciro Alonso Aquino

Created for personal and archival video conversion on macOS.