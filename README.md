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
