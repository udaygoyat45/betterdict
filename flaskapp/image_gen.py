def generate_url():
    import random
    url_list = ['https://images.pexels.com/photos/1054222/pexels-photo-1054222.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
                "https://images.pexels.com/photos/1831234/pexels-photo-1831234.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
                "https://images.pexels.com/photos/583848/pexels-photo-583848.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                "https://images.pexels.com/photos/1054218/pexels-photo-1054218.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                "https://images.pexels.com/photos/949587/pexels-photo-949587.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                "https://images.pexels.com/photos/1323550/pexels-photo-1323550.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"]
    return url_list[random.randint(1, len(url_list)-1)]