
# Hedgedoc File Grabber

### 1. Filling out the `config.txt` file

The `config.txt` file is designed to help organize your notes by associating each unique note ID with a specific location in a folder hierarchy.

#### Structure of Each Line

Each line in the `config.txt` file should follow this format:

```
<Note ID>, <Path in Hierarchy>
```

- **Note ID**: A unique identifier for each note. This is usually the last part of the link.
- **Path in Hierarchy**: Specifies where the note should be placed within your folder structure. This path should follow the defined hierarchy, with each folder separated by a `/`.

#### Example of a Line

```
97X2xBIKRKerdp-AqyjWoA, Semester8/Summary
```

In this example:
- `97X2xBIKRKerdp-AqyjWoA` is the ID of the note.
- `Semester8/Summary` is the path where this note will appear in the hierarchy. This means the note will be named  `Summary` and be within the `Semester8` folder.


### 2. Adding Session Cookie 

To ensure proper functioning of the script, you need to provide your session cookie. You have two options:

#### Option 1: Manually Add Your Session Cookie to `cookies.txt`

1. **Locate Your Session Cookie**:
   - Open your web browser and log in to the relevant website.
   - Use the browser's developer tools (usually accessed by pressing `F12`) to locate your session cookie. You need to pick `connect.sid`.

2. **Add the Cookie to `cookies.txt`**:
   - Open the `cookies.txt` file in a text editor.
   - Add your session cookie in the following format:
     ```
     <cookie_value>
     ```
   - Save the `cookies.txt` file.

#### Option 2: Let the Script Automatically Fetch the Cookie (Not Recommended)

If you prefer, you can skip creating the `cookies.txt` file, and the script will attempt to fetch the session cookie automatically. However, be aware that this method has a **low success rate** and is not reliable.

**Recommendation**: It is highly recommended to manually retrieve and input the session cookie yourself, as this ensures the highest chance of success. Automatic retrieval is available as a fallback but should not be relied upon.

### Change the HOST value

Go in the `HedgedocFileGrabber.py` file and change the HOST if needeed.