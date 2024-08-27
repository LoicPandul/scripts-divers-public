from PIL import Image, ImageDraw, ImageFont
import os

# Slide dimensions
width, height = 2730, 1536

# Colors
background_color = (255, 255, 255)
orange_color = (255, 92, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# White background
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Paths to fonts and images
current_directory = os.path.dirname(__file__)
fonts_path = os.path.join(current_directory, '../fonts')
img_path = os.path.join(current_directory, '../img')

# Load fonts
try:
    font_rubik_bold = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 72)
    font_rubik_regular = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 42)
    font_rubik_medium = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 55)
    font_jetbrains_mono = ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24)
    font_rubik_italic = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20)
except OSError as e:
    print(f"Error loading fonts: {e}")
    exit(1)

# BTC204 text
draw.text((50, 50), "BTC204 - Chapitre chpt - nm", font=font_rubik_regular, fill=black)

# Orange line + title
draw.rectangle([50, 125, 75, 275], fill=orange_color)
draw.text((120, 160), "titre", font=font_rubik_bold, fill=black)

# Orange rectangle on the right
right_rect_width = width // 5
draw.rectangle([width - right_rect_width, 0, width, height], fill=orange_color)

# Instructor
draw.text((width - right_rect_width + 120, 220), "Instructeur", font=font_rubik_medium, fill=black)

# Instructor photo
instructor_photo = Image.open(os.path.join(img_path, "instructeur.png")).convert("RGBA")
instructor_photo.thumbnail((400, 400))
image.paste(instructor_photo, (width - right_rect_width + 73, 350), instructor_photo)

# Waveform
waveform = Image.open(os.path.join(img_path, "waveform.png")).convert("RGBA")
waveform = waveform.resize((right_rect_width - 5, 700))
image.paste(waveform, (width - right_rect_width + 5, 700), waveform)

# PBN black logo
logo_planb = Image.open(os.path.join(img_path, "all black.png")).convert("RGBA")
logo_planb.thumbnail((1000, 1000))
image.paste(logo_planb, (width - right_rect_width + 320, height - 130 - 60), logo_planb)

# Line thickness
line_width = 8

# Dashed rectangle with rounded corners
def draw_dashed_rounded_rectangle(draw, xy, outline, width=line_width):
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

# Draw the frame
draw_dashed_rounded_rectangle(draw, [200, 350, width - right_rect_width - 200, height - 200], outline=orange_color, width=line_width)

# Black footer bar
draw.rectangle([0, 1480, 2730, 1536], fill=black)

# CC BY-SA logo
logo_cc_by_sa = Image.open(os.path.join(img_path, "by-sa.png")).convert("RGBA")
logo_cc_by_sa = logo_cc_by_sa.resize((120, 42))
image.paste(logo_cc_by_sa, (0, height - logo_cc_by_sa.height - 44), logo_cc_by_sa)

# OpenAI and Eleven Labs logos
logo_openai = Image.open(os.path.join(img_path, "openai.png")).convert("RGBA")
logo_eleven_labs = Image.open(os.path.join(img_path, "Eleven_Labs.png")).convert("RGBA")
logo_openai = logo_openai.resize((40, 40))
logo_eleven_labs = logo_eleven_labs.resize((40, 40))

band_height = 56
offset_y = height - band_height + (band_height - logo_openai.height) // 2

offset_x = width - logo_openai.width - logo_eleven_labs.width - 25

image.paste(logo_openai, (offset_x, offset_y), logo_openai)
image.paste(logo_eleven_labs, (offset_x + logo_openai.width + 10, offset_y), logo_eleven_labs)

# IA Translated text
text_ia_translated = "IA Translated"
bbox = font_rubik_italic.getbbox(text_ia_translated)
text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
text_x = offset_x - text_width - 20
text_y = height - band_height + (band_height - text_height) // 2
draw.text((text_x, text_y), text_ia_translated, font=font_rubik_italic, fill=white)

# PGP Key
draw.text((20, 1488), "BTC204 - FR - V.001 - 2024-08 - Plan₿ Network’s PGP: 5720 CD57 7E78 94C9 8DBD 580E 8F12 D0C6 3B1A 606E", font=font_jetbrains_mono, fill=white)

# Save the image
output_file = os.path.join(current_directory, "02.png")
try:
    image.save(output_file)
    print(f"Slide saved in: {output_file}")
except Exception as e:
    print(f"Error saving the slide: {e}")
