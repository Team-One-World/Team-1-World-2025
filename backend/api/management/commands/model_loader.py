from django.core.management.base import BaseCommand
import os
import requests

# Path where the model will live for API usage
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "api")
MODEL_FILE = os.path.join(BASE_DIR, "model.keras")
MODEL_URL = "https://huggingface.co/<username>/<repo-name>/resolve/main/model.keras"

class Command(BaseCommand):
    help = "Download Keras model from Hugging Face"

    def handle(self, *args, **options):
        if not os.path.exists(MODEL_FILE):
            self.stdout.write("Downloading model.keras from Hugging Face...")
            r = requests.get(MODEL_URL, stream=True)
            os.makedirs(BASE_DIR, exist_ok=True)
            with open(MODEL_FILE, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.stdout.write(self.style.SUCCESS(f"Downloaded model to {MODEL_FILE}"))
        else:
            self.stdout.write("model.keras already exists, skipping download.")
