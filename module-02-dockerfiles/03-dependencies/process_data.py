"""process_data.py — demonstrates using pip-installed packages inside Docker."""
import numpy as np
import pandas as pd
from datetime import datetime

print("📊 Data Processing Demo")
print("=" * 50)

# Create a sample DataFrame (simulating ML feature data)
np.random.seed(42)
n_samples = 100

df = pd.DataFrame({
    "sepal_length": np.random.normal(5.84, 0.83, n_samples),
    "sepal_width": np.random.normal(3.05, 0.43, n_samples),
    "petal_length": np.random.normal(3.76, 1.76, n_samples),
    "petal_width": np.random.normal(1.20, 0.76, n_samples),
    "species": np.random.choice(["setosa", "versicolor", "virginica"], n_samples),
})

print(f"\nGenerated {len(df)} samples")
print(f"\nDataFrame shape: {df.shape}")
print(f"\nColumn types:\n{df.dtypes}")
print(f"\nSummary statistics:\n{df.describe().round(3)}")
print(f"\nSpecies distribution:\n{df['species'].value_counts()}")

# Show that packages are installed and working
print(f"\nPackage versions:")
print(f"  numpy  : {np.__version__}")
print(f"  pandas : {pd.__version__}")
print(f"\nProcessed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
