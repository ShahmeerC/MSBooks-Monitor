from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from groq import Groq
import os

from dotenv import load_dotenv
load_dotenv()

def OpenAI_summary(stats_payload):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an inventory monitoring analyst. "
                        "Summarize bookstore inventory and pricing changes "
                        "for Discord alerts. Mention important additions, "
                        "removals, significant price movements, and trends. "
                        "Keep the summary concise but informative."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
                            Monitoring data:

                            {stats_payload}

                        Generate a professional weekly monitoring summary.
                        """
                }
            ],
            temperature=0.4
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI summary generation failed:", e)
        return None

def Gemini_summary(stats_payload):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)
    try:
        prompt = f"""
You are an inventory monitoring analyst.
Summarize bookstore inventory and pricing changes for a Discord alert.
Mention:
- important additions
- removals
- significant price movements
- general trends
Keep concise but informative.
Monitoring data:
{stats_payload}
"""
        response = client.models.generate_content(model="gemini-1.5-flash",contents=prompt)
        return response.text
    
    except Exception as e:
        print("AI summary generation failed:", e)
        return None
    
def Groq_summary(stats_payload):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an automated monitoring assistant for a bookstore inventory system. "
                        "Generate ONLY a concise Discord alert summary. "
                        "Do NOT provide recommendations, management advice, next steps, or extra sections. "
                        "Only summarize detected inventory and pricing changes clearly and professionally."
                        "Mention important additions, removals, significant price movements (prices are in pkr), and trends."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
                            Monitoring data:

                            {stats_payload}

                            Generate a concise Discord monitoring alert.
                            """
                }
            ],
            temperature=0.4
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI summary generation failed:", e)
        return None

def monthly_Groq_summary(stats_payload):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are an educational publishing market analyst.
You are given:

1. Previous month catalog statistics
2. Current month catalog statistics
3. Detailed inventory changes between the two months

Your task is to generate a Monthly Intelligence Report.

The report should do BOTH:

CATALOG OVERVIEW:
- Describe what the current catalog contains.
- Discuss the overall composition of the catalog.
- Mention dominant book types.
- Mention notable subject distributions.
- Discuss pricing structure using the provided statistics.
- Mention notable expensive books if relevant.

MONTHLY CHANGES:
- Describe how the catalog changed compared to the previous month.
- Mention inventory growth or reduction.
- Highlight important added books.
    - Highlight important removed books.
    - Discuss significant price changes.
    - Mention notable pricing trends.

Assume the audience is a human monitoring the educational bookstore catalog and wants a quick understanding of both the current catalog and notable changes since last month.
Structure the report into no more or no less than these 3 categories:
1. Catalog Overview
2. Monthly Changes
3. Key Takeaways
    - Summarize the most important observations supported by the data.
    - Focus on inventory composition, catalog growth/shrinkage, and pricing changes.

IMPORTANT:
- Keep report under 300 words (1900 characters)
- Do not simply repeat raw statistics.
- Interpret the data and explain what it means.
- Keep the report concise but informative.
- Focus on meaningful insights rather than listing every metric.
- Write in a professional monitoring-report style.
- Do not provide recommendations.
- Do not suggest future actions.
- Do not speculate beyond the provided data.
- Do not invent reasons for changes.
- All prices are in Pakistani Rupees (PKR).
- Never use "$".
- Always write prices as "Rs." or "PKR".
- Always add the Book Grade (O Level/A Level/IGCSE) when talking about a book(i.e. O Level Physics and A Level Physics are different books, cant be regarded as just Physics)
- Always list all inventory changes in a consistent format.
"""
                },
                {
                    "role": "user",
                    "content": f"""Monitoring data:

{stats_payload}

Generate a Monthly Intelligence Report using the provided data.
"""
                }
            ],
            temperature=0.4
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI summary generation failed:", e)
        return None

def Groq_dashboard_summary(stats_payload):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=GROQ_API_KEY)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """You are an educational catalog intelligence analyst.

You are generating a dashboard report for a human reviewing an educational bookstore inventory system.

The user already has access to:
- Inventory metrics
- Distribution charts
- Book tables
- Change logs

Your task is NOT to repeat visible statistics.

Your task is to interpret the data and explain what stands out.

Structure the report into exactly:

1. Catalog Overview
2. Change Analysis
3. Key Takeaways

Catalog Overview:
- Describe the overall composition of the catalog.
- Mention dominant book categories.
- Discuss notable subject concentration.
- Comment on pricing structure at a high level.

Change Analysis:
- Explain meaningful additions, removals, and pricing changes.
- Focus on changes that materially affect the catalog.
- Discuss overall inventory growth, reduction, or stability.

Key Takeaways:
- Summarize the most important observations supported by the data.
- Focus on composition, trends, and notable movements.

IMPORTANT:
- Assume charts and tables are already visible.
- Interpret rather than repeat.
- Do not list every statistic.
- Do not provide recommendations.
- Do not suggest actions.
- Do not speculate beyond the data.
- Do not infer motivations, causes, demand shifts, business decisions, or customer behavior.
- Keep under 300 words.
- All prices are in Pakistani Rupees (PKR).
- Never use "$".
- Always write prices as "Rs." or "PKR".
- Always add the Book Grade (O Level/A Level/IGCSE) when talking about a book(i.e. O Level Physics and A Level Physics are different books, cant be regarded as just Physics)
"""
                },
                {
                    "role": "user",
                    "content": f"""Monitoring data:

{stats_payload}

Generate a Monthly Intelligence Report using the provided data.
"""
                }
            ],
            temperature=0.4
        )
        return response.choices[0].message.content

    except Exception as e:
        print("AI summary generation failed:", e)
        return None