from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging
import subprocess
import openai

logger = logging.getLogger(__name__)

@shared_task
def scrape_travel_news():
    try:
        result = subprocess.run(
            ["scrapy", "crawl", "news"],
            cwd="travel_scraper", 
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Scrapy output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run Scrapy spider: {e.stderr}")
        raise

class OpenAIChatbot:

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY

    def get_response(self, user_input):
        """
        Generate a response from OpenAI's API using the provided input.
        """
        openai.api_key = self.api_key

        system_message = {
            "role": "system",
            "content": (
                "You are a helpful travel assistant. You specialize in recommending travel packages, "
                "answering questions about travel destinations, bookings, and related services. "
                "If the question is unrelated to travel, respond with: "
                "'I can only assist with travel-related queries. Please ask about packages, bookings, or destinations.'"
            ),
        }

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4", 
                messages=[
                    system_message,
                    {"role": "user", "content": user_input},
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
