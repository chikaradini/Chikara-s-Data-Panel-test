# 📊 Chikara's Econometric Data - Panel Data Analysis

Production function analysis using panel data econometrics in Python.

---

## 📖 Overview

This project analyzes **production functions** across multiple cities over time (annual data) using three econometric approaches:

- **Pooled OLS** - Baseline model treating all observations equally
- **Fixed Effects (FE)** - Controls for city-specific unobserved heterogeneity
- **Random Effects (RE)** - Assumes city effects are uncorrelated with regressors
- **Hausman Test** - Statistical test to determine the best model (FE vs RE)

---

## 📋 Data Structure

Your panel data should be organized as follows:

| City | Year | y | local inv | inter inv | laborforces | edu |
|------|------|---|-----------|-----------|-------------|-----|
| City1 | 2015 | 10.5 | 8.2 | 7.5 | 6.3 | 3.8 |
| City1 | 2016 | 10.6 | 8.3 | 7.6 | 6.4 | 3.9 |
| City2 | 2015 | 10.3 | 8.0 | 7.3 | 6.1 | 3.6 |
| City2 | 2016 | 10.4 | 8.1 | 7.4 | 6.2 | 3.7 |

**Variable Definitions:**

| Variable | Description | Form |
|----------|-------------|------|
| `City` | City identifier (panel entity) | Categorical |
| `Year` | Time period (annual data) | Numeric |
| `y` | Total Value of Production (dependent variable) | Natural log |
| `local inv` | Local investment | Natural log |
| `inter inv` | International investment | Natural log |
| `laborforces` | Labor force/Wages | Natural log |
| `edu` | Education level | Natural log |

---

