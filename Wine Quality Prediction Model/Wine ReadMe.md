# Wine Quality Prediction Model

> A machine learning classification project that predicts red wine quality scores using physicochemical properties, comparing logistic regression against a hyperparameter-tuned random forest.

---

## Overview

Using the UCI Wine Quality dataset, this notebook walks through the full machine learning pipeline: exploratory data analysis, preprocessing, model training, hyperparameter tuning, and evaluation. Two classifiers are compared, with the tuned random forest serving as the primary model and logistic regression as the baseline.

The project demonstrates practical skills in data cleaning, feature analysis, class-imbalance handling, and model evaluation using multiple metrics rather than accuracy alone.

---

## Dataset

The notebook uses the [UCI Wine Quality dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality) (`winequality-red.csv`), which contains 1,599 red wine samples described by 11 physicochemical features and rated on a quality scale from 0 to 10.

Place `winequality-red.csv` in the same directory as the notebook before running.

---

## Notebook Structure

| Section | Description |
|---|---|
| Data loading and inspection | Shape, dtypes, descriptive statistics |
| Missing data analysis | Null checks across all features |
| Exploratory data analysis | Quality score distribution, feature histograms, correlation heatmap, boxplots of top features vs quality |
| Outlier detection | IQR-based outlier counts per feature |
| Preprocessing pipeline | Train/test split with stratification, standard scaling |
| Baseline model | Logistic regression |
| Primary model | Random forest (100 estimators) |
| Hyperparameter tuning | GridSearchCV across estimators, depth, split size, and max features with 5-fold cross-validation |
| Feature importance | Bar chart of random forest feature importances |
| Evaluation | Classification reports, confusion matrices, and learning curves for both models |
| Summary | Accuracy, weighted F1, and macro F1 comparison table |

---

## Key Techniques

- Stratified train/test split to preserve class distribution across quality scores
- StandardScaler fitted on training data only, applied to test data separately to prevent data leakage
- GridSearchCV with weighted F1 scoring, chosen over accuracy to account for class imbalance in quality ratings
- Learning curves used to assess overfitting and generalisation across training set sizes

---

## Outputs

Running the notebook produces the following saved figures:

- `correlation_heatmap.png` — feature correlation matrix
- `boxplots_top_features.png` — alcohol, volatile acidity, sulphates, and citric acid vs quality
- `feature_importance.png` — ranked random forest feature importances
- `confusion_matrices.png` — side-by-side confusion matrices for both models
- `learning_curves.png` — training and cross-validation F1 scores across dataset sizes

---

## How to Run

### Prerequisites

- Python 3.9+
- Jupyter Notebook or JupyterLab

### Install dependencies

```bash
pip install -r requirements.txt
```

### Launch

```bash
jupyter notebook Wine_Quality_Prediction_Model.ipynb
```

Run all cells in order. The dataset file must be present in the same directory.

---

## Skills Demonstrated

- Exploratory data analysis and feature engineering
- Data preprocessing and scaling pipelines
- Binary and multiclass classification with scikit-learn
- Hyperparameter tuning with GridSearchCV
- Model evaluation using F1-weighted, F1-macro, accuracy, and confusion matrices
- Visualisation with Matplotlib and Seaborn