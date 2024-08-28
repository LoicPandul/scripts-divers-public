from PIL import Image, ImageDraw, ImageFont
import os
from colorama import init, Fore, Style
import yaml

init(autoreset=True)

# Shared dimensions, colors, and paths
width, height = 2730, 1536
white = (255, 255, 255)
black = (0, 0, 0)
orange_color = (255, 92, 0)
current_directory = os.path.dirname(__file__)
fonts_path = os.path.join(current_directory, '../fonts')
alt_fonts_path = os.path.join(current_directory, '../fonts/alt')
img_path = os.path.join(current_directory, '../img')
default_languages = ["cs", "de", "en", "es", "fi", "fr", "it", "ja", "pt", "ru", "vi"]

# Load fonts
def load_fonts(lang):
    try:
        if lang == 'ja':
            # Use Noto Sans JP for Japanese
            return {
                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 72),
                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Regular.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Regular.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Regular.ttf"), 20),
            }
        elif lang == 'vi':
            # Use Noto Sans for Vietnamese
            return {
                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Bold.ttf"), 72),
                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Regular.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Regular.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Regular.ttf"), 20),
            }
        else:
            # Use Rubik for all other languages
            return {
                "bold": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 72),
                "regular": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
            }
    except OSError as e:
        print(f"Error loading fonts for language {lang}: {e}")
        exit(1)

# Function to add common footer elements
def add_footer(draw, image, fonts):
    # Black footer bar
    draw.rectangle([0, 1480, 2730, 1536], fill=black)

    # CC BY-SA logo
    logo_cc_by_sa = Image.open(os.path.join(img_path, "by-sa.png")).convert("RGBA").resize((120, 42))
    image.paste(logo_cc_by_sa, (0, height - logo_cc_by_sa.height - 44), logo_cc_by_sa)

    # OpenAI and Eleven Labs logos
    logo_openai = Image.open(os.path.join(img_path, "openai.png")).convert("RGBA").resize((40, 40))
    logo_eleven_labs = Image.open(os.path.join(img_path, "Eleven_Labs.png")).convert("RGBA").resize((40, 40))

    band_height = 56
    offset_y = height - band_height + (band_height - logo_openai.height) // 2
    offset_x = width - logo_openai.width - logo_eleven_labs.width - 25

    image.paste(logo_openai, (offset_x, offset_y), logo_openai)
    image.paste(logo_eleven_labs, (offset_x + logo_openai.width + 10, offset_y), logo_eleven_labs)

    # IA Translated text
    text_ia_translated = "IA Translated"
    draw.text((offset_x - 140, offset_y), text_ia_translated, font=fonts["italic"], fill=white)

    # PGP Key text
    pgp_text = "BTC204 - FR - V.001 - 2024-08 - Plan₿ Network’s PGP: 5720 CD57 7E78 94C9 8DBD 580E 8F12 D0C6 3B1A 606E"
    draw.text((20, 1488), pgp_text, font=fonts["jetbrains"], fill=white)

# Function to draw a dashed rounded rectangle
def draw_dashed_rounded_rectangle(draw, xy, outline, width=8):
    left, top, right, bottom = xy
    corner_radius = 10
    dash_length = 30
    gap_length = 20

    # Circle segments for rounded corners
    draw.arc([left, top, left + 2 * corner_radius, top + 2 * corner_radius], start=180, end=270, fill=outline, width=width)
    draw.arc([right - 2 * corner_radius, top, right, top + 2 * corner_radius], start=270, end=360, fill=outline, width=width)
    draw.arc([right - 2 * corner_radius, bottom - 2 * corner_radius, right, bottom], start=0, end=90, fill=outline, width=width)
    draw.arc([left, bottom - 2 * corner_radius, left + 2 * corner_radius, bottom], start=90, end=180, fill=outline, width=width)
    
    # Straight line segments
    for x in range(left + corner_radius, right - corner_radius, dash_length + gap_length):
        draw.line([(x, top), (min(x + dash_length, right - corner_radius), top)], fill=outline, width=width)
        draw.line([(x, bottom), (min(x + dash_length, right - corner_radius), bottom)], fill=outline, width=width)
    
    for y in range(top + corner_radius, bottom - corner_radius, dash_length + gap_length):
        draw.line([(left, y), (left, min(y + dash_length, bottom - corner_radius))], fill=outline, width=width)
        draw.line([(right, y), (right, min(y + dash_length, bottom - corner_radius))], fill=outline, width=width)

# Function to load YAML data
def load_yaml_data(chapter, lang):
    yaml_path = os.path.join(current_directory, f"../chapters/{chapter}/timecodes/{lang}.yaml")
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: YAML file for language '{lang}' not found in chapter {chapter}.")
        return None

