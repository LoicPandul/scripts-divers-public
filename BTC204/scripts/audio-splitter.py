from pydub import AudioSegment
from colorama import init, Fore, Style
import os
import yaml

init(autoreset=True)

current_directory = os.path.dirname(__file__)

# Convert time string "MM:SS" to milliseconds
def time_to_milliseconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return (minutes * 60 + seconds) * 1000
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

# Format seconds MM:SS
def seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Split audio
def split_audio(chapter, lang, timecodes):
    audio_path = os.path.join(current_directory, f"../chapters/{chapter}/audio/{lang}/{lang}.mp3")
    output_folder = os.path.join(current_directory, f"../chapters/{chapter}/audio/{lang}")

    audio = AudioSegment.from_mp3(audio_path)
    
    for index, timecode in enumerate(timecodes):
        try:
            start_time = time_to_milliseconds(timecode['time'])
            
            if index + 1 < len(timecodes):
                next_time = timecodes[index + 1]['time']
                end_time = time_to_milliseconds(next_time)
            else:
                end_time = len(audio)

            segment = audio[start_time:end_time]
            segment.export(os.path.join(output_folder, f"{index + 1:02}.mp3"), format="mp3")

            print(f"{Style.DIM}- Segment {index + 1:02}.mp3 created from {timecode['time']} to {next_time if index + 1 < len(timecodes) else 'end of file'}")
        except ValueError as e:
            print(f"{Fore.RED}Error processing segment {index + 1}: {e}")

# Main script
if __name__ == "__main__":
    chapter = input(f"{Fore.LIGHTBLUE_EX}Enter the chapter number (e.g., 52): {Style.RESET_ALL}").strip()
    lang = input(f"{Fore.LIGHTBLUE_EX}Enter the language code (e.g., fr, en): {Style.RESET_ALL}").strip()

    yaml_path = os.path.join(current_directory, f"../chapters/{chapter}/timecodes/{lang}.yaml")
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
            timecodes = yaml_data['timecodes']
    except FileNotFoundError:
        print(f"{Fore.RED}Error: YAML file for language '{lang}' not found in chapter {chapter}.")
    except yaml.YAMLError as e:
        print(f"{Fore.RED}Error reading YAML file: {e}")
    
    split_audio(chapter, lang, timecodes)

    print(f"{Fore.GREEN}THE SCRIPT HAS FINISHED!{Style.RESET_ALL}")
