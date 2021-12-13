def rating_to_difficulty(rating):
    if rating <= 1100:
        return 'B'
    elif rating <= 1500:
        return 'E'
    elif rating <= 1800:
        return 'M'
    elif rating <= 2100:
        return 'H'
    elif rating <= 2600:
        return 'S'
    else:
        return 'C'
