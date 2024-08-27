from PIL import Image, ImageDraw, ImageFont
import os

# Slide dimensions
width, height = 2730, 1536

# Colors
background_color = (255, 92, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Orange background
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Paths to fonts and images
current_directory = os.path.dirname(__file__)
fonts_path = os.path.join(current_directory, 'fonts')
img_path = os.path.join(current_directory, 'img')

# Load fonts
try:
    font_rubik_bold = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Bold.ttf"), 96)
    font_rubik_regular = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Medium.ttf"), 48)
    font_jetbrains_mono = ImageFont.truetype(os.path.join(fonts_path, "JetBrainsMono-Italic.ttf"), 24)
    font_rubik_italic = ImageFont.truetype(os.path.join(fonts_path, "Rubik-Italic.ttf"), 20)
except OSError as e:
    print(f"Error loading fonts: {e}")
    exit(1)

# White bar on the left
draw.rectangle([200, 600, 214, 800], fill=white)

# Name
draw.text((240, 600), "name", font=font_rubik_bold, fill=white)

# Subtitle
draw.text((240, 720), "BTC204 - Par Loïc Morel - Chapitre chpt", font=font_rubik_regular, fill=black)

# PBN white logo
logo_all_white = Image.open(os.path.join(img_path, "all white.png")).convert("RGBA")
logo_all_white.thumbnail((185, 185))
image.paste(logo_all_white, (width - logo_all_white.width - 50, 50), logo_all_white)

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
output_file = os.path.join(current_directory, "01.png")
try:
    image.save(output_file)
    print(f"Image successfully saved in: {output_file}")
except Exception as e:
    print(f"Error saving the image: {e}")
