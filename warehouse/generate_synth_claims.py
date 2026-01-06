import pandas as pd
import numpy as np
from pathlib import Path

# Where parquet files will be saved
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "sample_data"
DATA_DIR.mkdir(exist_ok=True)

np.random.seed(42)

# -------------------------
# Dimension: Date
# -------------------------
dates = pd.date_range(start="2024-01-01", end="2024-06-30", freq="D")
dim_date = pd.DataFrame({
    "date_key": dates.strftime("%Y%m%d").astype(int),
    "date": dates,
    "year": dates.year,
    "month": dates.month,
    "week": dates.isocalendar().week
})
dim_date.to_parquet(DATA_DIR / "dim_date.parquet", index=False)

# -------------------------
# Dimension: Member
# -------------------------
n_members = 1000
dim_member = pd.DataFrame({
    "member_id": range(1, n_members + 1),
    "age_band": np.random.choice(["18-25", "26-40", "41-60", "60+"], n_members),
    "gender": np.random.choice(["M", "F"], n_members),
    "plan_type": np.random.choice(["HMO", "PPO", "EPO"], n_members),
    "state": np.random.choice(["CA", "TX", "NJ", "NY"], n_members)
})
dim_member.to_parquet(DATA_DIR / "dim_member.parquet", index=False)

# -------------------------
# Dimension: Provider
# -------------------------
n_providers = 200
dim_provider = pd.DataFrame({
    "provider_id": range(1, n_providers + 1),
    "specialty": np.random.choice(
        ["Cardiology", "Orthopedics", "Primary Care", "Neurology"], n_providers
    ),
    "facility_type": np.random.choice(["Hospital", "Clinic"], n_providers),
    "state": np.random.choice(["CA", "TX", "NJ", "NY"], n_providers)
})
dim_provider.to_parquet(DATA_DIR / "dim_provider.parquet", index=False)

# -------------------------
# Fact: Claims
# -------------------------
n_claims = 50_000

fact_claims = pd.DataFrame({
    "claim_id": range(1, n_claims + 1),
    "member_id": np.random.choice(dim_member["member_id"], n_claims),
    "provider_id": np.random.choice(dim_provider["provider_id"], n_claims),
    "service_date": np.random.choice(dates, n_claims),
    "paid_amount": np.round(np.random.gamma(2.0, 150.0, n_claims), 2),
    "denial_flag": np.random.choice([0, 1], n_claims, p=[0.9, 0.1])
})

# Introduce a denial spike (for demo impact)
spike_mask = fact_claims["service_date"] > "2024-05-15"
fact_claims.loc[spike_mask, "denial_flag"] = np.random.choice(
    [0, 1], spike_mask.sum(), p=[0.7, 0.3]
)

fact_claims.to_parquet(DATA_DIR / "fact_claims.parquet", index=False)

print("✅ Synthetic data generated successfully!")
print(f"📂 Files written to: {DATA_DIR}")
