def chord (root_chord, taper_ratio, half_span, spanwise_location):
    return root_chord - root_chord * (1 - taper_ratio) * (spanwise_location/half_span)
