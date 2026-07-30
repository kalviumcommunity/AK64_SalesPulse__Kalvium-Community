"""
String Cleaning & Text Normalisation Pipeline
---------------------------------------------
Assignment 11 - Kalvium SalesPulse Data Cleaning Pipeline

This script implements a comprehensive string cleaning and text normalisation
pipeline for messy customer, product, and segment text data.

Tasks Covered:
1. Strip Whitespace Consistently
2. Normalize Casing to Consistent Standard
3. Remove Special Characters Using Regex
4. Standardize Categorical Labels Using Mapping Dictionary
5. Build Reusable String Cleaning Function
"""

import os
import pandas as pd
import numpy as np


def create_synthetic_messy_data():
    """Create synthetic DataFrame with messy text data across multiple columns."""
    data = {
        'customer_name': [
            ' John Smith ',
            'JOHN SMITH',
            'john smith',
            ' Alice Brown ',
            'ALICE BROWN',
            'São Paulo_John',
            'Montréal_Marie!',
            'Carol White#',
            '  David Lee  ',
            'david lee'
        ],
        'product_category': [
            ' Electronics ',
            'electronics',
            'ELECTRONICS',
            ' Home & Kitchen ',
            'home_kitchen!',
            'HOME KITCHEN',
            ' Clothing ',
            'clothing#',
            'CLOTHING',
            ' Electronics '
        ],
        'customer_segment': [
            'b2b',
            'b 2 b',
            'business-to-business',
            'sme',
            'small medium enterprise',
            's m b',
            'enterprise',
            'ent',
            'corp',
            'b2b'
        ],
        'location_city': [
            'São Paulo',
            'Montréal',
            ' New York ',
            'NEW YORK',
            'new york',
            'san_francisco!',
            'London#',
            'Tokyo@',
            'São Paulo',
            ' Paris '
        ]
    }
    return pd.DataFrame(data)


# Task 1: Strip Whitespace Consistently
def strip_all_strings(df):
    """
    Strip leading and trailing whitespace from all string columns in the DataFrame.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        df: pandas DataFrame with stripped string columns
    """
    df_cleaned = df.copy()
    string_cols = df_cleaned.select_dtypes(include=['object', 'string']).columns
    
    print("\n--- TASK 1: STRIPPING WHITESPACE ---")
    total_whitespace_fixed = 0
    
    for col in string_cols:
        before_unique = df_cleaned[col].nunique()
        has_whitespace = df_cleaned[col].str.contains(r'^\s+|\s+$', regex=True, na=False).sum()
        total_whitespace_fixed += has_whitespace
        
        df_cleaned[col] = df_cleaned[col].str.strip()
        after_unique = df_cleaned[col].nunique()
        
        print(f"Column '{col}': {before_unique} -> {after_unique} unique values ({has_whitespace} values stripped)")
    
    print(f"Total whitespace issues fixed across dataset: {total_whitespace_fixed}")
    return df_cleaned


# Task 2: Normalize Casing to Consistent Standard
def normalize_casing(df, columns_to_lower):
    """
    Normalize casing for specified columns to lowercase.
    
    Business Decision:
        Normalizing categorical text to lowercase prevents case variation 
        (e.g., 'JOHN', 'john', 'John') from creating duplicate groups during 
        groupby aggregations, segment counts, and join operations. Lowercase is 
        chosen as the global analytics standard.
    
    Args:
        df: pandas DataFrame
        columns_to_lower: list of column names
        
    Returns:
        df: DataFrame with normalized casing
    """
    df_cleaned = df.copy()
    print("\n--- TASK 2: NORMALIZE CASING ---")
    
    for col in columns_to_lower:
        if col in df_cleaned.columns:
            before_counts = df_cleaned[col].nunique()
            df_cleaned[col] = df_cleaned[col].str.lower()
            after_counts = df_cleaned[col].nunique()
            print(f"Normalized '{col}' to lowercase ({before_counts} -> {after_counts} unique values)")
            
    return df_cleaned


# Task 3: Remove Special Characters Using Regex
def remove_special_characters(df, columns):
    """
    Remove special characters using regex pattern [^a-zA-Z0-9 ].
    
    Regex Pattern Explanation:
        - [^a-zA-Z0-9 ]: Brackets [] define a character set.
        - Caret ^ at the beginning inside [] means negation (NOT).
        - a-zA-Z matches all English uppercase and lowercase letters.
        - 0-9 matches all digits.
        - Space ' ' matches whitespace.
        - Combined: Matches any character that is NOT an alphanumeric letter, number, or space,
          replacing symbols like !, #, @, _, as well as accented non-ASCII characters.
          For instance, 'São Paulo' becomes 'So Paulo' and 'Montréal' becomes 'Montreal'.
    
    Args:
        df: pandas DataFrame
        columns: list of column names
        
    Returns:
        df: DataFrame with special characters removed
    """
    df_cleaned = df.copy()
    print("\n--- TASK 3: REMOVE SPECIAL CHARACTERS VIA REGEX ---")
    pattern = r'[^a-zA-Z0-9 ]'
    
    for col in columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].str.replace(pattern, '', regex=True)
            print(f"Removed special characters from column '{col}' using regex '{pattern}'")
            
    return df_cleaned


