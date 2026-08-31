# Morgan Fingerprint Interpretation

The model interpretation was extended beyond global molecular descriptors to investigate **local molecular environments encoded by Morgan fingerprints**.

Morgan fingerprints represent molecules as collections of atom-centered environments. Each fingerprint bit therefore represents a recurring structural environment generated from an atom and its surrounding neighborhood at a defined radius.

Because a fingerprint bit can occur in multiple molecules, and may occur at different structural contexts, the analysis treats fingerprint bits as **recurring molecular environments rather than unique chemical structures**.

---

## Selection of Morgan Fingerprint Features

Candidate fingerprint bits were evaluated using multiple complementary criteria:

* Random Forest feature importance
* Number of molecules containing the fingerprint bit
* Group-wise target comparison
* Incremental model performance
* Chemical-environment decoding

This multi-criterion analysis was used to identify fingerprint environments that were sufficiently represented in the dataset and potentially informative for model prediction.

The processed Morgan analysis files are available in:

```text
data/processed/morgan_incremental_r2.csv
data/processed/morgan_top_bits_summary.csv
data/processed/morgan_top_bits_decoded.csv
```

The final interpretation tables are available in:

```text
results/morgan_bit_analysis/final_morgan_interpretability_table.csv
results/morgan_bit_analysis/final_morgan_chemical_environments.csv
```

---

## Morgan Fingerprint Interpretability

![Morgan fingerprint interpretability](results/morgan_bit_analysis/morgan_interpretability_figure.png)

The Morgan fingerprint analysis provides a **local structural interpretation layer** that complements the global molecular-property interpretation obtained from SHAP.

The analysis connects:

```text
Morgan Fingerprint Bit
        ↓
Atom-Centered Environment
        ↓
Molecular Structure
        ↓
Model Importance / Association
        ↓
Chemical Interpretation
```

---

# Highlighted Morgan Fingerprint Environments

Four fingerprint bits were selected for detailed structural interpretation:

* **Bit 623**
* **Bit 82**
* **Bit 1290**
* **Bit 550**

The corresponding molecular environments were decoded using RDKit.

The decoded results show that these bits occur across multiple compounds rather than representing a single universal chemical structure.

---

## Bit 623

Bit 623 is observed across a diverse set of compounds and structural contexts.

Examples in the decoded dataset include **creatinine, metolazone, PNU-series compounds, amiloride, several neolignans, rhodamine 123, and other molecules**.

The bit occurs at different atom-centered environments, including radius 0, radius 1, and radius 2.

This diversity indicates that Bit 623 should be interpreted as a **recurring fingerprint environment encoded by the Morgan algorithm**, rather than as one specific functional group.

### Representative environment

![Morgan Bit 623](results/morgan_bit_visualizations/morgan_bit_623_EXACT.png)

The exact RDKit visualization highlights the atom-centered environment corresponding to the selected Bit 623 example.

---

## Bit 82

Bit 82 is also observed across multiple molecules.

Examples include **PNU-series compounds, digoxin, and several related permeability-model compounds**.

In the decoded dataset, Bit 82 is frequently represented at **radius 2**, indicating that the fingerprint environment incorporates a broader local neighborhood than a radius-0 atom feature.

### Representative environment

![Morgan Bit 82](results/morgan_bit_visualizations/morgan_bit_82_EXACT.png)

The visualization maps the numerical fingerprint bit to its corresponding atom-centered molecular environment.

---

## Bit 1290

Bit 1290 occurs across several structurally diverse compounds, including **pravastatin, atorvastatin, fluvastatin, saquinavir, biotin-saquinavir, peptide-like compounds, and other molecules**.

Many occurrences are encoded at **radius 1**, representing an atom-centered environment involving the immediate neighboring atoms.

### Representative environment

![Morgan Bit 1290](results/morgan_bit_visualizations/morgan_bit_1290_EXACT.png)

The visualization provides a structural representation of the selected Bit 1290 environment.

---

## Bit 550

Bit 550 is observed repeatedly in several chemically distinct molecules.

Examples include **echinacoside, digoxin, ouabain, epimedin A/B, icariin, quercitrin, naringin, doxorubicin, daunorubicin, and other compounds**.

