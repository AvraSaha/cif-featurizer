import pandas as pd
import numpy as np

def clean_features(input_csv, output_csv, nan_threshold=0.2, fill_method='mean'):
    """
    Load CSV, report NaNs, clean and save cleaned data.
    
    Parameters:
    - input_csv: path to the input CSV file with features
    - output_csv: path to save the cleaned CSV
    - nan_threshold: fraction (0-1) of allowed NaNs per column before dropping the column
    - fill_method: method to fill NaNs ('mean', 'median', or None to drop rows with NaNs)
    """
    # Load data
    df = pd.read_csv(input_csv)
    print(f"Loaded data with shape: {df.shape}")

    # Report NaNs info
    nan_counts = df.isna().sum()
    nan_fraction = nan_counts / len(df)
    print("NaN counts per column:")
    print(nan_counts[nan_counts > 0])
    
    # Drop columns with too many NaNs
    cols_to_drop = nan_fraction[nan_fraction > nan_threshold].index.tolist()
    if cols_to_drop:
        print(f"Dropping columns with >{nan_threshold*100:.1f}% NaNs: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
    else:
        print("No columns dropped due to NaN threshold.")

    # Fill or drop remaining NaNs
    if fill_method == 'mean':
        print("Filling remaining NaNs with column means.")
        df = df.fillna(df.mean(numeric_only=True))
    elif fill_method == 'median':
        print("Filling remaining NaNs with column medians.")
        df = df.fillna(df.median(numeric_only=True))
    elif fill_method is None:
        print("Dropping rows with any NaNs.")
        df = df.dropna()
    else:
        raise ValueError(f"Unknown fill_method: {fill_method}")

    # Final NaN check
    final_nan_count = df.isna().sum().sum()
    print(f"Total NaNs after cleaning: {final_nan_count}")

    # Save cleaned data
    df.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to {output_csv}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean feature CSV by handling NaNs.")
    parser.add_argument("--input_csv", type=str, required=True, help="Path to input feature CSV")
    parser.add_argument("--output_csv", type=str, required=True, help="Path to save cleaned CSV")
    parser.add_argument("--nan_threshold", type=float, default=0.2,
                        help="Max fraction NaNs allowed per column before dropping it (default=0.2)")
    parser.add_argument("--fill_method", type=str, default="mean",
                        choices=["mean", "median", "none"],
                        help="Method to handle remaining NaNs: mean, median, or none (drop rows). Default: mean")
    args = parser.parse_args()

    fill_method = args.fill_method if args.fill_method != "none" else None

    clean_features(args.input_csv, args.output_csv, args.nan_threshold, fill_method)

