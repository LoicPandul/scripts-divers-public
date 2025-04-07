# Create videos with slideshow backgrounds for courses

These scripts allow you to automate the creation of videos using slideshows as visual backgrounds. The videos consist of audio segments synchronized with corresponding slide images, automatically generated using a Python script. This process is configured using a set of YAML files for general settings and language-specific customizations.

### Project Structure

```
COURSE NAME/
│
├── scripts/
│   ├── audio-splitter.py
│   ├── video-creator.py
│   └── slides.py
│
├── fonts/
│   ├── Rubik-Bold.ttf
│   ├── Rubik-Medium.ttf
│   ├── Rubik-Italic.ttf
│   ├── JetBrainsMono-Italic.ttf
│   └── alt/
│       ├── NotoSans-Bold.ttf
│       ├── NotoSansJP-Medium.ttf
│       ├── NotoSansSC-Bold.ttf
│       └── [other alternative font files...]
│
├── img/
│   ├── all white.png
│   ├── all black.png
│   ├── by-sa.png
│   ├── openai.png
│   ├── Eleven_Labs.png
│   ├── instructeur.png
│   ├── waveform.png
│   └── [other image files...]
│
├── config/
│   ├── settings.yaml
│   └── lang/
│       ├── config_cs.yaml
│       ├── config_en.yaml
│       ├── config_fr.yaml
│       ├── config_ja.yaml
│       └── [other language configuration files...]
│
└── chapters/
    ├── 52/
    │   ├── audio/
    │   │   ├── fr/
    │   │   │   ├── 01.wav
    │   │   │   ├── 02.wav
    │   │   │   └── 03.wav
    │   │   └── en/
    │   │       ├── 01.wav
    │   │       ├── 02.wav
    │   │       └── 03.wav
    │   ├── slides/
    │   │   ├── fr/
    │   │   │   ├── 01.png
    │   │   │   ├── 02.png
    │   │   │   └── 03.png
    │   │   └── en/
    │   │       ├── 01.png
    │   │       ├── 02.png
    │   │       └── 03.png
    │   ├── video/
    │   │   ├── fr.mp4
    │   │   └── en.mp4
    │   └── timecodes/
    │       ├── fr.yaml
    │       └── en.yaml
    │
    └── [other chapters...]
```

## Prerequisites

- **Python 3.7 or higher**
- **PIP**

```bash
pip install Pillow colorama pyyaml pydub moviepy
```

