# Caco-2 Permeability Prediction Using Machine Learning

## Overview

This project develops an interpretable machine-learning workflow for predicting **Caco-2 permeability**, an important in-vitro ADMET endpoint used in drug-discovery research.

The workflow combines:

* RDKit molecular descriptors
* Morgan molecular fingerprints
* Random Forest regression
* 5-fold cross-validation
* Out-of-fold (OOF) prediction
* SHAP explainability
* Morgan fingerprint interpretation
* Statistical analysis of molecular environments
* RDKit-based structural visualization

The goal is not only to predict Caco-2 permeability, but also to understand **which molecular properties and local structural environments contribute to model behavior**.

---

## Dataset

The project uses the **Caco2_Wang** dataset from the Therapeutics Data Commons.

The processed dataset contains:

* **910 molecules**
* Molecular identifiers
* SMILES structures
* Caco-2 permeability measurements

The dataset was processed using RDKit before machine-learning analysis.

---

## Molecular Representations

### RDKit Molecular Descriptors

Physicochemical and structural descriptors were calculated from the molecular SMILES using RDKit.

These descriptors capture global molecular characteristics such as:

* molecular size
* lipophilicity
* hydrogen-bonding properties
* molecular topology
* polarity-related characteristics

### Morgan Fingerprints

Morgan circular fingerprints were generated to encode local molecular environments.

Unlike global descriptors, Morgan fingerprints capture structural patterns surrounding individual atoms and therefore provide complementary information about molecular structure.

---

# Machine-Learning Approach

Random Forest regression was used to predict the Caco-2 permeability target.

Three feature representations were compared:

1. RDKit descriptors
2. Morgan fingerprints
3. Combined RDKit descriptors + Morgan fingerprints

Performance was evaluated using **5-fold cross-validation**.

---

# Model Performance

The complete cross-validation comparison is shown below.

| Model                             |    Mean R² |      SD R² |  Mean RMSE |    SD RMSE |   Mean MAE |     SD MAE |
| --------------------------------- | ---------: | ---------: | ---------: | ---------: | ---------: | ---------: |
| RDKit Descriptors                 |     0.7159 |     0.0297 |     0.4114 |     0.0217 |     0.3182 |     0.0103 |
| Morgan Fingerprints               |     0.6612 |     0.0504 |     0.4483 |     0.0344 |     0.3356 |     0.0243 |
| **Combined Descriptors + Morgan** | **0.7455** | **0.0258** | **0.3895** | **0.0217** | **0.3005** | **0.0148** |

The **combined descriptor + Morgan representation performed best**.

Compared with RDKit descriptors alone:

* Mean R² increased from **0.7159 → 0.7455**
* Mean RMSE decreased from **0.4114 → 0.3895**
* Mean MAE decreased from **0.3182 → 0.3005**
* R² variability decreased from **0.0297 → 0.0258**

These results suggest that global physicochemical descriptors and local molecular fingerprints provide complementary information for Caco-2 permeability prediction.

The complete model comparison is stored in:

`results/caco2_model_comparison.csv`

---

# Out-of-Fold Validation

Pooled out-of-fold predictions were generated for all **910 molecules** using the combined molecular representation.

The pooled OOF performance was:

| Metric        | OOF Performance |
| ------------- | --------------: |
| Molecules     |             910 |
| R²            |      **0.7230** |
| RMSE          |      **0.4089** |
| MAE           |      **0.3177** |
| Mean residual |         −0.0216 |
| Residual SD   |          0.4085 |

The OOF predictions are stored in:

`results/caco2_combined_oof_predictions.csv`

### CV vs OOF

The **0.7455 R²** is the mean of the five individual cross-validation fold scores.

The **0.7230 R²** is calculated after pooling the predictions generated for every molecule when that molecule was held out during cross-validation.

These are therefore different but complementary measures of model performance.

---

# SHAP Model Interpretation

SHAP was used to investigate which molecular features influence Random Forest predictions.

The analysis provides:

* global feature importance
* direction and magnitude of feature effects
* feature-level interpretation
* hydrogen-bond donor dependence analysis

Current SHAP figures include:

```text
figures/caco2_shap_summary.png
figures/caco2_shap_feature_importance.png
figures/caco2_shap_HBD_dependence.png
```

SHAP provides a global explanation of the model based on the molecular descriptor representation.

---

# Morgan Fingerprint Interpretation

Morgan fingerprints were subsequently analyzed at the local molecular-environment level.

Candidate fingerprint bits were evaluated using:

* Random Forest importance
* number of molecules containing the bit
* difference between groups
* Cohen's d
* p-value
* FDR-adjusted q-value
* 95% confidence interval
* adjusted fingerprint coefficient
* incremental R²

Four representative Morgan environments were selected for detailed interpretation:

**Bit 623, Bit 82, Bit 1290, and Bit 550.**

---

# Key Morgan Fingerprint Results

| Bit      | N Present | Difference |   Cohen's d |      FDR q-value | Adjusted coefficient |          ΔR² |
| -------- | --------: | ---------: | ----------: | ---------------: | -------------------: | -----------: |
| **623**  |        52 |    −0.9217 |     −1.2329 |      6.70 × 10⁻⁹ |              −1.1612 | **+0.00850** |
| **82**   |        23 |    −1.3082 | **−1.7442** |      5.24 × 10⁻⁸ |              −1.4955 |     +0.00497 |
| **1290** |        38 |    −1.0128 |     −1.3491 |      3.12 × 10⁻⁹ |              −0.9232 |     +0.00288 |
| **550**  |        33 |    −1.2467 |     −1.6805 | **7.90 × 10⁻¹¹** |              −1.0997 |     −0.00027 |

