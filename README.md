# POE2 Filter Sound Editor

A simple, standalone GUI tool to edit alert sounds in your Path of Exile 2 item filter files.

## 🎯 Features

- Load `.filter` files and list alert sound rules
- View associated rarity and item context
- Replace individual or all matching sounds
- Automatically copies new sound files to the filter directory
- No Python installation needed when using the `.exe`

## 🚀 How to Use

### Option 1: Use the EXE

1. Download the latest release from the [Releases](https://github.com/xtheredshirtx/POE2-Filter-Custom-Sound-Editor/releases/tag/V1.0) page
2. Run `POE2_Filter_Sound_Editor.exe`
3. Follow the in-app instructions to load and modify your filter

### Option 2: Run via Python

```bash
git clone https://github.com/YOUR_USERNAME/POE2-Filter-Sound-Editor.git
cd POE2-Filter-Sound-Editor
python main.py
```

## 🛠 Requirements (Python version only)

- Python 3.x

## 🖼 Example Workflow

1. Load your `.filter` file
2. Select an alert sound entry
3. Click "Replace Sound File" to assign a new `.wav`, `.ogg`, `.mp3`, or `.wmv`
4. Enable "Bulk Replace" if you want to update all matching sounds
5. The app saves changes automatically

## 📂 Supported Sound Formats

- `.wav`
- `.ogg`
- `.mp3`
- `.wmv`

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
