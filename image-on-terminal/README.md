## Display Image on terminal directly

```sh
pip install rich
```

```python
def show(image, width=80):
    w, h = image.size
    aspect = h / (2 * w)
    height = int(width * aspect)
    image = image.resize((width, height))
    
    import rich.text, rich.console
    text = rich.text.Text()
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            text.append("█", style=f"rgb({r},{g},{b})")
        text.append("\n")

    return rich.console.Console(width=width).print(text)

image_path = 'your_image.png'
from PIL import Image
image = Image.open(image_path)
show(image, 160)
```