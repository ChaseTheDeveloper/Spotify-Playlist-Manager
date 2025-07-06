# 🎵 Spotify Playlist Manager (SPM)

A powerful Python tool for managing your Spotify playlists with advanced features like CSV importing, duplicate removal, and detailed playlist analysis.

# IMPORTANT MUST READ OR SCRIPT WONT WORK
!!! TO START OFF YOU NEED TO NAVIGATE TO "C:\Users\(user)\Downloads\Spotify-Playlist-Manager-main.zip\Spotify-Playlist-Manager-main\SPM-Chase.zip\SPM-Chase" AND EXTRACT THE "SPM-Chase" FOLDER INTO THE DOWNLOADS FOLDER OR ANOTHER FOLDER FOR YOU TO ACCESS !!!

## 📋 Table of Contents
- [MUST READ](#important-must-read-or-script-wont-work)
- [What This Tool Does](#what-this-tool-does)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Spotify API Setup](#spotify-api-setup)
- [How to Use](#how-to-use)
- [File Organization](#file-organization)
- [CSV Format](#csv-format)
- [Troubleshooting](#troubleshooting)
- [Features](#features)

## 🎯 What This Tool Does

This Spotify Playlist Manager can:

1. **📊 Create Playlists from CSV Files** - Import hundreds of songs from a spreadsheet
2. **🔍 Analyze Existing Playlists** - Get detailed reports about your playlists
3. **🧹 Remove Duplicates** - Clean up duplicate songs automatically
4. **📈 Generate Reports** - Create detailed analysis files for your music collection

## 🔧 Prerequisites

Before you start, you need:
- A computer with Windows, Mac, or Linux
- A Spotify account (free or premium)
- Internet connection
- Basic computer skills (opening folders, running programs)

## 📥 Installation Guide

### Step 1: Install Python
1. Go to [python.org](https://python.org/downloads/)
2. Download Python 3.8 or newer
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

### Step 2: Install Required Libraries
1. Press `Windows Key + R`, type `cmd`, press Enter
2. Copy and paste this command, then press Enter:
   ```
   pip install spotipy pandas
   ```
3. Wait for installation to complete

### Step 3: Download the Tool
1. Download the zip
2. Save it to a folder like `C:\Users\YourName\Downloads\SPM-Chase\`

## 🔑 Spotify API Setup

You need to create a Spotify app to use this tool:

### Step 1: Create Spotify App
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill out the form:
   - **App Name**: "My Playlist Manager" (or any name)
   - **App Description**: "Personal playlist management tool"
   - **Redirect URI**: `http://127.0.0.1:8080/callback`
   - Check the boxes and click "Save"

### Step 2: Get Your Credentials
1. Click on your newly created app
2. Click "Settings" in the top right
3. Copy your **Client ID** (you'll need this)
4. Click "View client secret" and copy your **Client Secret** (you'll need this)
5. **KEEP THESE PRIVATE** - Don't share them with anyone!

## 🚀 How to Use

### Running the Program

1. **Open Command Prompt**:
   - Press `Windows Key + R`
   - Type `cmd` and press Enter

2. **Navigate to your folder**:
   ```
   cd C:\Users\YourName\Downloads\SPM-Chase
   ```
   (Replace `YourName` with your actual username)

3. **Run the program**:
   ```
   python spm.py
   ```

### First Time Setup
The program will ask for:
- **Client ID**: Paste the Client ID from Spotify
- **Client Secret**: Paste the Client Secret from Spotify  
- **Username**: Your Spotify username (not email)

**Note**: After the first time, these will be saved automatically!

### Choose What to Do

The program offers 3 options:

#### Option 1: Create Playlist from CSV File
- Converts a spreadsheet of songs into a Spotify playlist
- You'll need a CSV file with "Artist" and "Song" columns
- The program will search for each song and add it to your playlist

#### Option 2: Analyze Existing Playlist
- Takes any Spotify playlist URL and creates a detailed report
- Shows artist breakdowns, song counts, and finds duplicates
- Great for understanding your music collection

#### Option 3: Remove Duplicates
- Scans a playlist for duplicate songs
- Removes duplicates automatically (keeps one copy)
- Creates a report of what was removed

## 📁 File Organization

The program automatically organizes files into folders:

```
C:\Users\YourName\Downloads\SPM-Chase\
├── Analyzed\          # Playlist analysis reports
├── Duplicates\        # Duplicate removal reports  
├── Playlist\          # CSV import reports
├── cache\             # Saved credentials and tokens
└── spm.py
└── setup.py
```

## 📊 CSV Format

Your CSV file should look like this:

```csv
Artist,Song,comment
Miley Cyrus,Party in the U.S.A.,I recommend using AI to create your playlist unless 
Miley Cyrus,The Climb,you wanna type it all yourself. and have the AI get rid of the comment (this)
```

**Requirements**:
- Must have "Artist" and "Song" columns (case-sensitive)
- Additional columns are okay (they'll be ignored)
- Save as `.csv` format in Excel or Google Sheets

## 🔧 Troubleshooting

### Common Issues

**"Command not found" or "Python not recognized"**
- Python wasn't added to PATH during installation
- Reinstall Python and check "Add Python to PATH"

**"Module not found" errors**
- Run: `pip install spotipy pandas`
- Make sure you have internet connection

**"Invalid playlist URL"**
- Make sure you're copying the full Spotify playlist URL
- URL should look like: `https://open.spotify.com/playlist/...`

**"HTTP 404 Error"**
- Check your Spotify username is correct
- Make sure your Spotify app settings are correct

**"No tracks found"**
- Check your CSV file format
- Make sure columns are named "Artist" and "Song" exactly
- Verify the file path is correct

### Getting Help

If you're stuck:
1. Check that Python and libraries are installed correctly
2. Verify your Spotify API credentials
3. Make sure your CSV file follows the correct format
4. Check that you have internet connection

## ✨ Features

### Smart Search
- Tries multiple search strategies to find songs
- Handles variations in song titles and artist names
- Reports songs that couldn't be found

### Duplicate Detection
- Finds exact duplicate tracks
- Removes duplicates while keeping one copy
- Creates detailed reports of what was removed

### Comprehensive Reports
- Artist breakdowns and statistics
- Song listings organized by artist
- Duplicate analysis
- Summary statistics

### File Management
- Automatically creates organized folder structure
- Prevents file overwrites by adding numbers
- Saves credentials for future use

### Comment Support
- CSV files can include comment lines starting with `#`
- Great for organizing and documenting your music lists

## 🎉 Example Workflow

1. **Prepare your music list** in Excel/Google Sheets
2. **Export as CSV** with "Artist" and "Song" columns
3. **Run the program** and choose option 1
4. **Enter your CSV file path** when prompted
5. **Choose a playlist name**
6. **Wait for the magic** - the program will:
   - Search for each song on Spotify
   - Create your playlist
   - Remove any duplicates
   - Generate detailed reports

## 📝 Tips for Best Results

- **Be specific with artist names** - use the exact name as it appears on Spotify
- **Keep song titles clean** - avoid extra text like "(Official Video)"
- **Use comments in CSV** to organize your music by genre or mood
- **Check the reports** to see which songs weren't found
- **Run analysis** on your playlists to discover patterns in your music

## 🔒 Privacy & Security

- Your credentials are stored locally on your computer
- No data is sent anywhere except to Spotify's official API
- You can delete the cache folder anytime to clear saved credentials
- The tool only requests permissions it needs (playlist management)

---

**Enjoy managing your Spotify playlists like a pro! 🎵**
