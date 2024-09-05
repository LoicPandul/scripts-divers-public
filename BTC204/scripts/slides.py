from PIL import Image, ImageDraw, ImageFont
import os
from colorama import init, Fore, Style
import yaml

init(autoreset=True)

# Current directory
current_directory = os.path.dirname(__file__)

# Shared dimensions
width, height = 2730, 1536

# Load settings from settings.yaml
def load_general_settings():
    settings_path = os.path.join(current_directory, '../config/settings.yaml')
    try:
        with open(settings_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: General settings file 'settings.yaml' not found.")
        exit(1)

# Load language-specific settings
def load_language_settings(lang):
    lang_settings_path = os.path.join(current_directory, f'../config/lang/config_{lang}.yaml')
    try:
        with open(lang_settings_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Language settings file for '{lang}' not found.")
        exit(1)

# Load timecode data for a specific chapter and language
def load_timecode_data(chapter, lang):
    yaml_path = os.path.join(current_directory, f"../chapters/{chapter}/timecodes/{lang}.yaml")
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: YAML file for language '{lang}' not found in chapter {chapter}.")
        return None

# Load fonts
def load_fonts(settings, lang):
    fonts_path = os.path.join(current_directory, '../fonts')
    alt_fonts_path = os.path.join(current_directory, '../fonts/alt')
    
    try:
        if lang == 'ja':
            return {
                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 86),
                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Bold.ttf"), 50),
                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Regular.ttf"), 38),
                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansJP-Medium.ttf"), 45),
                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
            }
        elif lang == 'vi':
            return {
                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Bold.ttf"), 60),
                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Regular.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSans-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
            }
        elif lang == 'zh-hans':
            return {
                "bold": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansSC-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansSC-Bold.ttf"), 60),
                "regular": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansSC-Regular.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(alt_fonts_path, "NotoSansSC-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
            }
        else:
            return {
                "bold": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 96),
                "bold2": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 60),
                "regular": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 48),
                "medium": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 55),
                "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
                "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
            }
    except OSError as e:
        print(f"Error loading fonts for language {lang}: {e}")
        exit(1)

# Add common footer elements
def add_footer(draw, image, fonts, settings, lang_settings):
    colors = settings['colors']
    footer_text = settings['ia_translated_text']
    
    draw.rectangle([0, 1480, width, height], fill=tuple(colors['black']))
    
    logo_cc_by_sa = Image.open(os.path.join(current_directory, '../img', settings['logos']['cc_by_sa'])).convert("RGBA").resize((120, 42))
    image.paste(logo_cc_by_sa, (0, 1450), logo_cc_by_sa)

    logo_openai = Image.open(os.path.join(current_directory, '../img', settings['logos']['openai'])).convert("RGBA").resize((40, 40))
    logo_eleven_labs = Image.open(os.path.join(current_directory, '../img', settings['logos']['eleven_labs'])).convert("RGBA").resize((40, 40))
    
    band_height = 56
    offset_y = height - band_height + (band_height - logo_openai.height) // 2
    offset_x = width - logo_openai.width - logo_eleven_labs.width - 25

    image.paste(logo_openai, (offset_x, offset_y), logo_openai)
    image.paste(logo_eleven_labs, (offset_x + logo_openai.width + 10, offset_y), logo_eleven_labs)

    draw.text((offset_x - 150, offset_y + 8), footer_text, font=fonts["italic"], fill=tuple(colors['white']))

    pgp_key = settings['pgp_key']
    course_code = settings['course_code']
    lang_code = lang_settings['lang_code']
    date = settings['date']
    version = settings['version']
    footer_full_text = f"{course_code} - {lang_code} - {version} - {date} - {pgp_key}"
    draw.text((20, 1492), footer_full_text, font=fonts["jetbrains"], fill=tuple(colors['white']))

