# Duplicate File Finder

A lightweight Python utility that recursively scans a directory and identifies duplicate files using a two-stage comparison process.

Instead of hashing every file immediately, the program first groups files by their size. SHA-256 hashing is then performed only on groups containing multiple files, reducing unnecessary file processing.

## Features

* 🔎 Recursively scans files and subdirectories
* 📦 Groups files by file size before hashing
* 🔐 Uses SHA-256 to identify potential duplicates
* ⚡ Avoids hashing files that have unique sizes
* 🛡️ Handles inaccessible or missing files
* 🔄 Detects files that change while being processed
* 📋 Displays duplicate files grouped together
* 🐍 Uses only Python's standard library

## How It Works

The program uses a two-stage approach to find duplicates.

### 1. Scan the directory

The program recursively searches the configured target directory using `pathlib.Path.rglob()`.

Only files are processed; directories are ignored.

### 2. Group files by size

Files are first grouped according to their size.

For example:

```text
1000 bytes
├── photo1.jpg
├── photo2.jpg
└── photo3.jpg

2048 bytes
└── document.pdf
```

Files with unique sizes cannot be identical, so they don't need to be hashed.

### 3. Hash potential duplicates

Only size groups containing more than one file are processed further.

Each file is read in chunks and hashed using SHA-256.

```text
Same size
    ↓
Calculate SHA-256
    ↓
Same hash
    ↓
Duplicate
```

### 4. Verify the file size

The program checks the file size again after hashing.

If the size has changed during processing, the file is reported separately rather than being treated as a reliable result.

### 5. Report results

Duplicate files are printed as groups:

```text
Duplicate Group:
target/photo1.jpg
target/backup/photo1.jpg
```

The program also reports:

* Files that couldn't be accessed
* Files that changed while being processed

## Requirements

* Python 3.x
* No external Python packages

Because the project uses only the Python standard library, `pip install` is not required.

## Installation

Clone the repository:

```bash
git clone https://github.com/harshitpatilx/duplicate-file-finder.git
cd duplicate-file-finder
```

## Usage

The program currently scans the following directory:

```text
./target/
```

Create the directory:

```text
duplicate-file-finder/
├── main.py
├── target/
└── .gitignore
```

Place the files you want to analyze inside `target/`.

Then run:

```bash
python main.py
```

## Example

Suppose the `target` directory contains:

```text
target/
├── photo1.jpg
├── photo2.jpg
├── notes.txt
└── backup/
    ├── photo1_copy.jpg
    └── document.pdf
```

If `photo1.jpg` and `photo1_copy.jpg` contain exactly the same data, the program will report:

```text
Duplicate Group:
target/photo1.jpg
target/backup/photo1_copy.jpg
```

## Handling Special Cases

### Inaccessible files

If a file cannot be found or permission is denied while it is being hashed, it is added to the inaccessible-files list.

The program reports:

```text
These files can't be accessed.
```

### Files changed during processing

A file could potentially be modified while the program is reading it.

The program compares the file's size before and after hashing. If the size has changed, the file is placed in a separate list.

The program reports:

```text
These files changed while processing.
```

## Project Structure

```text
duplicate-file-finder/
│
├── main.py
├── target/
│   └── files to scan
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Algorithm

The core algorithm can be summarized as:

```text
Start
  │
  ▼
Check target directory
  │
  ▼
Recursively find files
  │
  ▼
Group files by size
  │
  ├── Unique size ──────► Ignore
  │
  ▼
Multiple files with same size
  │
  ▼
Calculate SHA-256
  │
  ├── Cannot access ────► Report
  │
  ├── File changed ─────► Report
  │
  ▼
Group files by hash
  │
  ▼
Hash groups with >1 file
  │
  ▼
Duplicate files
```

## Why Compare Size First?

Hashing requires reading the contents of a file.

If a directory contains thousands of files, hashing every file would require unnecessary disk reads.

Two files with different sizes cannot be identical.

Therefore:

```text
File size → SHA-256
```

is more efficient than immediately doing:

```text
SHA-256 for every file
```

The current implementation reads files in `4096`-byte chunks while calculating the hash.

## Limitations

The current version intentionally keeps the project simple.

* The target directory is currently hard-coded as `./target/`
* There is no command-line interface yet
* Duplicate files are only reported; they are not deleted
* There is no graphical interface
* There is no progress indicator
* There is no persistent database or cache
* Files with the same size are hashed completely before comparison
* Only SHA-256 is currently used for content comparison

## Possible Future Improvements

Potential improvements for future versions:

* Add command-line arguments for selecting directories
* Add a progress indicator
* Add a summary of total files scanned
* Show total duplicate space
* Add an interactive duplicate-selection system
* Allow users to safely delete selected duplicates
* Add multithreaded hashing
* Add hash caching
* Add a graphical user interface
* Improve handling of files modified during scanning
* Add configurable chunk sizes
* Add unit tests

## Author

**Harshit Patil**

GitHub: https://github.com/harshitpatilx
