# Protest tactics in Chile, 2008–2024

Code for *Tactic prevalence shifted while associations persisted in Chilean protests from 2008 to 2024* by Cristian Candia. The study follows 27,488 newspaper-reported protest actions. It separates changes in how often tactics appear from changes in which tactics accompany one another, using reference models that preserve tactic frequencies, list lengths and, in the primary specification, protest context and coding position.

## Repository

| Path | Purpose |
|---|---|
| `notebooks/` | Eight notebooks in execution order, with native tables and figures saved inline |
| `config/analysis.json` | Source checksum, sample definitions, reference specifications and resampling parameters |
| `run_all.py` | Execute notebooks in order using a fresh kernel for each one |
| `requirements.txt` | Python dependencies |

The notebooks contain the analysis code and explain the definitions, assumptions and calculations where they are used. Outputs displayed in the notebooks are generated during execution. Table and figure exports use the same objects that are displayed.

## Obtain the data

Download these three files from the COES *Observatory of Conflicts – Cumulative Dataset*, Harvard Dataverse [version 9.0](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GKQXBR&version=9.0). Accept the dataset terms and complete the download guestbook. Keep the original filenames together in `data_local/raw/`.

| File | Use |
|---|---|
| `Base_Observatorio_conflictos_2005-2024_v1.xlsx` | Original event workbook |
| `User_Manual_OC_Dataset_ 2009_2019.pdf` | Tactic definitions in the first manual; the filename includes a space before `2009` |
| `Manual_Usuario_OCS_2020.pdf` | Tactic definitions in the second manual |

Notebook 01 verifies the workbook SHA-256 checksum, `24b1870f1098d233674d6489a2df9ce2ba4e2fc74140015e01c555976e37075c`, and compares the tactic definitions between the manuals. The COES terms require each user to obtain the data directly. Original files and action-level or day-level intermediates stay local and are excluded from version control; the saved notebook outputs contain aggregates.

## Reproduce the paper

Use Python 3.12 and a C++17 compiler (`g++` or `clang++`) for the independent sampler comparison. From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name protest-tactics --display-name "Protest tactics (Python)"
python run_all.py --kernel protest-tactics --raw data_local/raw/Base_Observatorio_conflictos_2005-2024_v1.xlsx
```

The runner executes notebooks 01–08, stops on errors and saves newly executed copies in `executed/`. It creates `data_local/` for reconstructed records and day-level intermediates, and `results/` for aggregate calculations and manuscript exports. All three directories are ignored by Git. The first run computes all references and bootstrap samples; allow time for notebook 02's samplers and notebooks 04–06's resampling.

Use `--raw` with another workbook path if the downloaded files are stored elsewhere. To rerun selected steps after their inputs have been generated, use, for example:

```bash
python run_all.py --kernel protest-tactics --only 06 07 08
```

For environments that block local kernel sockets, `python run_all.py --inprocess` runs a fresh IPython kernel in the active Python environment for each notebook and preserves its native display outputs. The same `--raw` and `--only` options apply. Interactive execution also works from the repository root or the `notebooks/` directory; run all cells in order with the installed Python environment.

## Reading the analysis

| Notebook | Question and output |
|---|---|
| [01 — Data reconstruction](notebooks/01_data_reconstruction.ipynb) | Which records and tactic codes define the study sample? Reconstructs actions, sample counts and annual tactic frequencies. |
| [02 — Reference models](notebooks/02_null_models.ipynb) | How often would tactics co-occur given the preserved margins? Samples six specifications and checks constraints and mixing. |
| [03 — Full-period structure](notebooks/03_full_period_structure.ipynb) | Which pairs and families appear together more or less often than expected? Produces observed/expected counts, log ratios and global discrepancy. |
| [04 — Annual stability](notebooks/04_annual_stability.ipynb) | How consistently do associations recur across years? Compares annual and pooled patterns, support choices and sampling reliability. |
| [05 — Annual pair-count models](notebooks/05_loglinear_decomposition.ipynb) | How well does a common association pattern describe changing annual counts? Fits the log-linear models and calibrates annual departures against within-year variation. |
| [06 — Robustness and change](notebooks/06_robustness.ipynb) | How do changes in tactic use compare with changes in pairing? Summarises robustness, contrasts periods, estimates annual family ratios and describes the largest residuals. |
| [07 — Figures](notebooks/07_figures.ipynb) | Generates the four main and ten supplementary figures, together with their plotted data. |
| [08 — Manuscript tables](notebooks/08_manuscript_exports.ipynb) | Generates Table 1, Tables S1–S13 and numerical macros for LaTeX. |

The full-period, annual and model comparisons cover all 17 years, including 2019 and 2020. The pooled 2008–2018 versus 2021–2024 comparison puts changes in prevalence and association on a common multiplicative scale. Diagnostic resampling calculations reported in the SI are identified as diagnostics within notebooks 04–05; the annual departure test uses the within-year-calibrated F statistic.

Figures are written to `results/figures/`, their data to `results/figures/data/`, intermediate tables to `results/tables/`, and manuscript-ready LaTeX to `results/manuscript/`. The `fit_gain_deviance` column is `1 − D(M1)/D(MA)`; `fit_gain_dispersion_adjusted` uses Pearson discrepancies after subtracting the same within-year dispersion floor from both models. Both compare models with the same number of parameters.

## Data citation

Reproducible Research, Centre for Social Conflict and Cohesion Studies (COES). 2020. *Observatory of Conflicts – Cumulative Dataset*, version 9. Harvard Dataverse. https://doi.org/10.7910/DVN/GKQXBR