A substantial number of the decoded occurrences correspond to **radius-2 environments**, capturing larger local structural neighborhoods.

### Representative environment

![Morgan Bit 550](results/morgan_bit_visualizations/morgan_bit_550_EXACT.png)

The visualization provides a structural representation of the selected Bit 550 environment.

---

# Four-Panel Morgan Environment Visualization

![Key Morgan environments](results/morgan_bit_visualizations/key_morgan_environments_4panel.png)

The four-panel visualization provides a compact comparison of the selected Morgan fingerprint environments.

This representation makes it possible to move from abstract fingerprint identifiers to visually interpretable molecular environments.

---

# Chemical Interpretation

The Morgan analysis demonstrates that machine-learning models can use information from **local molecular structure** in addition to global physicochemical descriptors.

However, the fingerprint results should be interpreted carefully.

A Morgan bit does not necessarily correspond to one unique functional group or one unique chemical effect. The same bit may occur in different molecules and structural contexts because Morgan fingerprints encode atom-centered environments algorithmically.

Therefore:

> **An important Morgan bit represents a recurring structural environment associated with model behavior, rather than a single causal chemical motif.**

The observed association may also reflect correlated molecular properties such as:

* Molecular size
* Lipophilicity
* Hydrogen-bonding capacity
* Polarity
* Molecular flexibility
* Aromaticity
* Overall scaffold structure

Consequently, Morgan fingerprint analysis is best used to generate **chemically interpretable hypotheses** rather than causal conclusions.

---

# Global and Local Interpretability

The project combines two complementary explainability approaches.

| Interpretation level | Method              | Information provided                                |
| -------------------- | ------------------- | --------------------------------------------------- |
| Global               | RDKit descriptors   | Overall molecular properties                        |
| Global               | SHAP                | Magnitude and direction of descriptor contributions |
| Local                | Morgan fingerprints | Recurring atom-centered molecular environments      |
| Structural           | RDKit visualization | Visual interpretation of selected environments      |

This combination allows the model to be investigated from both a **physicochemical** and a **structural** perspective.

---

# Interpretation Summary

The overall interpretation framework can therefore be summarized as:

```text
                         Caco-2 ML Model
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
        Molecular Descriptors          Morgan Fingerprints
                 │                             │
                 ▼                             ▼
              SHAP                     Fingerprint Analysis
                 │                             │
                 ▼                             ▼
      Global Property Effects        Local Structural Environments
                 │                             │
                 └──────────────┬──────────────┘
                                ▼
                    Chemical Interpretation
```

The two approaches provide complementary information: SHAP helps explain **which molecular properties influence predictions**, while Morgan analysis helps identify **recurring local structural environments used by the model**.
---

# Scaffold-Based Validation

Random cross-validation can provide optimistic estimates when structurally similar molecules are distributed across both training and validation folds. To evaluate whether the model can generalize to chemically distinct molecular scaffolds, an additional scaffold-based validation was performed.

The dataset contained:

* **910 molecules**
* **488 unique molecular scaffolds**
* **390 training scaffolds**
* **98 validation scaffolds**
* **676 training molecules**
* **234 validation molecules**
* **0 scaffold overlap between training and validation sets**
* **0 invalid molecular structures**

The scaffold leakage check passed, confirming that no molecular scaffold was shared between the training and validation sets.

The combined descriptor + Morgan representation was evaluated using a Random Forest model on the scaffold-based split.

| Metric        | Scaffold Validation |
| ------------- | ------------------: |
| R²            |          **0.6381** |
| RMSE          |          **0.4404** |
| MAE           |          **0.3466** |
| Residual Mean |             -0.0563 |
| Residual Std  |              0.4368 |

## Comparison with Random Cross-Validation

The scaffold-based validation performance was compared with the previously obtained random 5-fold cross-validation results.

| Evaluation             |                  R² |                RMSE |                 MAE |
| ---------------------- | ------------------: | ------------------: | ------------------: |
| Random 5-fold CV       | **0.7455 ± 0.0258** | **0.3895 ± 0.0217** | **0.3005 ± 0.0148** |
| Out-of-fold prediction |          **0.7230** |          **0.4089** |          **0.3177** |
| Scaffold validation    |          **0.6381** |          **0.4404** |          **0.3466** |

