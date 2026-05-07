excel_file = "Production in East Java.xlsx"  # Change to your actual file
python panel_data_analysis.py

"""
Panel Data Analysis: Production Function
Cities × Years (Annual Data)
Author: Chikara
Description: Econometric analysis using Pooled OLS, Fixed Effects, and Random Effects models
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS, RandomEffects, PooledOLS
from linearmodels.panel import compare
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. LOAD DATA
# ============================================================================

def load_panel_data(excel_file, sheet_name=0):
    """
    Load panel data from Excel file
    
    Parameters:
    -----------
    excel_file : str
        Path to Excel file
    sheet_name : str or int
        Sheet name or index
        
    Returns:
    --------
    pd.DataFrame
        Panel data with proper index
    """
    # Read Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Display data info
    print("=" * 80)
    print("DATA OVERVIEW")
    print("=" * 80)
    print(f"\nData shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")
    
    return df


def prepare_panel_data(df, city_col='City', year_col='Year'):
    """
    Prepare data for panel analysis by setting multi-index
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw data
    city_col : str
        Column name for city identifier
    year_col : str
        Column name for time period
        
    Returns:
    --------
    pd.DataFrame
        Panel data with MultiIndex (city, year)
    """
    # Set multi-index (entity, time)
    df_panel = df.set_index([city_col, year_col])
    
    # Ensure all variables are numeric
    numeric_cols = df_panel.select_dtypes(include=[np.number]).columns
    df_panel = df_panel[numeric_cols]
    
    print(f"\nPanel data shape: {df_panel.shape}")
    print(f"Number of cities: {df_panel.index.get_level_values(0).nunique()}")
    print(f"Number of years: {df_panel.index.get_level_values(1).nunique()}")
    print(f"Variables: {list(df_panel.columns)}\n")
    
    return df_panel


# ============================================================================
# 2. PANEL DATA MODELS
# ============================================================================

def fit_pooled_ols(df_panel, dependent_var, independent_vars):
    """
    Fit Pooled OLS model (ignoring panel structure)
    
    Parameters:
    -----------
    df_panel : pd.DataFrame
        Panel data with MultiIndex
    dependent_var : str
        Name of dependent variable
    independent_vars : list
        List of independent variable names
        
    Returns:
    --------
    LinearModelResults
        Pooled OLS estimation results
    """
    y = df_panel[dependent_var]
    X = df_panel[independent_vars]
    
    model = PooledOLS(y, X)
    results = model.fit()
    
    return results


def fit_fixed_effects(df_panel, dependent_var, independent_vars):
    """
    Fit Fixed Effects model (Within estimator)
    
    Parameters:
    -----------
    df_panel : pd.DataFrame
        Panel data with MultiIndex
    dependent_var : str
        Name of dependent variable
    independent_vars : list
        List of independent variable names
        
    Returns:
    --------
    LinearModelResults
        Fixed Effects estimation results
    """
    y = df_panel[dependent_var]
    X = df_panel[independent_vars]
    
    # Fixed Effects (entity_effects=True removes entity-specific intercepts)
    model = PanelOLS(y, X, entity_effects=True)
    results = model.fit()
    
    return results


def fit_random_effects(df_panel, dependent_var, independent_vars):
    """
    Fit Random Effects model (GLS estimator)
    
    Parameters:
    -----------
    df_panel : pd.DataFrame
        Panel data with MultiIndex
    dependent_var : str
        Name of dependent variable
    independent_vars : list
        List of independent variable names
        
    Returns:
    --------
    LinearModelResults
        Random Effects estimation results
    """
    y = df_panel[dependent_var]
    X = df_panel[independent_vars]
    
    # Random Effects model
    model = RandomEffects(y, X)
    results = model.fit()
    
    return results


# ============================================================================
# 3. MODEL DIAGNOSTICS AND TESTS
# ============================================================================

def hausman_test(fe_results, re_results):
    """
    Hausman test: FE vs RE
    H0: Random Effects is appropriate
    H1: Fixed Effects is appropriate
    
    If p-value < 0.05: Reject H0, use Fixed Effects
    If p-value >= 0.05: Use Random Effects
    """
    # Get coefficients
    fe_coefs = fe_results.params
    re_coefs = re_results.params
    
    # Get covariance matrices
    fe_cov = fe_results.cov
    re_cov = re_results.cov
    
    # Common variables
    common_vars = fe_coefs.index.intersection(re_coefs.index)
    
    # Difference in coefficients
    coef_diff = fe_coefs[common_vars] - re_coefs[common_vars]
    
    # Variance of difference
    var_diff = fe_cov.loc[common_vars, common_vars] - re_cov.loc[common_vars, common_vars]
    
    # Hausman test statistic
    try:
        H = coef_diff.T @ np.linalg.inv(var_diff) @ coef_diff
        p_value = 1 - stats.chi2.cdf(H, df=len(common_vars))
    except:
        H = np.nan
        p_value = np.nan
    
    return H, p_value


def print_hausman_test(H, p_value):
    """Print Hausman test results with interpretation"""
    print("\n" + "=" * 80)
    print("HAUSMAN TEST: Fixed Effects vs Random Effects")
    print("=" * 80)
    print(f"H-statistic: {H:.4f}")
    print(f"P-value: {p_value:.4f}")
    print("\nInterpretation:")
    if p_value < 0.05:
        print("✓ P-value < 0.05: REJECT null hypothesis")
        print("  → Use FIXED EFFECTS model (entities are correlated with regressors)")
    else:
        print("✗ P-value >= 0.05: FAIL TO REJECT null hypothesis")
        print("  → Use RANDOM EFFECTS model (entities are uncorrelated with regressors)")
    print("=" * 80)


def print_model_comparison(pols_results, fe_results, re_results):
    """
    Print comparison of all three models
    """
    print("\n" + "=" * 80)
    print("MODEL COMPARISON: Pooled OLS vs Fixed Effects vs Random Effects")
    print("=" * 80)
    
    # Create comparison table
    comparison_dict = {
        'Pooled OLS': pols_results,
        'Fixed Effects': fe_results,
        'Random Effects': re_results
    }
    
    comparison = compare(comparison_dict)
    print(comparison)
    print("=" * 80)


# ============================================================================
# 4. RESULTS SUMMARY
# ============================================================================

def print_detailed_results(results, model_name):
    """Print detailed results for each model"""
    print("\n" + "=" * 80)
    print(f"{model_name.upper()}")
    print("=" * 80)
    print(results)
    print("=" * 80)


# ============================================================================
# 5. VISUALIZATION
# ============================================================================

def plot_coefficients(pols_results, fe_results, re_results, independent_vars):
    """
    Plot coefficient comparison across models
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Get coefficients
    x = np.arange(len(independent_vars))
    width = 0.25
    
    pols_coefs = pols_results.params[independent_vars].values
    fe_coefs = fe_results.params[independent_vars].values
    re_coefs = re_results.params[independent_vars].values
    
    ax.bar(x - width, pols_coefs, width, label='Pooled OLS', alpha=0.8)
    ax.bar(x, fe_coefs, width, label='Fixed Effects', alpha=0.8)
    ax.bar(x + width, re_coefs, width, label='Random Effects', alpha=0.8)
    
    ax.set_xlabel('Variables', fontsize=12, fontweight='bold')
    ax.set_ylabel('Coefficient Values', fontsize=12, fontweight='bold')
    ax.set_title('Production Function Coefficients: Model Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(independent_vars)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    print("\n✓ Coefficient comparison plot saved: model_comparison.png")
    plt.show()


# ============================================================================
# 6. MAIN EXECUTION
# ============================================================================

def main(excel_file, sheet_name=0, city_col='City', year_col='Year', 
         dependent_var='ln_Production', independent_vars=['k', 'l', 'w', 'edu']):
    """
    Main function to run complete panel data analysis
    
    Parameters:
    -----------
    excel_file : str
        Path to Excel file with panel data
    sheet_name : str or int
        Excel sheet name or index
    city_col : str
        Column name for city identifier
    year_col : str
        Column name for time period
    dependent_var : str
        Name of dependent variable (Total Value of Production)
    independent_vars : list
        List of independent variable names [k, l, w, edu]
    """
    
    print("\n" + "=" * 80)
    print("PANEL DATA ANALYSIS: PRODUCTION FUNCTION")
    print("Cities × Years (Annual Data)")
    print("=" * 80)
    
    # Step 1: Load and prepare data
    print("\n[1/5] Loading data...")
    df = load_panel_data(excel_file, sheet_name)
    
    print("\n[2/5] Preparing panel data...")
    df_panel = prepare_panel_data(df, city_col, year_col)
    
    # Step 2: Fit models
    print("\n[3/5] Fitting models...")
    print("  • Pooled OLS...")
    pols_results = fit_pooled_ols(df_panel, dependent_var, independent_vars)
    
    print("  • Fixed Effects...")
    fe_results = fit_fixed_effects(df_panel, dependent_var, independent_vars)
    
    print("  • Random Effects...")
    re_results = fit_random_effects(df_panel, dependent_var, independent_vars)
    
    # Step 3: Model comparison and tests
    print("\n[4/5] Model comparison and tests...")
    print_model_comparison(pols_results, fe_results, re_results)
    
    # Hausman test
    H, p_value = hausman_test(fe_results, re_results)
    print_hausman_test(H, p_value)
    
    # Step 4: Detailed results
    print("\n[5/5] Detailed results...")
    print_detailed_results(pols_results, "Pooled OLS Results")
    print_detailed_results(fe_results, "Fixed Effects Results")
    print_detailed_results(re_results, "Random Effects Results")
    
    # Step 5: Visualization
    print("\nGenerating visualizations...")
    plot_coefficients(pols_results, fe_results, re_results, independent_vars)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    
    return {
        'pooled_ols': pols_results,
        'fixed_effects': fe_results,
        'random_effects': re_results,
        'hausman_test': (H, p_value),
        'data': df_panel
    }


if __name__ == "__main__":
    # UPDATE THIS PATH TO YOUR EXCEL FILE
    excel_file = "your_data.xlsx"  # Change this to your actual file path
    
    # Run analysis
    results = main(
        excel_file=excel_file,
        sheet_name=0,
        city_col='City',      # Adjust if your column name is different
        year_col='Year',      # Adjust if your column name is different
        dependent_var='ln_Production',  # Adjust to your dependent variable
        independent_vars=['k', 'l', 'w', 'edu']
    )
