from PIL import Image, ImageDraw, ImageFont
import os
import textwrap


def generate_persona_image(name, behavior, motivations, frustrations, output_filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "app", "templates", "persona_template.png")
    output_dir = "./backend/app/static/output/"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    font_path = "C:/Windows/Fonts/arial.ttf"
    font_body = ImageFont.truetype(font_path, size=18)

    # Coordinates aligned to your template
    draw.text((760, 125), behavior, font=font_body, fill="black")
    draw.text((760, 315), motivations, font=font_body, fill="black")
    draw.text((760, 505), frustrations, font=font_body, fill="black")

    image.save(output_path)
    return output_path

