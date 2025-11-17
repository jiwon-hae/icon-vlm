import cairosvg

def svg_to_png(svg_path, png_path, size=256):
    try:
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(png_path),
            output_width=size,
            output_height=size
        )
        return True
    except Exception as e:
        print("Conversion failed:", svg_path, e)
        return False
