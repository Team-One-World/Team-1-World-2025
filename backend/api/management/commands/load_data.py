import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Star, Planet
class Command(BaseCommand):
    help = "Load stars.csv and planets.csv into the database"

    def add_arguments(self, parser):
        parser.add_argument("--stars", type=str, default="stars.csv")
        parser.add_argument("--planets", type=str, default="planets.csv")

    def handle(self, *args, **options):
        stars_path = options["stars"]
        planets_path = options["planets"]

        self.stdout.write(f"📂 Loading stars from {stars_path}")
        stars_df = pd.read_csv(stars_path)

        # Build Star objects
        stars = [
            Star(
                name=row["name"],
                ra=row["ra"],
                dec=row["dec"],
                sy_dist=row["sy_dist"],
                star_temp=row["star_temp"],
                star_radius=row["star_radius"],
            )
            for _, row in stars_df.iterrows()
        ]

        Star.objects.all().delete()  # optional: clear old data
        Star.objects.bulk_create(stars, batch_size=1000, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"✅ Inserted {len(stars)} stars"))

        self.stdout.write(f"📂 Loading planets from {planets_path}")
        planets_df = pd.read_csv(planets_path)

        # Build Planet objects (requires star lookup by name)
        star_lookup = {s.name: s for s in Star.objects.all()}

        planets = []
        for _, row in planets_df.iterrows():
            star = star_lookup.get(row["star_name"])
            if not star:
                continue
            planets.append(
                Planet(
                    star=star,
                    name=row["name"],
                    orbital_period=row.get("orbital_period"),
                    radius=row.get("radius"),
                    ra=row.get("ra"),
                    dec=row.get("dec"),
                    duration=row.get("duration"),
                    transit_depth=row.get("transit_depth"),
                    model_snr=row.get("model_snr"),
                )
            )

        Planet.objects.all().delete()  # optional: clear old data
        Planet.objects.bulk_create(planets, batch_size=1000, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"✅ Inserted {len(planets)} planets"))
