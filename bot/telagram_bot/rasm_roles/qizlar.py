from PIL import ImageDraw, ImageFont

def add_text_to_image_qizlar(img, name):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("timesbd.ttf", 85)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = font.getbbox(name)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width, image_height = img.size
    x_position = (image_width - text_width) / 2
    y_position = 980
    draw.text(xy=(x_position, y_position), text=name, font=font, fill="black")
    return img
