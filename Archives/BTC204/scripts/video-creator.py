from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from colorama import init, Fore, Style
import os

init(autoreset=True)

current_directory = os.path.dirname(__file__)

# Create video from images and audio
def create_video(chapter, lang):
    audio_folder = os.path.join(current_directory, f"../chapters/{chapter}/audio/{lang}")
    slides_folder = os.path.join(current_directory, f"../chapters/{chapter}/slides/{lang}")
    video_folder = os.path.join(current_directory, f"../chapters/{chapter}/video")
    os.makedirs(video_folder, exist_ok=True)

    # List all audio and image files, sorted by name
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith((".wav", ".mp3"))])
    slide_files = sorted([f for f in os.listdir(slides_folder) if f.endswith(".png")])

    clips = []

    for i, (audio_file, slide_file) in enumerate(zip(audio_files, slide_files)):
        audio_path = os.path.join(audio_folder, audio_file)
        slide_path = os.path.join(slides_folder, slide_file)

        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(slide_path).set_duration(audio_clip.duration)
        image_clip = image_clip.set_audio(audio_clip)

        # No overlap or transition
        if i > 0:
            prev_clip = clips[-1]
            prev_clip.set_end(prev_clip.end)

        clips.append(image_clip)

        print(f"{Style.DIM}- Created video segment for {audio_file} with {slide_file}")

    final_video = concatenate_videoclips(clips, method="compose", padding=-0.01)
    output_video_path = os.path.join(video_folder, f"{lang}.mp4")
    final_video.write_videofile(output_video_path, codec="libx264", fps=24, audio_codec="aac")

    print(f"{Fore.GREEN}Video created successfully for language '{lang}' in chapter '{chapter}'.")

# Main script
if __name__ == "__main__":
    chapter = input(f"{Fore.LIGHTBLUE_EX}Enter the chapter number (e.g., 52): {Style.RESET_ALL}").strip()
    
    # Path audio/ folder
    audio_base_path = os.path.join(current_directory, f"../chapters/{chapter}/audio")
    
    # List of language directories audio/ folder
    languages = [d for d in os.listdir(audio_base_path) if os.path.isdir(os.path.join(audio_base_path, d))]

    if not languages:
        print(f"{Fore.RED}No language directories found in chapter '{chapter}'. Exiting.")
        exit(1)

    for lang in languages:
        print(f"{Fore.CYAN}Processing video creation for language: {lang}")
        create_video(chapter, lang)
