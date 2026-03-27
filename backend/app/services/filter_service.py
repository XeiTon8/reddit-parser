def filter_posts(posts, keywords):

    result = []

    for post in posts:
        text = (post["title"] + " " + post["selftext"]).lower()

        if any(key in text for key in keywords):
            result.append({
                "title": post["title"],
                "has_image": post["has_image"]
            })

    return result
