from PIL import ImageDraw, ImageFont


def add_text_to_image_yigitlar(img, name):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("timesbd.ttf", 85)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = img.size
    x_position = (image_width - text_width) // 2
    y_position = 980
    text_position = (x_position, y_position)
    text_color = "white"

    draw.text(text_position, name, font=font, fill=text_color)
    return img
