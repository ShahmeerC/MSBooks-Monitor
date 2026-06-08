from scraper import run_scraper
from monthly_stats import generate_stats_payload,monthly_price_changes,monthly_book_changes,avg_price_changes
from AI_summaries import monthly_Groq_summary,Groq_dashboard_summary

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

# ---------------- BASELINE UPDATE ----------------

shutil.copy("data/Books_cleaned.csv", "data/Books_cleaned_baseline.csv")
print("Monitor baseline updated.")

# ---------------- MAIN PIPELINE ----------------

print("Running mega monitor scraper...\n")
run_scraper()
print("\nLoading monitor datasets...")
old_df = pd.read_csv("data/Books_cleaned_baseline.csv")
new_df = pd.read_csv("data/Books_cleaned.csv")

# ---------------- CHANGE DETECTION ----------------

previous_stats = generate_stats_payload(old_df)
current_stats = generate_stats_payload(new_df)

added_books, removed_books = monthly_book_changes(old_df, new_df)
price_changes = monthly_price_changes(old_df, new_df)
price_change_stats = avg_price_changes(price_changes)

# ---------------- AI PAYLOAD ----------------

stats_payload = {
    "previous_month_stats": previous_stats,
    "current_month_stats": current_stats,

    "new_books_count": len(added_books),
    "removed_books_count": len(removed_books),
    "price_changes_count": len(price_changes),
    "added_books": added_books,
    "removed_books": removed_books,
    "price_changes": price_changes,
    "pricing_changes_summary": price_change_stats
}

# ---------------- RAW FALLBACK MESSAGE ----------------

fallback_sections = []

if added_books:
    added_text = []
    for book in added_books:
        added_text.append(f"{book['Title']} | Code: {book['Subject Code']} | Type: {book['Type']} | Rs.{book['Price']}")
    fallback_sections.append(f"{len(added_books)} new books detected:\n" +"\n\n".join(added_text))

if removed_books:
    removed_text = []
    for book in removed_books:
        removed_text.append(f"{book['Title']} | Code: {book['Subject Code']} | Type: {book['Type']} | Rs.{book['Price']}")
    fallback_sections.append(f"{len(removed_books)} books removed:\n" +"\n\n".join(removed_text))

if price_changes:
    price_text = []
    for book in price_changes:
        price_text.append(
            f"{book['Title']} | Code: {book['Subject Code']} | Type: {book['Type']}\n"
            f"Price change: Rs.{book['Old Price']} → Rs.{book['New Price']}\n"
            f"% change: ({book['Percent Change']}%)"
        )
    fallback_sections.append(f"{len(price_changes)} price changes detected:\n" +"\n\n".join(price_text))

fallback_message = ("\n\n".join(fallback_sections) if fallback_sections else "No updates detected this month.")

# ---------------- AI ALERT ----------------

ai_alert_summary = monthly_Groq_summary(stats_payload)
if ai_alert_summary:
    send_alert(ai_alert_summary)
else:
    send_alert(fallback_message)

# ---------------- AI DASHBOARD SUMMARY ----------------

ai_dashboard_summary = Groq_dashboard_summary(stats_payload)

# ---------------- MONTHLY LOGGING ----------------

today = datetime.now().strftime("%Y-%m-%d")
log_entry = pd.DataFrame([{
    "Date": today,
    "Total Books": len(new_df),
    "Unique Subjects": new_df["Subject code"].nunique(),
    "Unique Authors": new_df["Author"].nunique(),
    "New Books": len(added_books),
    "Removed Books": len(removed_books),
    "Price Changes": len(price_changes),
    "Change Details": fallback_message,
    "AI Alert Summary": ai_alert_summary,
    "AI Dashboard Summary": ai_dashboard_summary
}])
if os.path.exists("data/monthly_monitor_log.csv"):
    log_entry.to_csv("data/monthly_monitor_log.csv",mode="a",header=False,index=False)
else:
    log_entry.to_csv("data/monthly_monitor_log.csv",index=False)
print("Monthly log updated.")

new_df.to_csv(f"data/history/{today}_catalog.csv",index=False)





