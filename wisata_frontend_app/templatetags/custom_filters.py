from django import template
register = template.Library()

@register.filter
def star_range(rating):
    """
    Mengembalikan list: [full, full, full, half, empty]
    """
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0
    stars = []
    full_stars = int(rating)
    half_star = (rating - full_stars) >= 0.5
    for _ in range(full_stars):
        stars.append('full')
    if half_star and len(stars) < 5:
        stars.append('half')
    while len(stars) < 5:
        stars.append('empty')
    return stars 