The reduction in R² from random cross-validation (**0.7455**) to scaffold validation (**0.6381**) indicates that prediction becomes more challenging when the model is evaluated on molecules containing scaffolds that were not represented during training.

This difference demonstrates why scaffold-aware validation is important for molecular machine-learning models. Random splitting can place chemically related molecules in both training and validation sets, whereas scaffold splitting provides a more stringent assessment of generalization to structurally distinct chemistry.

Despite the reduction in performance, the model retains meaningful predictive ability on unseen scaffolds, with a scaffold-validation **R² of 0.6381**.

Therefore, the model demonstrates useful predictive performance within the chemical space represented by the dataset, while predictions for substantially novel molecular scaffolds should be interpreted with greater caution.

The scaffold-validation result is available in:

```text
results/caco2_scaffold_validation.csv
```

The validation procedure is implemented in:

```text
src/07_scaffold_validation.py
```

---

# Reproducibility

The complete analysis pipeline is organized into sequential scripts:

```text
src/
├── 01_download_data.py
├── 02_generate_descriptors.py
├── 03_generate_morgan.py
├── 04_model_comparison.py
├── 05_visualize_key_morgan_bits.py
├── 06_final_morgan_bit_figures.py
└── 07_scaffold_validation.py
```

The project uses a reproducible Python environment with the required dependencies specified in:

```text
requirements.txt
```

The principal workflow is:

```text
Caco-2 Dataset
      │
      ▼
RDKit Molecular Descriptors
      │
      ├───────────────┐
      │               │
      ▼               ▼
Morgan Fingerprints   Descriptor Features
      │               │
      └───────┬───────┘
              ▼
      Random Forest Models
              │
              ▼
       Model Comparison
              │
       ┌──────┴──────┐
       ▼             ▼
   Random CV     Scaffold Validation
       │             │
       └──────┬──────┘
              ▼
       Model Interpretation
       ┌──────┴──────┐
       ▼             ▼
      SHAP      Morgan Analysis
       │             │
       └──────┬──────┘
              ▼
     Chemical Interpretation
```

---

# Limitations

Several limitations should be considered when interpreting the results.

1. The dataset contains **910 molecules**, which limits the chemical diversity available for model development.
2. Random Forest performance depends on the molecular representations supplied to the model.
3. Random cross-validation may provide more optimistic estimates when related chemical structures occur across folds.
4. Scaffold validation produced lower performance than random cross-validation, indicating reduced generalization to unseen scaffolds.
5. Morgan fingerprint bits represent algorithmically generated atom-centered environments and should not automatically be interpreted as unique functional groups.
6. Feature importance and SHAP associations do not establish causal relationships between molecular properties and Caco-2 permeability.
7. The model is intended for research and hypothesis generation rather than direct experimental or clinical decision-making.

---

# Conclusion

This project developed a reproducible machine-learning workflow for predicting **Caco-2 permeability** from molecular structure.

Three molecular representations were evaluated:

* RDKit physicochemical descriptors
* Morgan fingerprints
* Combined RDKit descriptors + Morgan fingerprints

The combined representation produced the strongest random 5-fold cross-validation performance:

**R² = 0.7455 ± 0.0258**

with:

**RMSE = 0.3895 ± 0.0217**

and:

**MAE = 0.3005 ± 0.0148**.

Out-of-fold evaluation across all 910 molecules produced:

**R² = 0.7230**

**RMSE = 0.4089**

**MAE = 0.3177**

A more stringent scaffold-based validation produced:

**R² = 0.6381**

**RMSE = 0.4404**

**MAE = 0.3466**

The reduction in performance under scaffold validation demonstrates that generalization to chemically novel molecular scaffolds remains more challenging than prediction under random splitting.

Model interpretation was performed using both **SHAP** and **Morgan fingerprint analysis**, providing complementary information about global physicochemical effects and recurring local structural environments.

Overall, the workflow demonstrates how molecular descriptors, structural fingerprints, rigorous validation, out-of-fold prediction, and explainability methods can be combined to develop a more transparent and reproducible ADMET machine-learning model.



