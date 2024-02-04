import os, io, re, shutil, sys, requests, subprocess, datetime, logging
from PIL import Image
from pytube import Playlist
from pytube.exceptions import RegexMatchError, VideoUnavailable

# Constant variables
AUDIO_DIRECTORY = "audio"
COVER_DIRECTORY = "cover_images"

# Configure logging
log_file = 'error.log'  # Specify the name of the log file
logging.basicConfig(filename=log_file, level=logging.ERROR,
                    format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Print error messages with timestamp
def print_error_message(message):
    # Get the timestamp
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    logging.error(message)
    error_message = f"[{formatted_time}] Error: {message}"
    print(error_message)

# Function to download a YouTube video as audio and its cover image
def download_music_with_cover(playlist_title, video):
    try:
        video_name = f"{video.title} - {video.author}".replace("/", "|")
        output_file_name = os.path.join(playlist_title, f"{video_name}.mp3")
        if os.path.exists(output_file_name):
            return

        # Download the audio stream
        audio_stream = video.streams.filter(
            only_audio=True, file_extension='mp4').first()
        audio_file_path = os.path.join(AUDIO_DIRECTORY, f"{video_name}.mp4")
        audio_stream.download(output_path=AUDIO_DIRECTORY,
                              filename=video_name+".mp4")

        # Download the video thumbnail (cover image)
        thumbnail_url = video.thumbnail_url
        response = requests.get(thumbnail_url)
        image_data = response.content

        # Create a Pillow image object and save it
        image = Image.open(io.BytesIO(image_data))
        image_file_name = os.path.join(COVER_DIRECTORY, f"{video_name}.jpg")
        image.save(image_file_name, "JPEG")

        # Redirect both stdout and stderr to the null device (Linux/Unix) or "nul" (Windows)
        stream = open(os.devnull, 'w') if os.name != 'nt' else open("nul", 'w')

        # Combine operations into a single ffmpeg command
        command = [
            'ffmpeg',
            '-i', audio_file_path, # Input the audio file
            '-i', image_file_name, # Input the cover image
            '-map', '0:0',  # Map audio stream from first input
            '-map', '1:0',  # Map image stream from second input
            '-c:a', 'libmp3lame',  # Convert audio to MP3
            '-metadata', f'title={video.title}',  # Set audio title
            '-metadata', f'artist={video.author}',  # Set audio artist
            '-id3v2_version', '3',  # Specify ID3v2 version
            '-n', output_file_name
        ]

        # Execute the command
        subprocess.call(command, stdout=stream, stderr=subprocess.STDOUT)

        # Remove the downloaded MP4, cover image, and temporary MP3 file
        os.remove(audio_file_path)
        os.remove(image_file_name)

    except (RegexMatchError, VideoUnavailable) as e:
        print_error_message(str(e) + '\nVideo URL:' + video.watch_url)
    except Exception as e:
        print_error_message(str(e) + '\nVideo URL:' + video.watch_url)

# Function to download all videos from a playlist
def download_playlist(playlist_url):
    try:
        # Create a YouTube playlist object
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title
        playlist_length = len(playlist.videos)

        print(f"Downloading playlist: {playlist_title}")

        # Create the REQUIRED directories if they don't already exist
        os.makedirs(AUDIO_DIRECTORY, exist_ok=True)
        os.makedirs(COVER_DIRECTORY, exist_ok=True)
        os.makedirs(playlist_title, exist_ok=True)

        # Iterate through the playlist videos and download each one
        for idx, video in enumerate(playlist.videos):
            download_music_with_cover(playlist_title, video)
            progress = ((idx+1) / playlist_length) * 100
            print(
                f"\x1b[6;30;42mProgress: {progress}%\x1b[0m" + " "*10, end="\r")

        print("Download completed!")

    except (RegexMatchError, VideoUnavailable) as e:
        print_error_message(str(e))
    except Exception as e:
        print_error_message(str(e))
    finally:
        try:
            # Safely remove the temporary directories
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
