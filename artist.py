class Artist:
    """store artist data"""
    def __init__(self, name, rank, url, plays=0, image_url=""):
        self.name = name
        self.rank = rank
        self.url = url
        self.image_url = image_url
        self.play_count = plays

