def get_ending(link: str):
    replacement = "https://www.youtube.com/watch?v="
    link = link.replace(replacement, "")
    if '&' in link:
        link = link[:link.find('&')]
    return link