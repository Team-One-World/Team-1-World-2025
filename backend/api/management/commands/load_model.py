from django.core.management.base import BaseCommand
import os
import requests

# Base directory for storing models
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Files and their corresponding URLs
FILES_TO_DOWNLOAD = {
    "model.keras": "https://huggingface.co/nimitjalan/team1world/resolve/main/model.keras",
    "scaler.joblib": "https://huggingface.co/nimitjalan/team1world/resolve/main/scaler.joblib",
    "label_encoder.joblib": "https://huggingface.co/nimitjalan/team1world/resolve/main/label_encoder.joblib",
}

class Command(BaseCommand):
    help = "Download model and related files from Hugging Face"

    def handle(self, *args, **options):
        os.makedirs(BASE_DIR, exist_ok=True)
        
        for filename, url in FILES_TO_DOWNLOAD.items():
            file_path = os.path.join(BASE_DIR, filename)
            
            if not os.path.exists(file_path):
                self.stdout.write(f"Downloading {filename} from Hugging Face...")
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Will stop if download fails
                
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                self.stdout.write(self.style.SUCCESS(f"Downloaded {filename} to {file_path}"))
            else:
                self.stdout.write(f"{filename} already exists, skipping download.")