# Function to create introduction slide
def create_intro_slide(output_folder, yaml_data, fonts):
    image_intro = Image.new("RGB", (width, height), orange_color)
    draw_intro = ImageDraw.Draw(image_intro)
    
    chapter_text = yaml_data.get("chpt", "Unknown Chapter")
    name_text = yaml_data.get("nm", "No Name")
    chapter_label = yaml_data.get("Chapitre", "Chapitre")
    author_label = yaml_data.get("Par", "Par")

    # Specific elements for intro slide
    draw_intro.rectangle([200, 600, 214, 800], fill=white)
    draw_intro.text((240, 600), name_text, font=fonts["bold"], fill=white)
    draw_intro.text((240, 720), f"{chapter_label} {chapter_text} - {author_label} Loïc Morel", font=fonts["regular"], fill=black)

    # PBN white logo (intro slide)
    logo_all_white = Image.open(os.path.join(img_path, "all white.png")).convert("RGBA")
    logo_all_white.thumbnail((185, 185))
    image_intro.paste(logo_all_white, (width - logo_all_white.size[0] - 50, 50), logo_all_white)

    add_footer(draw_intro, image_intro, fonts)

    # Save the intro slide
    output_file_intro = os.path.join(output_folder, "01.png")
    image_intro.save(output_file_intro)
    print(f"Intro slide successfully saved in: {output_file_intro}")

