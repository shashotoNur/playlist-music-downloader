import os, io, re, shutil, sys, requests, subprocess, datetime
from PIL import Image
from pytube import Playlist
from pytube.exceptions import RegexMatchError, VideoUnavailable

# Constant variables
AUDIO_DIRECTORY = "audio"
COVER_DIRECTORY = "cover_images"

# Print error messages with timestamp
def print_error_message(message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"[{formatted_time}] Error: {message}"
    print(error_message)

# Function to download a YouTube video as audio and its cover image
def download_music_with_cover(playlist_title, video):
    try:
        # Create a YouTube object
        streams = video.streams
        audio_stream = streams.filter(
            only_audio=True, file_extension='mp4').first()
        video_name = f"{video.title} - {video.author}"

        # Download the audio stream
        audio_file_path = os.path.join(AUDIO_DIRECTORY, f"{video_name}.mp4")
        audio_stream.download(output_path=AUDIO_DIRECTORY,
                              filename=video_name+".mp4")

        # Download the video thumbnail (cover image)
        thumbnail_url = video.thumbnail_url
        response = requests.get(thumbnail_url)
        image_data = response.content

        # Create a Pillow image object
        image = Image.open(io.BytesIO(image_data))

        # Save the thumbnail as a cover image
        image_file_name = os.path.join(COVER_DIRECTORY, f"{video_name}.jpg")
        image.save(image_file_name, "JPEG")

        # Redirect both stdout and stderr to the null device (Linux/Unix) or "nul" (Windows)
        stream = open(os.devnull, 'w') if os.name != 'nt' else open("nul", 'w')

        # Convert the downloaded audio (in MP4 format) to MP3
        mp3_audio_file_path = os.path.join(
            AUDIO_DIRECTORY, f"{video_name}.mp3")
        subprocess.call(['ffmpeg', '-i', audio_file_path,
                        mp3_audio_file_path], stdout=stream, stderr=subprocess.STDOUT)

        # Merge audio (MP3) and cover image using ffmpeg
        output_file_name = os.path.join(playlist_title, f"{video_name}.mp3")
        subprocess.call(['ffmpeg', '-i', mp3_audio_file_path, '-i', image_file_name, '-map',
                         '0', '-map', '1', '-c', 'copy', '-id3v2_version', '3', '-n', output_file_name], stdout=stream, stderr=subprocess.STDOUT)

        # Remove the downloaded MP4, cover image, and temporary MP3 file
        os.remove(audio_file_path)
        os.remove(image_file_name)
        os.remove(mp3_audio_file_path)

    except (RegexMatchError, VideoUnavailable) as e:
        print_error_message(str(e))
    except Exception as e:
        print_error_message(str(e))

# Function to download all videos from a playlist
def download_playlist(playlist_url):
    try:
        # Create a YouTube playlist object
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title
        print(f"Downloading playlist: {playlist_title}")

        # Create the REQUIRED directories if they don't already exist
        os.makedirs(AUDIO_DIRECTORY, exist_ok=True)
        os.makedirs(COVER_DIRECTORY, exist_ok=True)
        os.makedirs(playlist_title, exist_ok=True)

        # Iterate through the playlist videos and download each one
        for idx, video in enumerate(playlist.videos):
            download_music_with_cover(playlist_title, video)
            print(f"Progress: {(idx+1/len(playlist.videos))*100}%", " " * 10, end="\r")

        print("Download completed!")

    except (RegexMatchError, VideoUnavailable) as e:
        print_error_message(str(e))
    except Exception as e:
        print_error_message(str(e))
    finally:
        # Safely remove the temporary directories
        try:
            shutil.rmtree(AUDIO_DIRECTORY)
            shutil.rmtree(COVER_DIRECTORY)
        except Exception as e:
            print_error_message(str(e))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        playlist_url = input("Please enter your playlist url: ")
    else:
        playlist_url = sys.argv[1]

    # Validate the YouTube playlist URL using a simple regex
    url_pattern = re.compile(
        r'^(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[A-Za-z0-9_-]+(?:&[A-Za-z0-9_=-]+)*$')
    if not url_pattern.match(playlist_url):
        print_error_message(
            "Invalid YouTube playlist URL. Please provide a valid playlist URL.")
        sys.exit(1)

    download_playlist(playlist_url)
