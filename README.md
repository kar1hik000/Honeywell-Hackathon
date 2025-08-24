# Multivariate Time-Series Anomaly Detection Ensemble

This project implements a robust and modular ensemble pipeline for detecting anomalies in multivariate time-series data, such as sensor readings. It combines the strengths of tree-based, density-based, and sequence-aware models to produce a calibrated abnormality score and identify the most significant contributing features for each detected anomaly.

## Key Features

-   **Ensemble Model:** Utilizes a weighted combination of Isolation Forest (IForest), Local Outlier Factor (LOF), and an LSTM Autoencoder (LSTM-AE) for comprehensive anomaly detection.
-   **Calibrated Scoring:** Generates an `abnormality_score` on a scale of 0-100, calibrated on a user-defined "normal" training period.
-   **Feature Attribution:** Identifies the top 7 features contributing to each anomaly, using SHAP (SHapley Additive exPlanations) when available, with a fallback to a robust z-score and reconstruction error-based method.
-   **Data Handling:** Includes robust preprocessing for numeric data, handles missing values, and is designed to manage edge cases like insufficient data or all-normal datasets.
-   **Ease of Use:** Can be run with a simple main entrypoint that only requires input and output CSV paths.
-   **Analysis & Reporting:** Comes with add-ons for interactive visualization of anomaly timelines, feature attribution heatmaps, and automatic generation of severity reports.

## Technical Approach

The pipeline follows a structured, end-to-end workflow:

1.  **Data Loading and Preprocessing:**
    * Loads data from a CSV file.
    * Identifies and processes a timestamp column if specified.
    * Selects only numeric features for analysis.
    * Handles missing values using forward and backward fill.

2.  **Model Training:**
    * Data is split into a "normal" training window and the full dataset.
    * Features are scaled using `RobustScaler`.
    * An **Isolation Forest** and a **Local Outlier Factor** model are trained on the normal data. For high-dimensional data, PCA is applied before training the LOF model.
    * An optional **LSTM Autoencoder** is trained to learn temporal patterns and identify anomalies based on reconstruction errors.

3.  **Scoring and Calibration:**
    * The trained models are used to score the entire dataset.
    * Individual model scores are combined into a single raw ensemble score using configurable weights.
    * This raw score is then calibrated to a 0-100 scale based on the distribution of scores from the normal training period.

4.  **Score Smoothing and Feature Attribution:**
    * An Exponentially Weighted Moving Average (EWMA) is applied to the calibrated scores to ensure stability and reduce noise.
    * The top contributing features for each data point are determined to provide explainability for the anomaly scores.

5.  **Output Generation:**
    * The final output is a CSV file containing the original data along with the `abnormality_score` and `top_feature_1` through `top_feature_7` columns.

## Setup and Usage

### Dependencies

The core pipeline relies on standard Python data science libraries. For full functionality, including the LSTM model and SHAP-based feature attribution, additional packages are needed.

**Core Dependencies:**
-   `pandas`
-   `numpy`
-   `scikit-learn`

**Optional Dependencies:**
-   `tensorflow` (for the LSTM Autoencoder)
-   `shap` (for SHAP-based feature attribution)
-   `plotly` (for interactive visualizations)
-   `matplotlib` (as a fallback for plotting)

You can install the necessary packages using pip:
```bash
pip install pandas numpy scikit-learn tensorflow shap plotly matplotlib
