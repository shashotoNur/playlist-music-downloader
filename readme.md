# Playlist Music Downloader

## Overview

This Python script allows you to download audio from videos in a YouTube playlist, embed a cover image into the audio, and save the final MP3 files. It is a convenient tool for creating a collection of music from your favorite YouTube playlists while preserving cover art.

## Features

- Downloads audio from a YouTube playlist.
- Embeds the video's cover image into the audio as album art.
- Saves the final MP3 files in a designated directory.
- Automatically removes temporary MP4 and image files (optional).

## Prerequisites

Before using this script, ensure you have the following dependencies installed:

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone or download this repository to your local machine.

   ```bash
   git clone https://github.com/shashoto-nur/playlist-music-downloader.git
   ```

2. Navigate to the project directory.

   ```bash
   cd playlist-music-downloader
   ```

3. Install the required Python packages.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script with the URL of the YouTube playlist you want to download.

   ```bash
   python index.py https://www.youtube.com/playlist?list=your_playlist_id
   ```

2. The script will start downloading audio from each video in the playlist.

3. Once the process is complete, the MP3 files with embedded cover images will be saved in the "Music" directory.

4. Temporary MP4 and image files will be removed automatically (configurable in the script).

## Configuration

You can customize the script by modifying the following constants in the script:

- `AUDIO_DIRECTORY`: Directory to store downloaded audio files (MP4 format).
- `COVER_DIRECTORY`: Directory to store downloaded cover images (JPEG format).

## Code Explanation

1. **Importing Libraries and Setting Constants:**

   The code starts by importing necessary libraries and defining some constants.

   - `os`: For file and directory operations.
   - `io`: For working with byte streams.
   - `re`: For regular expressions used for URL validation.
   - `shutil`: For removing directories and their contents.
   - `sys`: To access command-line arguments.
   - `requests`: To send HTTP requests to fetch the video thumbnail (cover image).
   - `subprocess`: To call external commands (e.g., `ffmpeg`).
   - `Image` (from PIL): For handling and saving cover images.
   - `pytube` (from pytube import YouTube): To download YouTube videos and retrieve their information.
   - `RegexMatchError`, `VideoUnavailable` (from pytube.exceptions): Exceptions from the `pytube` library.

   Constants:
   - `AUDIO_DIRECTORY`: The directory to store downloaded audio (MP4) files.
   - `COVER_DIRECTORY`: The directory to store downloaded cover images (JPEG).

2. **`download_music_with_cover` Function:**

   This function downloads a single YouTube video's audio and cover image, embeds the cover image into the audio, and saves the final MP3 file. Here are the key steps:

   - Create a YouTube object using the provided video URL.
   - Get the best audio stream (MP4 format) available for the video.
   - Download the audio stream and save it as an MP4 file in the `AUDIO_DIRECTORY`.
   - Fetch the video thumbnail (cover image) URL.
   - Download the thumbnail and create a Pillow image object from the byte data.
   - Save the thumbnail as a JPEG cover image in the `COVER_DIRECTORY`.
   - Use `ffmpeg` to merge the audio and cover image into an MP3 file in the `PLAYLIST_DIRECTORY`.
   - Remove the temporary MP4 and cover image files.

3. **`download_playlist` Function:**

   This function downloads all videos from a YouTube playlist. Here are the key steps:

   - Create the required directories (`AUDIO_DIRECTORY`, `COVER_DIRECTORY`, and `PLAYLIST_DIRECTORY`) if they don't already exist.
   - Create a YouTube playlist object using the provided playlist URL.
   - Iterate through the playlist videos and call `download_music_with_cover` for each video.
   - After all videos are processed, remove the temporary `AUDIO_DIRECTORY` and `COVER_DIRECTORY`.

4. **Main Execution:**

   - Check if the script is executed with the correct number of command-line arguments (the playlist URL).
   - Validate the YouTube playlist URL using a regex pattern.
   - Call the `download_playlist` function to start downloading audio with cover images from the playlist.

The script will proceed to download each video in the playlist, convert the audio to an MP3 file with an embedded cover image, save it in the specified `PLAYLIST_DIRECTORY`, and remove the temporary files stored in `AUDIO_DIRECTORY` and `COVER_DIRECTORY`.

## Additional Notes

- This script uses external tools like `ffmpeg` for audio and image merging. Ensure you have `ffmpeg` installed on your system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pytube](https://github.com/nficano/pytube) - A Python library for accessing and downloading YouTube videos.
- [Autopep8](https://pypi.org/project/autopep8/) - A Python code formatter used for code formatting.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.
