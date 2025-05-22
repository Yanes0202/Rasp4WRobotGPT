def compress(action):
    match action:
        case "front":
            return "f"
        case "right":
            return "r"
        case "far_right":
            return "fr"
        case "left":
            return "l"
        case "far_left":
            return "fl"
        case "back":
            return "b"
        case _:
            print("Nieznana komenda:", action)
            return action
