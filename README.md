# Chikara's Econometric Data - Panel Data Analysis

Production function analysis using panel data econometrics in Python.

## Overview

This project analyzes production functions across multiple cities over time (annual data) using three econometric approaches:
- **Pooled OLS** - Treats all observations equally, ignoring panel structure
- **Fixed Effects (FE)** - Controls for city-specific unobserved heterogeneity
- **Random Effects (RE)** - Assumes city effects are uncorrelated with regressors
- **Hausman Test** - Tests whether FE or RE is more appropriate

## Data Structure

Your panel data should have the following structure:

| City | Year | Y | local inv | inter inv | laborforce | edu |
|------|------|---------------|---|---|---|-----|
| City1 | 2015 | 10.5 | 8.2 | 7.5 | 6.3 | 3.8 |
| City1 | 2016 | 10.6 | 8.3 | 7.6 | 6.4 | 3.9 |
| ... | ... | ... | ... | ... | ... | ... |

**Variables:**
- `City`: City identifier (panel/entity)
- `Year`: Time period (annual)
- `y`: Total Value of Production (dependent variable, log form)
- `local inv`: local investment (log form)
- `inter inv`: international investment (log form)
- `laborforces`: Wages (log form)
- `edu`: Education (log form)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chikaradini/datapanelchikara.git
cd datapanelchikara

pip install -r requirements.txt

from panel_data_analysis import main

# Run analysis
results = main(
    excel_file="your_data.xlsx",
    sheet_name=0,
    city_col='City',
    year_col='Year',
    dependent_var='y',
    independent_vars=['local inv', 'inter inv', 'laborforce', 'edu']
)
python panel_data_analysis.py

if __name__ == "__main__":
    excel_file = "Production in East Java"  # Change to your actual file path

If p-value < 0.05 (Significant):
  → Use FIXED EFFECTS model
  → City-specific effects are correlated with regressors
  → Within-variation is important

If p-value >= 0.05 (Not significant):
  → Use RANDOM EFFECTS model
  → City-specific effects are uncorrelated with regressors
  → Between-variation is important

local inv     0.45   (Elasticity of local investment)
inter inv     0.35   (Elasticity of international investment)
laborforce     0.15   (Elasticity of laborforce)
edu   0.08   (Elasticity of Education)

datapanelchikara/
├── panel_data_analysis.py    # Main analysis script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── your_data.xlsx           # Your panel data (add your file here)
