import cairosvg, io, pygame
def svg_to_surface(filepath):

    png_io = io.BytesIO()
    svg_io = open(filepath, "r", encoding="utf-8")
    cairosvg.svg2png(bytestring=bytes(svg_io, "utf8"), write_to=png_io)
    png_io.seek(0)

    surf = pygame.image.load(png_io, "png")
    return surf