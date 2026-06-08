def generate_stats_payload(df):
    return {
        "inventory_overview": {
            "total_books": len(df),
            "unique_subjects": df["Subject code"].nunique(),
            "unique_authors": df["Author"].nunique()
        },
        "price_stats": df.groupby("Type")["Price"].describe().round(2).to_dict("index"),
        "distributions": {
            "grade_distribution": df["Grade"].value_counts().to_dict(),
            "type_distribution": df["Type"].value_counts().to_dict(),
            "subject_distribution(top 10)": df[df["Subject code"] != "Unknown"]["Subject code"].value_counts().head(10).to_dict(),
            "subject_distribution(bottom 10)": df[df["Subject code"] != "Unknown"]["Subject code"].value_counts().tail(10).to_dict()
        },
        "top_expensive_books": df.nlargest(10, "Price")[["Title", "Price"]].to_dict("records")
    }


def monthly_price_changes(old_df, new_df):
    price_changes = []
    old_prices = dict(zip(old_df["Title"], old_df["Price"]))
    new_prices = dict(zip(new_df["Title"], new_df["Price"]))
    title_to_info = (new_df.set_index("Title")[["Subject code", "Type"]].to_dict("index"))
    for title in old_prices:
        if title in new_prices:
            old_price = old_prices[title]
            new_price = new_prices[title]
            info = title_to_info[title]
            if old_price != new_price:
                difference = new_price - old_price
                percent_change = (difference / old_price) * 100
                price_changes.append({
                    "Title": title,
                    "Subject Code": info["Subject code"],
                    "Type": info["Type"],
                    "Old Price": old_price,
                    "New Price": new_price,
                    "Difference": difference,
                    "Percent Change": round(percent_change, 2)
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


def monthly_book_changes(old_df, new_df):
    old_titles = set(old_df["Title"])
    new_titles = set(new_df["Title"])
    added_titles = new_titles - old_titles
    removed_titles = old_titles - new_titles
    new_title_to_info = (new_df.set_index("Title")[["Subject code", "Type", "Price"]].to_dict("index"))
    old_title_to_info = (old_df.set_index("Title")[["Subject code", "Type", "Price"]].to_dict("index"))
    added_books = []
    removed_books = []
    for title in added_titles:
        info = new_title_to_info[title]
        added_books.append({
            "Title": title,
            "Subject Code": info["Subject code"],
            "Type": info["Type"],
            "Price": info["Price"]
        })
    for title in removed_titles:
        info = old_title_to_info[title]
        removed_books.append({
            "Title": title,
            "Subject Code": info["Subject code"],
            "Type": info["Type"],
            "Price": info["Price"]
        })
    return added_books, removed_books
