def web2kmlcolor(color, opacity='3c'):
    """This function convert a web exadecimal color in a kml color
       color = rrggbb or rrggbbaa
    """

    if  not color:
        return ''

    if color.startswith('#'):
        color = color[1:]

    r = color[0:2]
    g = color[2:4]
    b = color[4:6]
    a = opacity
    if len(color) == 8:
        # alpha layer could be bassed by color varible
        a = color[6:8]

    return a + b + g + r
