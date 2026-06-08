def pricechanges(old_df, new_df):
    price_changes = []
    old_prices = dict(zip(old_df["Title"], old_df["Price"]))
    new_prices = dict(zip(new_df["Title"], new_df["Price"]))
    title_to_url = dict(zip(new_df["Title"], new_df["URL"]))
    for title in old_prices:
        if title in new_prices:
            old_price = old_prices[title]
            new_price = new_prices[title]
            if old_price != new_price:
                difference = new_price - old_price
                percent_change = (difference / old_price) * 100
                price_changes.append({
                    "title": title,
                    "url": title_to_url[title],
                    "old_price": old_price,
                    "new_price": new_price,
                    "difference": difference,
                    "percent_change": round(percent_change, 2)
                })
    return price_changes

def avg_price_changes(price_changes):
    increases = [p for p in price_changes if p["difference"] > 0]
    decreases = [p for p in price_changes if p["difference"] < 0]
    stats = {
        "books_with_increases": len(increases),
        "books_with_decreases": len(decreases),
        "avg_increase": None,
        "avg_decrease": None,
        "largest_increase": None,
        "largest_decrease": None,
        "net_price_movement": 0
    }
    if increases:
        stats["avg_increase"] = round(sum(p["percent_change"] for p in increases) / len(increases),2)
        stats["largest_increase"] = max(increases,key=lambda x: x["percent_change"])
    if decreases:
        stats["avg_decrease"] = round(sum(abs(p["percent_change"]) for p in decreases) / len(decreases),2)
        stats["largest_decrease"] = min(decreases,key=lambda x: x["percent_change"])
    if price_changes:
        stats["net_price_movement"] = sum(p["difference"] for p in price_changes)
    return stats


def book_changes(old_df, new_df):
    old_titles = set(old_df["Title"])
    new_titles = set(new_df["Title"])
    added_titles = new_titles - old_titles
    removed_titles = old_titles - new_titles
    title_to_url = dict(zip(new_df["Title"], new_df["URL"]))
    old_title_to_url = dict(zip(old_df["Title"], old_df["URL"]))
    added_books = []
    removed_books = []
    for title in added_titles:
        added_books.append({
            "title": title,
            "url": title_to_url[title]
        })
    for title in removed_titles:
        removed_books.append({
            "title": title,
            "url": old_title_to_url[title]
        })
    return added_books, removed_books





