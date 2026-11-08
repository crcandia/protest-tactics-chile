# Protest tactics in Chile, 2008–2024

Analysis code for the manuscript *Tactic frequencies shifted while patterns of co-occurrence persisted in Chilean protests, 2008–2024* by Cristian Candia. The study analyses 27,488 protest actions reported by Chilean newspapers and coded by the COES Observatory of Conflicts. For each pair of tactics, it compares the number of actions that recorded both with reference models that preserve the frequency of each tactic and the number of tactics recorded per action.

This repository contains code only. It does not include the COES records or files derived from them. The COES terms of use do not permit transferring the materials to third parties, so each user downloads them from Harvard Dataverse.

## Contents

| Path | Content |
|---|---|
| `notebooks/` | Eight numbered Jupyter notebooks, saved with their outputs |
| `run_all.py` | Runs the notebooks in order and saves executed copies |
| `config/` | The analysis specification and its two dated amendments |
| `requirements.txt` | Python dependencies, tested with Python 3.12 |

## Data

Download three files from the COES *Observatory of Conflicts – Cumulative Dataset* on Harvard Dataverse, [version 9.0](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GKQXBR&version=9.0). On each file page select **Access File → Download**, accept the COES terms of use and complete the guestbook. Keep the original filenames and put the three files together in `data_local/raw/`.

| File | Use |
|---|---|
| `Base_Observatorio_conflictos_2005-2024_v1.xlsx` | Event workbook. Notebook 01 verifies its SHA-256 checksum, `24b1870f1098d233674d6489a2df9ce2ba4e2fc74140015e01c555976e37075c`. |
| `User_Manual_OC_Dataset_ 2009_2019.pdf` | First archived user manual, used to compare tactic definitions. The filename includes a space before “2009”. |
| `Manual_Usuario_OCS_2020.pdf` | Second archived user manual, used for the same comparison. |

## Run the analysis

Install a C++17 compiler (`g++` or `clang++`) for the independent sampler check. Then, from the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name protest-tactics --display-name "Protest tactics (Python)"
python run_all.py --kernel protest-tactics --raw data_local/raw/Base_Observatorio_conflictos_2005-2024_v1.xlsx
```

The runner executes notebooks 01–08 in order, writes the executed copies to `executed/` and creates local outputs in `data_local/` and `results/`. These folders are excluded from version control. A full run takes about six minutes on an 18-core computer. Use `--raw` to point to the workbook if the three downloaded files are stored elsewhere. Once the upstream results exist, `--only` reruns selected notebooks, for example `python run_all.py --kernel protest-tactics --only 06 07`. If your environment blocks Jupyter kernel sockets, add `--inprocess` to run a socket-free kernel in the active Python environment; the outputs are still saved as native Jupyter outputs.

| Notebook | Purpose |
|---|---|
| 01 | Verify the source workbook, reconstruct the study sample and compare the two manuals |
| 02 | Generate the six randomised references and check the sampler |
| 03 | Estimate pair-level and family-level structure over the study period |
| 04 | Estimate annual stability, sampling reliability and sensitivity |
| 05 | Fit the log-linear models and calibrate departures against within-year variability |
| 06 | Summarise robustness, list the largest pair residuals in the flagged years, compare change in tactic use with change in pairing between 2008–2018 and 2021–2024, and compute codebook-family ratios by year |
| 07 | Draw the four main and ten supplementary figures |
| 08 | Export the numbers, Table 1 and the supplementary LaTeX tables used in the manuscript to `results/manuscript/` |

## Analysis specification

`config/` holds the analysis specification and its two dated amendments, which record the decisions and terminology in force when the analyses were conducted. Columns named `frequency_share_*` hold the relative reductions in model discrepancy reported in the paper (residual deviance and dispersion-adjusted Pearson discrepancy).

## Data citation

Reproducible Research, Centre for Social Conflict and Cohesion Studies (COES). 2020. *Observatory of Conflicts – Cumulative Dataset*, version 9. Harvard Dataverse. https://doi.org/10.7910/DVN/GKQXBR
