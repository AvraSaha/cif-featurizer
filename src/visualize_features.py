def visualize_features(input_csv, output_dir):
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv(input_csv)
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Distribution plots
    plt.figure(figsize=(12, 8))
    for i, col in enumerate(numeric_cols[:6], 1):
        plt.subplot(2, 3, i)
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f'Distribution of {col}')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "feature_distributions.png"))
    plt.close()

    # Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Feature Correlation Heatmap")
    plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
    plt.close()

    # Pairplot
    sns.pairplot(df[numeric_cols[:4]])
    plt.savefig(os.path.join(output_dir, "pairplot.png"))
    plt.close()