All four environments showed statistically significant associations after FDR correction.

Bit 82 produced the largest standardized effect size, while Bit 550 produced the strongest FDR-adjusted statistical evidence.

Bit 623 produced the largest incremental R² improvement among the four evaluated environments.

These results represent **statistical associations**, not proof that the individual molecular environments causally determine permeability.

---

# Exact Morgan Environment Verification

The four selected Morgan environments were independently verified using RDKit's Morgan fingerprint `bitInfo` mapping.

| Bit      | Representative molecule | Atom | Radius | Verification |
| -------- | ----------------------- | ---: | -----: | ------------ |
| **623**  | Creatinine              |    7 |      0 | Verified     |
| **82**   | PNU200001               |    1 |      2 | Verified     |
| **1290** | Elarofiban              |    3 |      1 | Verified     |
| **550**  | Echinacoside            |    1 |      2 | Verified     |

The exact atom/radius environments were then highlighted on the corresponding molecular structures.

---

# Morgan Environment Figures

Individual exact Morgan environments are stored in:

```text
results/morgan_bit_visualizations/
```

The final four-panel figure is:

```text
results/morgan_bit_visualizations/key_morgan_environments_4panel.png
```

This figure connects the statistical fingerprint analysis to explicit molecular structures.

---

# Project Structure

```text
admet-drug-discovery-ml/
│
├── data/
│   └── caco2_wang.csv
│
├── src/
│   ├── 01_download_data.py
│   ├── 02_generate_descriptors.py
│   ├── 03_generate_morgan.py
│   ├── 04_model_comparison.py
│   ├── 05_visualize_key_morgan_bits.py
│   └── 06_final_morgan_bit_figures.py
│
├── results/
│   ├── caco2_model_comparison.csv
│   ├── caco2_combined_oof_predictions.csv
│   │
│   ├── morgan_bit_analysis/
│   │   ├── final_morgan_chemical_environments.csv
│   │   ├── final_morgan_interpretability_table.csv
│   │   └── morgan_interpretability_figure.png
│   │
│   └── morgan_bit_visualizations/
│       ├── key_morgan_environments_4panel.png
│       ├── morgan_bit_623_EXACT.png
│       ├── morgan_bit_82_EXACT.png
│       ├── morgan_bit_1290_EXACT.png
│       └── morgan_bit_550_EXACT.png
│
├── figures/
│   ├── caco2_shap_summary.png
│   ├── caco2_shap_feature_importance.png
│   └── caco2_shap_HBD_dependence.png
│
├── requirements.txt
└── README.md
```

---

# Reproducibility

The principal analysis scripts are located in `src/`.

The Python environment dependencies are specified in:

```text
requirements.txt
```

The workflow is organized so that data preparation, molecular representation generation, model comparison, and molecular interpretation can be reproduced from the source code.

---

# Scientific Interpretation

The project demonstrates a two-level approach to interpretable ADMET machine learning.

At the **global level**, molecular descriptors and SHAP analysis identify physicochemical characteristics associated with model predictions.

At the **local structural level**, Morgan fingerprint analysis identifies molecular environments that show statistically significant associations with the Caco-2 target.

Together, these approaches connect:

**molecular structure → numerical representation → machine-learning prediction → model explanation → chemical interpretation**

This provides a more informative workflow than prediction alone.

---

# Limitations

1. Caco-2 permeability is an experimental in-vitro endpoint and does not capture the complete process of human intestinal absorption.
2. Morgan fingerprint bits are computational representations and should not automatically be interpreted as unique biological mechanisms.
3. Statistical association does not establish causality.
4. The same fingerprint bit may occur in different chemical contexts across molecules.
5. Model performance should be interpreted using cross-validation and OOF analysis rather than relying on a single train/test split.
6. Independent external validation would provide stronger evidence of generalizability.

---

# Future Work

Potential extensions include:

* independent external validation
* scaffold-based validation
* applicability-domain analysis
* uncertainty estimation
* additional machine-learning algorithms
* chemical-space analysis
* systematic interpretation of additional Morgan environments
* integration with additional ADMET endpoints
* prospective prioritization of compounds for experimental testing

---

# Conclusion

This project establishes an interpretable machine-learning workflow for Caco-2 permeability prediction using molecular descriptors and Morgan fingerprints.

The combined representation achieved the strongest 5-fold cross-validation performance, with a mean R² of **0.7455**, RMSE of **0.3895**, and MAE of **0.3005**.

Pooled out-of-fold predictions across 910 molecules produced an R² of **0.7230**, RMSE of **0.4089**, and MAE of **0.3177**.

SHAP analysis provides global feature-level interpretation, while Morgan fingerprint analysis adds a localized structural interpretation layer. Four Morgan environments—**623, 82, 1290, and 550**—showed strong statistically significant associations with the Caco-2 target after FDR correction.

Overall, the project demonstrates how **machine learning, cheminformatics, statistical analysis, and molecular visualization can be integrated into an interpretable ADMET modeling workflow**.

