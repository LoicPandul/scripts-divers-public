from PIL import Image, ImageDraw, ImageFont
import os

# Shared dimensions, colors, and paths
width, height = 2730, 1536
white = (255, 255, 255)
black = (0, 0, 0)
orange_color = (255, 92, 0)
current_directory = os.path.dirname(__file__)
fonts_path = os.path.join(current_directory, '../fonts')
img_path = os.path.join(current_directory, '../img')

# Load fonts
def load_fonts():
    try:
        return {
            "bold": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 96),
            "bold2": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 72),
            "regular": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 48),
            "medium": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 55),
            "jetbrains": ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24),
            "italic": ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20),
        }
    except OSError as e:
        print(f"Error loading fonts: {e}")
        exit(1)

fonts = load_fonts()

# Function to add common footer elements
def add_footer(draw, image):
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
    bbox = fonts["italic"].getbbox(text_ia_translated)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_x = offset_x - text_width - 20
    text_y = height - band_height + (band_height - text_height) // 2
    draw.text((text_x, text_y), text_ia_translated, font=fonts["italic"], fill=white)

    # PGP Key text
    draw.text((20, 1488), "BTC204 - FR - V.001 - 2024-08 - Plan₿ Network’s PGP: 5720 CD57 7E78 94C9 8DBD 580E 8F12 D0C6 3B1A 606E", font=fonts["jetbrains"], fill=white)

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

# Function to create introduction slide
def create_intro_slide():
    image_intro = Image.new("RGB", (width, height), orange_color)
    draw_intro = ImageDraw.Draw(image_intro)
    
    # Specific elements for intro slide
    draw_intro.rectangle([200, 600, 214, 800], fill=white)
    draw_intro.text((240, 600), "name", font=fonts["bold"], fill=white)
    draw_intro.text((240, 720), "BTC204 - Par Loïc Morel - Chapitre chpt", font=fonts["regular"], fill=black)

    # PBN white logo (intro slide)
    logo_all_white = Image.open(os.path.join(img_path, "all white.png")).convert("RGBA")
    logo_all_white.thumbnail((185, 185))
    image_intro.paste(logo_all_white, (width - logo_all_white.size[0] - 50, 50), logo_all_white)

    add_footer(draw_intro, image_intro)

    # Save the intro slide
    output_file_intro = os.path.join(current_directory, "01.png")
    image_intro.save(output_file_intro)
    print(f"Intro slide successfully saved in: {output_file_intro}")

# Function to create main slide
def create_main_slide():
    image_main = Image.new("RGB", (width, height), white)
    draw_main = ImageDraw.Draw(image_main)
    
    # Specific elements for main slide
    draw_main.text((50, 50), "BTC204 - Chapitre chpt - nm", font=fonts["regular"], fill=black)
    draw_main.rectangle([50, 125, 75, 275], fill=orange_color)
    draw_main.text((120, 160), "titre", font=fonts["bold2"], fill=black)

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

    draw_main.text((width - right_rect_width + 120, instructor_text_y), "Instructeur", font=fonts["medium"], fill=black)

    instructor_photo = Image.open(os.path.join(img_path, "instructeur.png")).convert("RGBA")
    instructor_photo.thumbnail((400, 400))
    instructor_photo_width, instructor_photo_height = instructor_photo.size
    image_main.paste(instructor_photo, (width - right_rect_width + 73, photo_y), instructor_photo)

    waveform = Image.open(os.path.join(img_path, "waveform.png")).convert("RGBA")
    waveform = waveform.resize((right_rect_width - 5, 700))
    image_main.paste(waveform, (width - right_rect_width + 5, waveform_y), waveform)

    draw_dashed_rounded_rectangle(draw_main, [200, 350, width - right_rect_width - 200, height - 200], outline=orange_color, width=8)
    
    add_footer(draw_main, image_main)

    # Save the main slide
    output_file_main = os.path.join(current_directory, "02.png")
    image_main.save(output_file_main)
    print(f"Main slide successfully saved in: {output_file_main}")

# Run the functions to create slides
create_intro_slide()
create_main_slide()