# Create introduction slide
def create_intro_slide(output_folder, yaml_data, fonts, settings, lang_settings):
    colors = settings['colors']
    image_intro = Image.new("RGB", (2730, 1536), tuple(colors['orange']))
    draw_intro = ImageDraw.Draw(image_intro)
    
    chapter_text = yaml_data.get("chpt", "Unknown Chapter")
    name_text = yaml_data.get("nm", "No Name")
    chapter_label = lang_settings["chapter"]
    author_label = lang_settings["by"]

    draw_intro.rectangle([200, 600, 214, 800], fill=tuple(colors['white']))
    draw_intro.text((240, 600), name_text, font=fonts["bold"], fill=tuple(colors['white']))
    draw_intro.text((240, 720), f"{chapter_label} {chapter_text} - {author_label} Loïc Morel", font=fonts["regular"], fill=tuple(colors['black']))

    logo_all_white = Image.open(os.path.join(current_directory, '../img', settings['logos']['pbn_all_white'])).convert("RGBA")
    logo_all_white.thumbnail((185, 185))
    image_intro.paste(logo_all_white, (2730 - logo_all_white.size[0] - 50, 50), logo_all_white)

    add_footer(draw_intro, image_intro, fonts, settings, lang_settings)

    output_file_intro = os.path.join(output_folder, "01.png")
    image_intro.save(output_file_intro)
    print(f"{Style.DIM}- Slide 01 created (intro)")

# Function to draw a dashed rounded rectangle
def draw_dashed_rounded_rectangle(draw, xy, outline, width=8):
    left, top, right, bottom = xy
    corner_radius = 10
    dash_length = 30
    gap_length = 20

    # Draw the corners
    draw.arc([left, top, left + 2 * corner_radius, top + 2 * corner_radius], start=180, end=270, fill=outline, width=width)
    draw.arc([right - 2 * corner_radius, top, right, top + 2 * corner_radius], start=270, end=360, fill=outline, width=width)
    draw.arc([right - 2 * corner_radius, bottom - 2 * corner_radius, right, bottom], start=0, end=90, fill=outline, width=width)
    draw.arc([left, bottom - 2 * corner_radius, left + 2 * corner_radius, bottom], start=90, end=180, fill=outline, width=width)

    # Draw the dashed lines
    for x in range(left + corner_radius, right - corner_radius, dash_length + gap_length):
        draw.line([(x, top), (min(x + dash_length, right - corner_radius), top)], fill=outline, width=width)
        draw.line([(x, bottom), (min(x + dash_length, right - corner_radius), bottom)], fill=outline, width=width)

    for y in range(top + corner_radius, bottom - corner_radius, dash_length + gap_length):
        draw.line([(left, y), (left, min(y + dash_length, bottom - corner_radius))], fill=outline, width=width)
        draw.line([(right, y), (right, min(y + dash_length, bottom - corner_radius))], fill=outline, width=width)

