# src/run_pipeline.py

import os
from src.featurize_cifs import batch_featurize_cifs_parallel
from src.clean_features import clean_features
from src.visualize_features import visualize_features

def main():
    # Define paths
    input_folder = "data/raw"
    features_csv = "results/features/features.csv"
    cleaned_csv = "data/processed/features_cleaned.csv"
    log_file = "results/logs/featurization.log"
    plot_folder = "results/plots"

    # Featurize CIFs
    batch_featurize_cifs_parallel(
        input_folder=input_folder,
        output_csv=features_csv,
        log_file=log_file,
        workers=4
    )

    # Clean features
    clean_features(
        input_csv=features_csv,
        output_csv=cleaned_csv,
        nan_threshold=0.2,
        fill_method="mean"
    )

    # Visualize
    visualize_features(
        input_csv=cleaned_csv,
        output_dir=plot_folder
    )