# Task 4: Standardize Categorical Labels Using Mapping Dictionary
def standardize_categorical_labels(df, col_name, mapping):
    """
    Standardize categorical variations into canonical forms using a mapping dictionary.
    
    Business Decision / Justifications:
        1. B2B variations ('b2b', 'b 2 b', 'business-to-business') -> 'B2B':
           Standardized to uppercase 'B2B' for consistency with CRM database schema.
        2. SMB variations ('sme', 'small medium enterprise', 's m b') -> 'SMB':
           Standardized to 'SMB' as standard financial reporting metric.
        3. Enterprise variations ('ent', 'enterprise', 'corp') -> 'Enterprise':
           Standardized to 'Enterprise' for global sales territory classification.
    
    Args:
        df: pandas DataFrame
        col_name: target column name
        mapping: dict mapping raw/cleaned labels to canonical forms
        
    Returns:
        df: DataFrame with standardized categorical column
    """
    df_cleaned = df.copy()
    print("\n--- TASK 4: STANDARDIZE CATEGORICAL LABELS ---")
    
    if col_name in df_cleaned.columns:
        print(f"Value counts before mapping for '{col_name}':")
        print(df_cleaned[col_name].value_counts())
        
        df_cleaned[col_name] = df_cleaned[col_name].map(mapping).fillna(df_cleaned[col_name])
        
        print(f"\nValue counts after mapping for '{col_name}':")
        print(df_cleaned[col_name].value_counts())
        
    return df_cleaned


# Task 5: Build Reusable String Cleaning Function
def clean_text_column(series, lowercase=True, strip=True, remove_special=False, mapping=None):
    """
    Reusable text cleaning function for any pandas string column (Series).
    
    Args:
        series: pandas Series to clean
        lowercase: bool, whether to convert text to lowercase
        strip: bool, whether to strip leading/trailing whitespace
        remove_special: bool, whether to remove non-alphanumeric characters with regex
        mapping: dict, optional dictionary to map categorical labels to canonical form
        
    Returns:
        series: cleaned pandas Series
    """
    result = series.copy()
    
    # Handle null values with warning
    if result.isna().any():
        null_count = result.isna().sum()
        print(f"Warning: {null_count} null value(s) detected in column '{series.name}'. Preserving nulls.")
    
    if strip:
        result = result.str.strip()
        
    if lowercase:
        result = result.str.lower()
        
    if remove_special:
        result = result.str.replace(r'[^a-zA-Z0-9 ]', '', regex=True)
        
    if mapping:
        # Use map and retain unmapped non-null values or map directly
        result = result.map(mapping).fillna(result)
        
    return result