- **FFmpeg**: Required by MoviePy for audio and video handling. Install it from the [official FFmpeg site](https://ffmpeg.org/download.html) or via package managers (e.g., `apt-get install ffmpeg` on Ubuntu).

## Configuration

### General Settings (`config/settings.yaml`)

This YAML file defines the general settings for creating slides throughout your training course. You need to fill it with information relevant to your course:

```yaml
# Logos
logos:
  cc_by_sa: "by-sa.png"
  openai: "openai.png"
  eleven_labs: "Eleven_Labs.png"
  pbn_all_white: "all white.png"
  pbn_all_black: "all black.png"
  instructeur_photo: "instructeur.png"
  waveform: "waveform.png"

# General information for the footer
pgp_key: "Plan₿ Network’s PGP: 5720 CD57 7E78 94C9 8DBD 580E 8F12 D0C6 3B1A 606E"
course_code: "BTC204"
version: "V.001"
date: "2024-08"
ia_translated_text: "IA Translated"

# Colors in RGB format
colors:
  white: [255, 255, 255]
  black: [0, 0, 0]
  orange: [255, 92, 0]

# Default languages for slides
default_languages:
  - cs
  - de
  - en
  - es
  - fi
  - fr
  - it
  - ja
  - pt
  - ru
  - vi
```

The default languages are those for which you want to create slides. You should have schemas available in all these languages, or by default, the English schemas will be added to the slides.

### Language-Specific Settings (`config/lang/config_<lang>.yaml`)

Each language has its own configuration file providing translations for certain general text elements across all chapters of the course. Example for French (`config/lang/config_fr.yaml`):

```yaml
# Language code for the footer
lang_code: "FR"

# Translations of texts for slides
instructor: "Instructeur"
by: "By"
chapter: "Chapter"
```

## Usage

### 1. Prepare the Environment

Ensure all required Python libraries are installed and FFmpeg is available on your system.

Fill in the configuration files and translate them.

Make sure you have all the schemas and visuals for your course on your computer. Each schema should be sequentially named and organized as follows:

```txt
assets/
│
├── notext/
│   ├── 11/
│   │   ├── 01.webp
│   │   ├── 03.webp
│   │   └── [other no-text schemas for chapter 1.1...]
│   ├── 12/
│   │   ├── 01.webp
│   │   ├── 04.webp
│   │   └── [other no-text schemas for chapter 1.2...]
│   └── [other chapters...]
│
├── fr/
│   ├── 11/
│   │   ├── 02.webp
│   │   ├── 04.webp
│   │   └── [other French schemas for chapter 1.1...]
│   ├── 12/
│   │   ├── 02.webp
│   │   ├── 03.webp
│   │   └── [other French schemas for chapter 1.2...]
│   └── [other chapters...]
│
├── en/
│   ├── 11/
│   │   ├── 02.webp
│   │   ├── 04.webp
│   │   └── [other English schemas for chapter 1.1...]
│   ├── 12/
│   │   ├── 02.webp
│   │   ├── 03.webp
│   │   └── [other English schemas for chapter 1.2...]
│   └── [other chapters...]
│
└── [other languages...]
```

### 2. Create the Audio

Record your presentation for the chosen chapter. Use editing software to polish your audio. While editing, remember to gradually note the timecodes in the file corresponding to your native language.

These .yaml files are located in: `chapters/<chapter_number>/timecodes/<lang>.yaml`

These files define the chapter number, the main title, and the start time of each slide for each language. Example (`chapters/52/timecodes/fr.yaml`):

```yaml
chpt: 5.2
nm: Zerolink and Chaumian Coinjoins
timecodes:
  - time: "00:00"
    titre: "Zerolink and Chaumian Coinjoins"
  - time: "00:10"
    titre: "The Role of Coinjoin Coordinators"
  # Other timecodes...
```

The audio must always be exported in `.wav` format and named according to its language code. For example, a recording in French should be saved as `fr.wav`. This file should then be placed in the `audio/<lang>/` folder corresponding to the chapter and the language of the recording. For example, for chapter 5.2 recorded in French, the full path will be: `chapters/52/audio/fr/fr.wav`.

### 3. Translate the Timecodes

From your .yaml timecode file, which includes the start times for each slide and the corresponding titles in your language, proceed to translate this file into all necessary languages. You can use an LLM like ChatGPT for quick translations.

Save the translated .yaml files in the `chapters/<chapter_number>/timecodes/` folder, and name them according to the appropriate language code, e.g., `en.yaml`, `fr.yaml`, `ja.yaml`, `cs.yaml`.

### 4. Create the Slides

Run the `slides.py` script to generate slides based on the provided configuration and timecode files.

```bash
python scripts/slides.py
```

The script will prompt you for input:
- The chapter number without a separator (e.g., `11`, `12`, `52`, etc.)
- The full path to the folder containing all schemas for your course (`../assets`)
- The language codes you wish to produce. In any case, the script will process all default languages entered in the general configuration file `settings.yaml`. However, you can add new ones here by noting the two-letter language code. You can enter several separated by commas.

If the script cannot locate the folder containing schemas for a specified language, either in the input or the configuration file, it will default to using the `notext/` and `en/` folders.

### 5. Split the Audio

Run the `audio-splitter.py` script to divide the main audio file into segments based on the timecode files.

```bash
python scripts/audio-splitter.py
```

The script will prompt you for input:
- The chapter number to process (e.g., for chapter 5.2, enter `52`)
- The language code to split (e.g., `fr`)

The script outputs the different audio segments into the same folder as the source audio: `01.wav`, `02.wav`, etc., each corresponding to a slide. You can translate the audio using Eleven Labs and place each translated segment into a language subfolder within the chapter’s `audio/` folder.

### 6. Create the Video

Run the `video-creator.py` script to generate the video by combining the slides and audio segments. Note that this step takes a significant amount of time. For example, on my laptop, generating a 17-minute video took 20 minutes.

```bash
python scripts/video-creator.py
```

The script will prompt you for input:
- The chapter number to process (e.g., `52`)

The script will automatically detect the available language directories and create videos for each language.

After running the scripts, the output videos are categorized into the `chapters/<chapter_number>/video/` folder.

### Fonts

By default, the slide generation script supports all Latin and Cyrillic languages, as well as Vietnamese, Japanese, Simplified Chinese, and Korean. If you want to handle a language not included in these character sets and avoid displaying tofu on the slides, you'll need to add the appropriate .ttf file to the `fonts/alt/` folder and modify the beginning of the script by adding this section for the additional language. For example for the japanese : 

```python
elif lang == 'ja':

            return {

                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 86),

                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 50),

                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Regular.ttf"), 38),

                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Medium.ttf"), 45),

                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),

                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),

            }
```

Please do not modify the "jetbrains" and "italic" fonts that are used for the footer.
