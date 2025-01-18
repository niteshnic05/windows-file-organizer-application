# Windows File Organizer Application

A simple Windows application that organizes files into folders based on their date, either by file name or creation date. The application can differentiate between images and videos, creating separate folders for each type, and can detect and handle duplicate images.

## Features
- **Organize Files by Date**:
  - Choose to organize files based on either the date in the filename or the file's creation date.
- **Create Year and Month Folders**:
  - Files are moved into folders structured as `Year -> Month -> Type (Images/Videos)`.
- **Separate Images and Videos**:
  - Creates separate subfolders for images and videos within each month folder.
- **Handle Duplicates**:
  - Detects duplicate images using perceptual hashing and moves them to a `Duplicates` folder.
- **Move Unrecognized Files**:
  - Files that don't match the specified criteria are moved to an `Others` folder.
- **Supported File Formats**:
  - It's supports - .png, .jpg, .jpeg, .bmp, .gif, .mp4, .mkv, .avi, .mov, .wmv, .3gp
- **User-Friendly GUI**:
  - Browse and select the folder to organize.
  - Choose the organization method.
  - View logs and results in the same window.
  - Double-click folders in the result tree view to open them in File Explorer.

## Preview
![Alt text](screenshot.jpg?raw=true "Windows File Organizer Application")

## How to Use
1. **Launch the Application**: Run the `FileOrganizer.exe` file.
2. **Select a Folder**: Use the `Browse` button to choose the folder you want to organize.
3. **Choose Organization Method**: Select either:
   - `Use Filename Date`
   - `Use Created Date`
4. **Click 'Run Arrange'**: The application will organize the files and display logs and results.
5. **View Results**:
   - The results are displayed in a tree view.
   - Double-click any folder in the tree view to open it in File Explorer.

## Statistics Displayed
- **Images Found**
- **Videos Found**
- **Folders Created**
- **Duplicates Found**

## Folder Structure Example
```
Organized_Folder
|
|-- 2023
|   |-- January-01
|       |-- Images
|       |   |-- img1.jpg
|       |   |-- img2.png
|       |-- Videos
|           |-- video1.mp4
|           |-- video2.avi
|-- Others
    |-- Images
    |-- Videos
|-- Duplicates
    |-- img1_duplicate.jpg
```

## Handling Duplicate Files
The application uses perceptual hashing to detect duplicate images even if they have different file sizes or names. Detected duplicates are moved to a `Duplicates` folder.

## Changing the Application Icon
To change the application icon:
1. Create or download an `.ico` file for your icon.
2. Use the following command with PyInstaller to generate the executable with the new icon:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon=app_icon.ico organize_files_by_date.py
   ```

## Building the Executable
To create a standalone executable:
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Run the following command:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --icon=app_icon.ico arrange-files-ui.py
   ```
3. The `.exe` file will be located in the `dist` folder.

## Requirements
- Windows 7, 10, or 11
- No need to install Python; the application is packaged as a standalone executable.

## Technologies Used
- **Python**
- **Tkinter** for the GUI
- **Pillow (PIL)** for image processing
- **ImageHash** for duplicate detection

## Contribution
Feel free to contribute to this project by forking the repository and creating pull requests. Any improvements or bug fixes are welcome!

## License
This project is licensed under the MIT License.
