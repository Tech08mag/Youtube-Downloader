def get_ending(link: str):
    replacement = "https://www.youtube.com/watch?v="
    link = link.replace(replacement, "")
    return link