# Function to create main slides with schemas
def create_main_slide(output_folder, schema_path, slide_number, yaml_data, timecode_index, fonts):
    image_main = Image.new("RGB", (width, height), white)
    draw_main = ImageDraw.Draw(image_main)
    
    chapter_text = yaml_data.get("chpt", "Unknown Chapter")
    name_text = yaml_data.get("nm", "No Name")
    chapter_label = yaml_data.get("Chapitre", "Chapitre")
    title_text = yaml_data["timecodes"][timecode_index].get("titre", "No Title")

    # Specific elements for main slide
    draw_main.text((50, 50), f"{chapter_label} {chapter_text} - {name_text}", font=fonts["regular"], fill=black)
    draw_main.rectangle([50, 125, 75, 275], fill=orange_color)
    draw_main.text((120, 160), title_text, font=fonts["bold2"], fill=black)

    right_rect_width = width // 5
    draw_main.rectangle([width - right_rect_width, 0, width, height], fill=orange_color)

    # PBN black logo (main slides)
    logo_planb = Image.open(os.path.join(img_path, "all black.png")).convert("RGBA")
    logo_planb.thumbnail((185, 185))
    image_main.paste(logo_planb, (width - logo_planb.size[0] - 50, 50), logo_planb)

    # Adjusted position for instructor text, photo, and waveform
    instructor_text_y = 400
    photo_y = instructor_text_y + 120
    waveform_y = 800

    # Use a default value for the instructor if the key is not found
    instructor_label = yaml_data.get("Instructeur", "Instructeur")
    
    # Width of the instructor photo
    photo_width = 400
    photo_center_x = width - right_rect_width + 73 + (photo_width // 2)

    # Width of the instructor text
    text_width = draw_main.textbbox((0, 0), instructor_label, font=fonts["medium"])[2]

    # x position of img instructor
    text_x = photo_center_x - (text_width // 2)

    # Draw the centered instructor text
    draw_main.text((text_x, instructor_text_y), instructor_label, font=fonts["medium"], fill=black)

    instructor_photo = Image.open(os.path.join(img_path, "instructeur.png")).convert("RGBA")
    instructor_photo.thumbnail((400, 400))
    instructor_photo_width, instructor_photo_height = instructor_photo.size
    image_main.paste(instructor_photo, (width - right_rect_width + 73, photo_y), instructor_photo)

    waveform = Image.open(os.path.join(img_path, "waveform.png")).convert("RGBA")
    waveform = waveform.resize((right_rect_width - 5, 700))
    image_main.paste(waveform, (width - right_rect_width + 5, waveform_y), waveform)

    draw_dashed_rounded_rectangle(draw_main, [200, 350, width - right_rect_width - 200, height - 200], outline=orange_color, width=8)

    # Adding schema img to the main slide
    try:
        schema_image = Image.open(schema_path).convert("RGBA")
    except (OSError, IOError) as e:
        print(f"Error opening image {schema_path}: {e}")
        return

    # Increase the resolution of the schema image
    original_width, original_height = schema_image.size
    high_res_width, high_res_height = original_width * 2, original_height * 2
    schema_image = schema_image.resize((high_res_width, high_res_height), Image.LANCZOS)

    # Images size
    margin = 55

    frame_left, frame_top, frame_right, frame_bottom = (
        200 + margin, 
        350 + margin, 
        width - right_rect_width - 200 - margin, 
        height - 200 - margin
    )

    max_width = frame_right - frame_left
    max_height = frame_bottom - frame_top

    aspect_ratio = schema_image.width / schema_image.height

    # Resize the image to fit
    if schema_image.width > max_width or schema_image.height > max_height:
        if schema_image.width / max_width > schema_image.height / max_height:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        schema_image = schema_image.resize((new_width, new_height), Image.LANCZOS)

    # Check if the img has transparency
    has_transparency = schema_image.mode == "RGBA" and schema_image.getextrema()[3][0] < 255

    # Apply rounded corners only to no transparency img
    if not has_transparency:
        corner_radius = 30
        mask = Image.new("L", schema_image.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, schema_image.size[0], schema_image.size[1]], corner_radius, fill=255)
        schema_image.putalpha(mask)

    # White BG for non-transparent images
    background = Image.new("RGBA", schema_image.size, (255, 255, 255, 0))
    background.paste(schema_image, (0, 0), schema_image)

    # Center img
    center_x = frame_left + (frame_right - frame_left - schema_image.width) // 2
    center_y = frame_top + (frame_bottom - frame_top - schema_image.height) // 2

    # Paste img
    image_main.paste(schema_image, (center_x, center_y), schema_image)

    add_footer(draw_main, image_main, fonts)

    # Save the main slide
    output_file_main = os.path.join(output_folder, f"{slide_number:02}.png")
    image_main.save(output_file_main)
    print(f"{Style.DIM}Slide {slide_number} successfully saved.")

# Main script
if __name__ == "__main__":
    chapter = input("Enter the chapter number (e.g., 52): ").strip()
    assets_path = input("Enter the full path to the assets folder: ").strip().strip('"')

    languages_input = input(f"Enter the languages codes to add (comma-separated) or press Enter for only default [{', '.join(default_languages)}]: ").strip()
    
    # Combine default languages with user input languages
    languages = set(default_languages)
    if languages_input:
        input_languages = {lang.strip() for lang in languages_input.split(',')}
        languages.update(input_languages)
    languages = list(languages)

    base_chapter_path = os.path.join(current_directory, "../chapters", chapter)
    notext_path = os.path.join(assets_path, "notext", chapter)
    
    for lang in languages:
        lang_path = os.path.join(assets_path, lang, chapter)
        output_folder = os.path.join(base_chapter_path, "slides", lang)
        os.makedirs(output_folder, exist_ok=True)

        # Load YAML data for the current language
        yaml_data = load_yaml_data(chapter, lang)
        if yaml_data is None:
            continue

        # Load fonts based on the current language
        fonts = load_fonts(lang)

        # Check if the language directory exists, otherwise "en" as default
        if not os.path.exists(lang_path):
            print(f"{Fore.YELLOW}Warning: Directory for language '{lang}' not found. Using English (en) as default.")
            lang_path = os.path.join(assets_path, 'en', chapter)

        # Create the intro slide
        create_intro_slide(output_folder, yaml_data, fonts)

        slide_number = 2  # Start after intro
        timecode_index = 1  # Start at second timecode (first is intro)

        if os.path.exists(lang_path):
            for image_name in sorted(os.listdir(lang_path)):
                if image_name.endswith(".webp"):
                    create_main_slide(output_folder, os.path.join(lang_path, image_name), slide_number, yaml_data, timecode_index, fonts)
                    slide_number += 1
                    timecode_index += 1

        if os.path.exists(notext_path):
            for image_name in sorted(os.listdir(notext_path)):
                if image_name.endswith(".webp"):
                    create_main_slide(output_folder, os.path.join(notext_path, image_name), slide_number, yaml_data, timecode_index, fonts)
                    slide_number += 1
                    timecode_index += 1

        print(f"{Style.BRIGHT}{Fore.CYAN}Slides created for language: {lang}")

    # Handle case when only /notext exists
    if not os.listdir(os.path.join(base_chapter_path, "slides")):
        output_folder = os.path.join(base_chapter_path, "slides", "gen")
        os.makedirs(output_folder, exist_ok=True)
        create_intro_slide(output_folder, yaml_data, fonts)

        slide_number = 2
        timecode_index = 1

        for image_name in sorted(os.listdir(notext_path)):
            if image_name.endswith(".webp"):
                create_main_slide(output_folder, os.path.join(notext_path, image_name), slide_number, yaml_data, timecode_index, fonts)
                slide_number += 1
                timecode_index += 1

        print(f"{Style.BRIGHT}{Fore.CYAN}General slides created in: {output_folder}")
