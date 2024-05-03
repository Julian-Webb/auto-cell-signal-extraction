import colorsys


def generate_distinct_colors(n):
    """Generate n evenly spaces hues in the color spectrum"""
    hues = [i / n for i in range(n)]

    # Convert hues to RGB
    colors = []
    for hue in hues:
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.8)  # You can adjust saturation and value as needed
        colors.append((r, g, b))

    return colors
