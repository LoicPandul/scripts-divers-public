from pydub import AudioSegment
from colorama import init, Fore, Style
import os
import yaml
import sys
import time
import threading

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

# Processing animation
def show_processing(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Processing... {spinner[idx % len(spinner)]}{Style.RESET_ALL}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")

# Split audio
def split_audio(chapter, lang, timecodes):
    audio_path = os.path.join(current_directory, f"../chapters/{chapter}/audio/{lang}/{lang}.wav")
    output_folder = os.path.join(current_directory, f"../chapters/{chapter}/audio/{lang}")

    audio = AudioSegment.from_wav(audio_path)
    
    for index, timecode in enumerate(timecodes):
        try:
            start_time = time_to_milliseconds(timecode['time'])
            
            if index + 1 < len(timecodes):
                next_time = timecodes[index + 1]['time']
                end_time = time_to_milliseconds(next_time)
            else:
                end_time = len(audio)

            segment = audio[start_time:end_time]
            segment.export(os.path.join(output_folder, f"{index + 1:02}.wav"), format="wav")

            print(f"{Style.DIM}- Segment {index + 1:02}.wav created from {timecode['time']} to {next_time if index + 1 < len(timecodes) else 'end of file'}")
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
    
    # Start the processing animation
    stop_event = threading.Event()
    processing_thread = threading.Thread(target=show_processing, args=(stop_event,))
    processing_thread.start()

    try:
        split_audio(chapter, lang, timecodes)
    finally:
        stop_event.set()
        processing_thread.join()

    print(f"{Fore.GREEN}THE SCRIPT HAS FINISHED!{Style.RESET_ALL}")
