# POE2 Filter Sound Editor

A simple, standalone GUI tool to edit alert sounds in your Path of Exile 2 item filter files.

## 🎯 Features

- Load `.filter` files and list alert sound rules
- View associated rarity and item context
- Replace individual or all matching sounds
- Automatically copies new sound files to the filter directory
- No Python installation needed — just run the `.exe`

## 🚀 How to Use

1. [Download the app](https://github.com/xtheredshirtx/POE2-Filter-Custom-Sound-Editor/releases/tag/V1.0)
2. Run `POE2_Filter_Sound_Editor.exe`
3. Click **"Load Filter File"** and select your `.filter` file
4. Select an entry from the table
5. (Optional) Enable **"Bulk Replace All Matching Sounds"**
6. Click **"Replace Sound File"** and choose your `.wav`, `.ogg`, `.mp3`, or `.wmv` file
7. The filter will automatically update and save
8. Once it finishes saving, you will then be asked to select that filter again to show the updated filter with the sounds that were changed. I forgot to fix this so creating V2.0 so it doesn't need to do that moving forward.

## 🖼 Example Workflow

- Load your `.filter` file
- Select an alert sound entry
- Replace the sound
- You're done!

## 📂 Supported Sound Formats

- `.wav`
- `.ogg`
- `.mp3`
- `.wmv`

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
