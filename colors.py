import webcolors

def color_name_to_rgb(color_name):
    try:
        rgb_tuple = webcolors.name_to_rgb(color_name)
        print(rgb_tuple.red)
        print(rgb_tuple.green)
        print(rgb_tuple.blue)
        return rgb_tuple
    except ValueError:
        print(f"Error: Color name '{color_name}' not recognized.")
        return None



color_name_to_rgb("orange")