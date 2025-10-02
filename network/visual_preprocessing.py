import pandas as pd

# Load raw CSVs (skip comment lines that start with #)
planets_raw = pd.read_csv("data/visual/Planetary Systems.csv", comment='#', low_memory=False)
stars_raw   = pd.read_csv("data/visual/Stellar Hosts.csv", comment='#', low_memory=False)

# --- Process Stars ---
stars = stars_raw.rename(columns={
    "hostname": "name",
    "ra": "ra",
    "dec": "dec",
    "st_teff": "star_temp",
    "st_rad": "star_radius",
    "sy_dist": "sy_dist"
})

stars = stars[["name", "ra", "dec", "star_temp", "star_radius", "sy_dist"]].drop_duplicates()
stars.reset_index(drop=True, inplace=True)
stars.index.name = "id"

stars.to_csv("stars.csv")
print(f"✅ Saved {len(stars)} stars → stars.csv")

# --- Process Planets ---
planets = planets_raw.rename(columns={
    "pl_name": "name",
    "hostname": "star_name",
    "pl_orbper": "orbital_period",
    "pl_rade": "radius",
    "ra": "ra",
    "dec": "dec",
    "pl_trandur": "duration",
    "pl_trandep": "transit_depth"
})

planets = planets[[
    "name", "star_name", "orbital_period", "radius",
    "ra", "dec", "duration", "transit_depth"
]].dropna(subset=["name", "star_name"])

# Average numeric columns for each planet
numeric_cols = ["orbital_period", "radius", "ra", "dec", "duration", "transit_depth"]
planets = planets.groupby("name", as_index=False).agg({
    "star_name": "first",  # star name stays the same
    **{col: "mean" for col in numeric_cols}  # average numeric columns
})

# Add placeholder for model_snr
planets["model_snr"] = None

planets.reset_index(drop=True, inplace=True)
planets.index.name = "id"

planets.to_csv("planets.csv")
print(f"✅ Saved {len(planets)} planets → planets.csv")
