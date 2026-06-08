from scraper import run_mini
from weekly_stats import book_changes, pricechanges, avg_price_changes
from AI_summaries import OpenAI_summary, Gemini_summary, Groq_summary

import pandas as pd
import requests
import shutil
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ---------------- SEND ALERT ----------------

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
def send_alert(message):
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Alert sent successfully.")
    else:
        print("Failed to send alert.")
        print(response.status_code)
        print(response.text)

# ---------------- MAIN PIPELINE ----------------

print("Running lightweight monitor scraper...\n")
run_mini()
print("\nLoading monitor datasets...")
old_df = pd.read_csv("data/books_monitor_baseline.csv")
new_df = pd.read_csv("data/books_monitor.csv")

# ---------------- CHANGE DETECTION ----------------

added_books, removed_books = book_changes(old_df, new_df)
# #test
# added_books.append({
#     "title": "TEST AI MONITOR BOOK",
#     "url": "https://test-url.com"
# })
price_changes = pricechanges(old_df, new_df)
price_stats = avg_price_changes(price_changes)

# ---------------- AI PAYLOAD ----------------

stats_payload = {
    "new_books_count": len(added_books),
    "removed_books_count": len(removed_books),
    "price_changes_count": len(price_changes),

    "added_books": added_books,
    "removed_books": removed_books,
    "price_changes": price_changes,

    "pricing_summary": price_stats
}

# ---------------- RAW FALLBACK MESSAGE ----------------

fallback_sections = []

if added_books:
    added_text = []
    for book in added_books:
        added_text.append(f"{book['title']}\n{book['url']}")
    fallback_sections.append(f"{len(added_books)} new books detected:\n" +"\n\n".join(added_text))

if removed_books:
    removed_text = []
    for book in removed_books:
        removed_text.append(f"{book['title']}\n{book['url']}")
    fallback_sections.append(f"{len(removed_books)} books removed:\n" +"\n\n".join(removed_text))

if price_changes:
    price_text = []
    for change in price_changes:
        price_text.append(
            f"{change['title']}: "
            f"Rs.{change['old_price']} → Rs.{change['new_price']} "
            f"({change['percent_change']}%)\n"
            f"{change['url']}"
        )
    fallback_sections.append("Price changes detected:\n" +"\n\n".join(price_text))

fallback_message = ("\n\n".join(fallback_sections) if fallback_sections else "No updates detected this week.")

# ---------------- AI ALERT ----------------

ai_summary = Groq_summary(stats_payload)
if ai_summary:
    send_alert(ai_summary)
else:
    send_alert(fallback_message)

# ---------------- WEEKLY LOGGING ----------------

today = datetime.now().strftime("%Y-%m-%d")
log_entry = pd.DataFrame([{
    "Date": today,
    "New Books": len(added_books),
    "Removed Books": len(removed_books),
    "Price Changes": len(price_changes),
    "Change Details": fallback_message
}])
if os.path.exists("data/weekly_monitor_log.csv"):
    log_entry.to_csv("data/weekly_monitor_log.csv",mode="a",header=False,index=False)
else:
    log_entry.to_csv("data/weekly_monitor_log.csv",index=False)
print("Weekly log updated.")

# ---------------- BASELINE UPDATE ----------------

shutil.copy("data/books_monitor.csv", "data/books_monitor_baseline.csv")
print("Monitor baseline updated.")