# Interpretable Machine Learning for Caco-2 Permeability Prediction

**Cheminformatics • ADMET • Molecular Machine Learning • Explainable AI • Molecular Interpretation**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![RDKit](https://img.shields.io/badge/RDKit-Cheminformatics-green.svg)](https://www.rdkit.org/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-purple.svg)](https://shap.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

## Overview

Caco-2 permeability is an important **in-vitro ADMET endpoint** used to investigate intestinal permeability during drug-discovery research.

This project develops a reproducible and interpretable machine-learning workflow for predicting Caco-2 permeability from molecular structure.

Rather than treating the problem as prediction alone, the workflow investigates **why the models make their predictions** by combining:

* RDKit molecular descriptors
* Morgan circular fingerprints
* Random Forest regression
* 5-fold cross-validation
* pooled out-of-fold (OOF) prediction
* SHAP-based model interpretation
* statistical analysis of Morgan fingerprint environments
* RDKit-based molecular visualization

The central research question is:

> **Can combining global physicochemical descriptors with local molecular fingerprints improve Caco-2 permeability prediction while retaining chemically interpretable information?**

---

## Key Results

### Model comparison

Three molecular representations were evaluated using 5-fold cross-validation.

| Representation           |    Mean R² |      SD R² |  Mean RMSE |   Mean MAE |
| ------------------------ | ---------: | ---------: | ---------: | ---------: |
| RDKit descriptors        | **0.7159** |     0.0297 |     0.4114 |     0.3182 |
| Morgan fingerprints      |     0.6612 |     0.0504 |     0.4483 |     0.3356 |
| **Descriptors + Morgan** | **0.7455** | **0.0258** | **0.3895** | **0.3005** |

The combined representation produced the strongest cross-validation performance.

Compared with RDKit descriptors alone:

* **R²:** 0.7159 → **0.7455**
* **RMSE:** 0.4114 → **0.3895**
* **MAE:** 0.3182 → **0.3005**
* **R² variability:** 0.0297 → **0.0258**

This indicates that global physicochemical descriptors and local structural fingerprints provide complementary information for this dataset.

### Pooled out-of-fold performance

To obtain a molecule-level estimate using predictions generated while each molecule was held out, predictions from all five validation folds were pooled.

| Metric        | OOF performance |
| ------------- | --------------: |
| Molecules     |             910 |
| R²            |      **0.7230** |
| RMSE          |      **0.4089** |
| MAE           |      **0.3177** |
| Mean residual |         −0.0216 |
| Residual SD   |          0.4085 |

The distinction between the mean CV score and pooled OOF score is intentional:

* **0.7455 R²** = mean of the five fold-level R² values
* **0.7230 R²** = R² calculated after pooling all out-of-fold predictions

These metrics answer related but different questions and are therefore both reported.

---

## Research Workflow

```text
Caco-2 molecular dataset
          │
          ▼
      Data cleaning
          │
          ▼
 ┌─────────────────────┐
 │ Molecular structure │
 │       SMILES        │
 └─────────────────────┘
          │
     ┌────┴────┐
     ▼         ▼
 RDKit      Morgan
descriptors fingerprints
     │         │
     └────┬────┘
          ▼
   Representation
    comparison
          │
          ▼
 Random Forest models
          │
          ▼
    5-fold CV + OOF
          │
     ┌────┴──────────────┐
     ▼                   ▼
  SHAP analysis     Morgan-bit
     │              interpretation
     │                   │
     ▼                   ▼
Global molecular     Local chemical
feature effects      environments
          │                   │
          └─────────┬─────────┘
                    ▼
        Interpretable ADMET model
```

---

## Dataset

The project uses the **Caco2_Wang** dataset from the Therapeutics Data Commons.

The processed dataset contains:

* **910 molecules**
* molecular identifiers
* SMILES structures
* experimental Caco-2 permeability measurements

Molecular structures were processed using RDKit before feature generation.

The dataset is retained in the repository under:

```text
data/
├── raw/
│   └── caco2_wang.csv
└── processed/
    ├── caco2_rdkit_features.csv
    ├── caco2_morgan_fingerprints.csv
    └── ...
```

---

# Molecular Representations

## 1. RDKit Molecular Descriptors

Physicochemical and structural descriptors were calculated from molecular SMILES using RDKit.

These descriptors capture global molecular characteristics including:

* molecular size
* lipophilicity
* hydrogen-bonding properties
* molecular topology
* polarity-related properties

These features provide a compact representation of whole-molecule physicochemical behavior.

---

## 2. Morgan Fingerprints

Morgan circular fingerprints encode local molecular environments around atoms.

Unlike conventional global descriptors, fingerprints capture structural patterns occurring within localized molecular neighborhoods.

This provides complementary structural information that may not be represented explicitly by a small descriptor set.

---

## 3. Combined Representation

The final representation combines:

```text
RDKit descriptors + Morgan fingerprints
```

The improvement in cross-validation performance suggests that the two representations contain complementary predictive information.

---

# Machine-Learning Model

A **Random Forest regression** model was used as the primary predictive algorithm.

The three representations evaluated were:

1. RDKit molecular descriptors
2. Morgan fingerprints
3. RDKit descriptors + Morgan fingerprints

Performance was evaluated using **5-fold cross-validation**.

The workflow also generated pooled **out-of-fold predictions**, allowing molecule-level residual analysis without using predictions from a model trained on that molecule.

---

# Model Performance

![Model representation comparison](figures/caco2_model_representation_comparison.png)

*Comparison of Caco-2 permeability prediction performance across molecular representations.*

The combined representation achieved the strongest overall cross-validation performance.

The result supports a central modeling observation:

> **Global physicochemical descriptors and local structural fingerprints can provide complementary information for Caco-2 permeability prediction.**

Complete numerical results are available in:

```text
results/caco2_model_comparison.csv
```

---

# Out-of-Fold Prediction Analysis

![OOF predicted vs experimental](figures/caco2_oof_predicted_vs_experimental.png)

*Experimental versus pooled out-of-fold predictions for the 910 molecules.*

![OOF residuals](figures/caco2_oof_residuals.png)

*Residual distribution from pooled out-of-fold predictions.*

The OOF analysis provides a more granular view of model behavior across the complete dataset.

The predictions are available in:

```text
results/caco2_combined_oof_predictions.csv
```

---

# Explainable AI with SHAP

Prediction performance alone does not explain which molecular properties influence the model.

SHAP was therefore used to investigate the contribution of molecular features to Random Forest predictions.

The analysis includes:

* global feature importance
* feature contribution magnitude
* direction of feature effects
* hydrogen-bond donor dependence

## SHAP summary

![SHAP summary](figures/caco2_shap_summary.png)

## SHAP feature importance

![SHAP feature importance](figures/caco2_shap_feature_importance.png)

## Hydrogen-bond donor dependence

![HBD SHAP dependence](figures/caco2_shap_HBD_dependence.png)

This provides a **global molecular-property interpretation layer** for the predictive model.

---

# Morgan Fingerprint Interpretation

The analysis was extended beyond global molecular descriptors to investigate individual Morgan fingerprint environments.

Candidate fingerprint bits were evaluated using multiple complementary criteria:

* Random Forest importance
* number of molecules containing the fingerprint
* difference between groups
* Cohen's *d*
* p-value
* FDR-adjusted q-value
* 95% confidence interval
* adjusted fingerprint coefficient
* incremental R²

This allows fingerprint features to be investigated statistically rather than simply ranked by model importance.

---

## Key Morgan Environments

Four representative fingerprint environments were selected for detailed structural interpretation:

| Morgan bit | N present | Difference | Cohen's *d* |      FDR q-value | Adjusted coefficient |      ΔR² |
| ---------: | --------: | ---------: | ----------: | ---------------: | -------------------: | -------: |
|        623 |        52 |    −0.9217 |     −1.2329 |      6.70 × 10⁻⁹ |              −1.1612 | +0.00850 |
|         82 |        23 |    −1.3082 | **−1.7442** |      5.24 × 10⁻⁸ |              −1.4955 | +0.00497 |
|       1290 |        38 |    −1.0128 |     −1.3491 |      3.12 × 10⁻⁹ |              −0.9232 | +0.00288 |
|        550 |        33 |    −1.2467 |     −1.6805 | **7.90 × 10⁻¹¹** |              −1.0997 | −0.00027 |

All four selected environments remained statistically significant after FDR correction.

### Interpretation

* **Bit 82** showed the largest standardized effect size.
* **Bit 550** showed the strongest FDR-adjusted statistical evidence.
* **Bit 623** produced the largest incremental R² improvement among the four evaluated environments.

These findings should be interpreted as **statistical associations**, not evidence that an individual molecular environment causally determines permeability.

---

# Exact Structural Verification

Morgan fingerprint interpretation can be difficult because a fingerprint bit is an encoded representation rather than a chemical name.

To make the interpretation chemically explicit, the selected bits were independently verified using RDKit's Morgan fingerprint `bitInfo` mapping.

|  Bit | Representative molecule | Atom | Radius | Status   |
| ---: | ----------------------- | ---: | -----: | -------- |
|  623 | Creatinine              |    7 |      0 | Verified |
|   82 | PNU200001               |    1 |      2 | Verified |
| 1290 | Elarofiban              |    3 |      1 | Verified |
|  550 | Echinacoside            |    1 |      2 | Verified |

The exact atom/radius environments were then highlighted on the corresponding molecular structures.

## Four key molecular environments

![Key Morgan environments](results/morgan_bit_visualizations/key_morgan_environments_4panel.png)

*Exact structural environments corresponding to the four selected Morgan fingerprint bits.*

Individual verified structures are available in:

```text
results/morgan_bit_visualizations/
```

---

# Two Levels of Molecular Interpretation

The project deliberately combines two complementary interpretation strategies.

### Global interpretation

```text
Molecular descriptors
        ↓
Random Forest
        ↓
SHAP
        ↓
Global physicochemical effects
```

### Local structural interpretation

```text
Morgan fingerprints
        ↓
Statistical analysis
        ↓
Fingerprint bit
        ↓
RDKit bitInfo verification
        ↓
Explicit molecular environment
```

Together they connect:

**molecular structure → numerical representation → machine-learning prediction → model explanation → chemical interpretation**

This is the primary scientific focus of the project.

---

# Reproducibility

The analysis pipeline is organized into sequential Python scripts.

```text
src/
├── 01_download_data.py
├── 02_generate_descriptors.py
├── 03_generate_morgan.py
├── 04_model_comparison.py
├── 05_visualize_key_morgan_bits.py
└── 06_final_morgan_bit_figures.py
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

Run the workflow sequentially:

```bash
python src/01_download_data.py
python src/02_generate_descriptors.py
python src/03_generate_morgan.py
python src/04_model_comparison.py
python src/05_visualize_key_morgan_bits.py
python src/06_final_morgan_bit_figures.py
```

The repository contains generated intermediate datasets, analysis tables, predictions, and figures so that the workflow can also be inspected without rerunning every step.

---

# Repository Structure

```text
admet-drug-discovery-ml/
│
├── data/
│   ├── raw/
│   │   └── caco2_wang.csv
│   └── processed/
│       ├── caco2_rdkit_features.csv
│       ├── caco2_morgan_fingerprints.csv
│       └── ...
│
├── figures/
│   ├── caco2_5fold_cv_r2.png
│   ├── caco2_model_representation_comparison.png
│   ├── caco2_oof_predicted_vs_experimental.png
│   ├── caco2_oof_residuals.png
│   ├── caco2_shap_summary.png
│   ├── caco2_shap_feature_importance.png
│   └── caco2_shap_HBD_dependence.png
│
├── results/
│   ├── caco2_model_comparison.csv
│   ├── caco2_combined_oof_predictions.csv
│   ├── morgan_bit_analysis/
│   └── morgan_bit_visualizations/
│
├── src/
│   ├── 01_download_data.py
│   ├── 02_generate_descriptors.py
│   ├── 03_generate_morgan.py
│   ├── 04_model_comparison.py
│   ├── 05_visualize_key_morgan_bits.py
│   └── 06_final_morgan_bit_figures.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Scientific Limitations

Several limitations should be considered when interpreting the results.

1. **Caco-2 permeability is an in-vitro endpoint** and does not represent the complete biological process of human intestinal absorption.

2. **Fingerprint bits are computational representations.** A Morgan bit should not automatically be interpreted as a unique biological mechanism.

3. **Statistical association is not causation.** Significant fingerprint associations identify patterns in the dataset but do not establish mechanistic causality.

4. **Fingerprint environments may occur in multiple chemical contexts.** A single bit does not necessarily correspond to one unique chemical structure.

5. **Cross-validation and OOF predictions are preferable to relying on a single train/test split**, but they do not replace independent external validation.

6. **External validation is still required** to establish generalization to genuinely unseen chemical space.

7. **Random Forest predictions are model-dependent.** Different algorithms or representations may identify different important features.

---

# Future Work

The next development stages will focus on improving both predictive robustness and chemical interpretation.

### Validation

* scaffold-based cross-validation
* independent external validation
* applicability-domain analysis
* uncertainty estimation

### Modeling

* gradient-boosting models
* XGBoost/LightGBM comparison
* additional descriptor families
* graph-based molecular representations
* ensemble modeling

### Chemical interpretation

* systematic analysis of additional Morgan environments
* chemical-space visualization
* scaffold-level interpretation
* structure–permeability relationship analysis
* uncertainty-aware molecular interpretation

### ADMET expansion

The workflow can subsequently be extended to additional ADMET endpoints, enabling construction of a broader interpretable ADMET modeling framework.

---

# Conclusion

This project demonstrates an interpretable machine-learning workflow for Caco-2 permeability prediction that integrates **cheminformatics, machine learning, statistical analysis, explainable AI, and molecular visualization**.

The combined RDKit descriptor + Morgan fingerprint representation achieved the strongest 5-fold cross-validation performance:

**R² = 0.7455 ± 0.0258**

with:

**RMSE = 0.3895 ± 0.0217**

and:

**MAE = 0.3005 ± 0.0148**

Pooled out-of-fold predictions across 910 molecules produced:

**R² = 0.7230**

**RMSE = 0.4089**

**MAE = 0.3177**

Beyond prediction, SHAP analysis provides a global feature-level interpretation, while Morgan fingerprint analysis connects statistically important local structural environments to explicit molecular structures.

The resulting workflow therefore moves from:

> **Prediction → Explanation → Statistical validation → Chemical interpretation**

rather than treating machine learning as a black-box prediction exercise.

---

## Research Positioning

This repository represents a computational drug-discovery project at the intersection of:

**Computational Chemistry × Cheminformatics × Machine Learning × Explainable AI × ADMET**

It is designed as a reproducible research artifact and as a foundation for future work in interpretable molecular property prediction.

---

## Author

**Moneeba Asghar**

MS Chemistry | Computational Chemistry | Machine Learning for Molecular Science

Research interests:

* Computational Chemistry
* Cheminformatics
* Molecular Machine Learning
* ADMET Prediction
* Explainable AI
* Drug Discovery
* Molecular Design

---

## Citation

If you use this workflow or repository in academic work, please cite the repository:

```text
Asghar, M. Interpretable Machine Learning for Caco-2 Permeability Prediction.
GitHub repository: Moneebaasghar/admet-drug-discovery-ml.
```

---

## Acknowledgements

The project uses the Caco2_Wang dataset distributed through the Therapeutics Data Commons and cheminformatics functionality provided by RDKit.

