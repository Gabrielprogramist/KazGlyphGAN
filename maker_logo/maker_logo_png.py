from PIL import Image

# Открыть изображение
image = Image.open('maker_logo\Қ.png').convert('RGBA')
pixels = image.load()

# Перебор всех пикселей
for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = pixels[x, y]
        # Если пиксель черный (или почти черный), делаем его белым
        if r < 50 and g < 50 and b < 50:
            pixels[x, y] = (255, 255, 255, 255)
        # Если пиксель белый (или почти белый), делаем его прозрачным
        elif r > 200 and g > 200 and b > 200:
            pixels[x, y] = (255, 255, 255, 0)

# Сохранить изображение
image.save('output_image.png', 'PNG')
