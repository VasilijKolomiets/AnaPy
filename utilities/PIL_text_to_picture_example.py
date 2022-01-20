from PIL import Image, ImageDraw, ImageFont


def txt_to_image_EN(text_str: str, out_file: str='text.png', font_ttf: str = 'arial.ttf'):
    img = Image.new('RGB', (226*2, 34*2), (255, 255, 255))

    font = ImageFont.truetype(font_ttf, size=24, encoding='UTF-8')  # 'monocondensedc1.ttf'
    draw = ImageDraw.Draw(img)

    # draw.text((10, 10), str) -- ошибка
    # draw.text((10, 1), text_str, font=font, fill=(0, 0, 0))

    # draw multiline text
    draw.multiline_text((1, 1), text_str, font=font, fill=(0, 0, 0))

    img.show()
    img.save(out_file)


if __name__ == '__main___':
    txt_to_image_EN("1_Календарь настенный \n В упаковке 3333 изделия")