def run_pipeline():
    """Run full demonstration of the string cleaning pipeline and verify requirements."""
    print("=========================================================")
    print("      STRING CLEANING & TEXT NORMALISATION PIPELINE      ")
    print("=========================================================")
    
    # Ensure data directories exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Create and save synthetic dataset
    raw_df = create_synthetic_messy_data()
    raw_df.to_csv('data/raw/messy_text_data.csv', index=False)
    print("\nLoaded raw messy dataset (data/raw/messy_text_data.csv):")
    print(raw_df)
    
    # --- TASK 1 DEMONSTRATION ---
    print("\n" + "="*50)
    print("DEMO TASK 1: Strip Whitespace")
    print("="*50)
    print("Before whitespace strip value counts for 'product_category':")
    print(raw_df['product_category'].value_counts())
    print("\nBefore whitespace strip value counts for 'location_city':")
    print(raw_df['location_city'].value_counts())
    
    df_step1 = strip_all_strings(raw_df)
    
    print("\nAfter whitespace strip value counts for 'product_category':")
    print(df_step1['product_category'].value_counts())
    print("\nAfter whitespace strip value counts for 'location_city':")
    print(df_step1['location_city'].value_counts())
    
    # --- TASK 2 DEMONSTRATION ---
    print("\n" + "="*50)
    print("DEMO TASK 2: Normalize Casing")
    print("="*50)
    cols_to_lower = ['customer_name', 'product_category', 'location_city']
    print("Sample rows before casing normalization:")
    print(df_step1[cols_to_lower].head())
    
    df_step2 = normalize_casing(df_step1, cols_to_lower)
    
    print("\nSample rows after casing normalization:")
    print(df_step2[cols_to_lower].head())
    
    print("\nVerification that 'JOHN SMITH', 'john smith', and ' John Smith ' consolidated:")
    print(df_step2['customer_name'].value_counts())
    
    # --- TASK 3 DEMONSTRATION ---
    print("\n" + "="*50)
    print("DEMO TASK 3: Remove Special Characters via Regex")
    print("="*50)
    print("Sample location_city before regex special char removal:")
    print(df_step2['location_city'].tolist())
    
    df_step3 = remove_special_characters(df_step2, ['customer_name', 'product_category', 'location_city'])
    
    print("\nSample location_city after regex special char removal:")
    print(df_step3['location_city'].tolist())
    print("\nDemonstration of international character transformation:")
    print(" 'são paulo' -> 'so paulo'")
    print(" 'montréal'  -> 'montreal'")
    
    # --- TASK 4 DEMONSTRATION ---
    print("\n" + "="*50)
    print("DEMO TASK 4: Standardize Categorical Labels")
    print("="*50)
    segment_map = {
        # Category 1: B2B variations
        'b2b': 'B2B',
        'b 2 b': 'B2B',
        'b2 b': 'B2B',
        'business-to-business': 'B2B',
        'businesstobusiness': 'B2B',
        
        # Category 2: SMB variations
        'sme': 'SMB',
        'small medium enterprise': 'SMB',
        'smallmediumenterprise': 'SMB',
        's m b': 'SMB',
        'smb': 'SMB',
        
        # Category 3: Enterprise variations
        'enterprise': 'Enterprise',
        'ent': 'Enterprise',
        'corp': 'Enterprise'
    }
    
    df_step4 = standardize_categorical_labels(df_step2, 'customer_segment', segment_map)
    
    # --- TASK 5 DEMONSTRATION ---
    print("\n" + "="*50)
    print("DEMO TASK 5: Reusable String Cleaning Function")
    print("="*50)
    print("Applying clean_text_column to 3 different columns with distinct parameter choices:\n")
    
    demo_df = create_synthetic_messy_data()
    
    # Column 1: customer_name - strip whitespace & normalize case
    print("1. customer_name: strip=True, lowercase=True, remove_special=False")
    demo_df['customer_name_clean'] = clean_text_column(
        demo_df['customer_name'], 
        strip=True, 
        lowercase=True, 
        remove_special=False
    )
    
    # Column 2: location_city - strip whitespace, lowercase & remove special chars
    print("2. location_city: strip=True, lowercase=True, remove_special=True")
    demo_df['location_city_clean'] = clean_text_column(
        demo_df['location_city'], 
        strip=True, 
        lowercase=True, 
        remove_special=True
    )
    
    # Column 3: customer_segment - strip whitespace, lowercase, remove_special & apply mapping
    print("3. customer_segment: strip=True, lowercase=True, remove_special=True, mapping=segment_map")
    demo_df['customer_segment_clean'] = clean_text_column(
        demo_df['customer_segment'], 
        strip=True, 
        lowercase=True, 
        remove_special=True,
        mapping=segment_map
    )
    
    print("\nCleaned Columns Comparison Sample:")
    print(demo_df[['customer_name', 'customer_name_clean', 'location_city', 'location_city_clean', 'customer_segment', 'customer_segment_clean']].head())
    
    # --- EDGE CASE TESTING ---
    print("\n" + "="*50)
    print("RUNNING EDGE CASE TESTS")
    print("="*50)
    test_cases = [
        '  Product A  ',      # Leading/trailing spaces
        'PRODUCT B',         # All caps
        'Product_C',         # Special char
        None,                # Null value
        ''                   # Empty string
    ]
    test_series = pd.Series(test_cases, name='test_column')
    print("Input Edge Case Series:")
    print(test_series)
    
    cleaned_test_series = clean_text_column(
        test_series, 
        lowercase=True, 
        strip=True, 
        remove_special=True
    )
    print("\nOutput Cleaned Series:")
    print(cleaned_test_series)
    
    # Save final cleaned dataset
    final_df = df_step4.copy()
    final_df.to_csv('data/processed/clean_text_data.csv', index=False)
    print("\nSaved final clean dataset to 'data/processed/clean_text_data.csv'.")
    print("Pipeline Execution Completed Successfully.")


if __name__ == '__main__':
    run_pipeline()