# Create main slides with schemas
def create_main_slide(output_folder, schema_path, slide_number, yaml_data, timecode_index, fonts, settings, lang_settings):
    colors = settings['colors']
    image_main = Image.new("RGB", (2730, 1536), tuple(colors['white']))
    draw_main = ImageDraw.Draw(image_main)
    
    chapter_text = yaml_data.get("chpt", "Unknown Chapter")
    name_text = yaml_data.get("nm", "No Name")
    chapter_label = lang_settings["chapter"]
    title_text = yaml_data["timecodes"][timecode_index].get("titre", "No Title")

    draw_main.text((50, 50), f"{chapter_label} {chapter_text} - {name_text}", font=fonts["regular"], fill=tuple(colors['black']))
    draw_main.rectangle([50, 125, 75, 275], fill=tuple(colors['orange']))
    draw_main.text((120, 160), title_text, font=fonts["bold2"], fill=tuple(colors['black']))

    right_rect_width = 2730 // 5
    draw_main.rectangle([2730 - right_rect_width, 0, 2730, 1536], fill=tuple(colors['orange']))

    logo_planb = Image.open(os.path.join(current_directory, '../img', settings['logos']['pbn_all_black'])).convert("RGBA")
    logo_planb.thumbnail((185, 185))
    image_main.paste(logo_planb, (2730 - logo_planb.size[0] - 50, 50), logo_planb)

    instructor_label = lang_settings.get("instructor", "Instructeur")
    photo_center_x = 2730 - right_rect_width + 73 + (400 // 2)
    text_width = draw_main.textbbox((0, 0), instructor_label, font=fonts["medium"])[2]
    text_x = photo_center_x - (text_width // 2)
    draw_main.text((text_x, 400), instructor_label, font=fonts["medium"], fill=tuple(colors['black']))

    instructor_photo = Image.open(os.path.join(current_directory, '../img', settings['logos']['instructeur_photo'])).convert("RGBA")
    instructor_photo.thumbnail((400, 400))
    image_main.paste(instructor_photo, (2730 - right_rect_width + 73, 520), instructor_photo)

    waveform = Image.open(os.path.join(current_directory, '../img', settings['logos']['waveform'])).convert("RGBA")
    waveform = waveform.resize((right_rect_width - 5, 700))
    image_main.paste(waveform, (2730 - right_rect_width + 5, 800), waveform)

    draw_dashed_rounded_rectangle(draw_main, [200, 350, 2730 - right_rect_width - 200, 1536 - 200], outline=tuple(colors['orange']), width=8)

    try:
        schema_image = Image.open(schema_path).convert("RGBA")
    except (OSError, IOError) as e:
        print(f"Error opening image {schema_path}: {e}")
        return

    original_width, original_height = schema_image.size
    high_res_width, high_res_height = original_width * 2, original_height * 2
    schema_image = schema_image.resize((high_res_width, high_res_height), Image.LANCZOS)

    margin = 55

    frame_left, frame_top, frame_right, frame_bottom = (
        200 + margin, 
        350 + margin, 
        2730 - right_rect_width - 200 - margin, 
        1536 - 200 - margin
    )

    max_width = frame_right - frame_left
    max_height = frame_bottom - frame_top

    aspect_ratio = schema_image.width / schema_image.height

    if schema_image.width > max_width or schema_image.height > max_height:
        if schema_image.width / max_width > schema_image.height / max_height:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        schema_image = schema_image.resize((new_width, new_height), Image.LANCZOS)

    has_transparency = schema_image.mode == "RGBA" and schema_image.getextrema()[3][0] < 255

    if not has_transparency:
        corner_radius = 30
        mask = Image.new("L", schema_image.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, schema_image.size[0], schema_image.size[1]], corner_radius, fill=255)
        schema_image.putalpha(mask)

    background = Image.new("RGBA", schema_image.size, (255, 255, 255, 0))
    background.paste(schema_image, (0, 0), schema_image)

    center_x = frame_left + (frame_right - frame_left - schema_image.width) // 2
    center_y = frame_top + (frame_bottom - frame_top - schema_image.height) // 2

    image_main.paste(schema_image, (center_x, center_y), schema_image)

    add_footer(draw_main, image_main, fonts, settings, lang_settings)

    output_file_main = os.path.join(output_folder, f"{slide_number:02}.png")
    image_main.save(output_file_main)
    print(f"{Style.DIM}- Slide {slide_number:02} created")

# Main script
if __name__ == "__main__":
    settings = load_general_settings()

    chapter = input(f"{Fore.LIGHTBLUE_EX}Enter the chapter number (e.g., 52): {Style.RESET_ALL}").strip()
    assets_path = input("Enter the full path to the assets folder: ").strip().strip('"')

    languages_input = input(f"{Fore.LIGHTBLUE_EX}Enter the languages codes to add (comma-separated) or press Enter for only default [{', '.join(settings['default_languages'])}]: ").strip()
    
    languages = set(settings['default_languages'])
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

        yaml_data = load_timecode_data(chapter, lang)
        if yaml_data is None:
            continue

        lang_settings = load_language_settings(lang)
        fonts = load_fonts(settings, lang)

        if not os.path.exists(lang_path):
            print(f"{Fore.YELLOW}Warning: Directory for language '{lang}' not found. Using English (en) as default.")
            lang_path = os.path.join(assets_path, 'en', chapter)

        create_intro_slide(output_folder, yaml_data, fonts, settings, lang_settings)

        slide_number = 2
        timecode_index = 1

        if os.path.exists(lang_path):
            for image_name in sorted(os.listdir(lang_path)):
                if image_name.endswith(".webp"):
                    create_main_slide(output_folder, os.path.join(lang_path, image_name), slide_number, yaml_data, timecode_index, fonts, settings, lang_settings)
                    slide_number += 1
                    timecode_index += 1

        if os.path.exists(notext_path):
            for image_name in sorted(os.listdir(notext_path)):
                if image_name.endswith(".webp"):
                    create_main_slide(output_folder, os.path.join(notext_path, image_name), slide_number, yaml_data, timecode_index, fonts, settings, lang_settings)
                    slide_number += 1
                    timecode_index += 1

        print(f"{Style.BRIGHT}{Fore.CYAN}Slides created for language: {lang}")

    print(f"{Fore.GREEN}THE SCRIPT HAS FINISHED!{Style.RESET_ALL}")
