# Protest tactics in Chile, 2008–2024

Analysis code for Cristian Candia’s manuscript *Tactic frequencies shifted while patterns of co-occurrence persisted in Chilean protests, 2008–2024*. The study analyses 27,488 protest actions recorded in Chilean newspapers. It compares observed pairs of tactics with reference models preserving the recorded tactic frequencies and the number of tactics per action.

## Read or verify the results

Open the eight numbered notebooks in `notebooks/` to inspect the analyses and their saved Jupyter outputs. Figure 4 can also be drawn from the published figure values in a fresh checkout. These commands use Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-verify.txt
python verify_targets.py
```

This writes Figure 4 as PDF, PNG and TIFF, together with `verification/checks.json`. The check compares each year’s plotted estimate and interval in panel (a) with the figure data and independently calculates the three raw and dispersion-adjusted comparisons in panel (b). Under N2, the two measures are a 71.24% relative reduction in deviance and a 95.94% relative reduction in dispersion-adjusted Pearson discrepancy.

To regenerate Supplementary Table S11 as well, supply a `results/` directory created by the full analysis or provided separately for peer review. This command runs only the S11 section of notebook 06 and the Figure 4 section of notebook 07, in an isolated working directory:

```bash
python verify_targets.py --results results --output verification-s11
```

The required private inputs are `aggregates/null_N2.npz` (annual draws and observed pair counts), `aggregates/eligible_primary.npy` (the eligible-pair mask), and `tables/annual_departure_F.csv` (the flagged years), all relative to the supplied `results/` folder. The checker compares all 64 regenerated rows with the rounded entries in published Supplementary Table S11. The public `published/` directory contains four small CSVs: the annual strength estimates and intervals, model discrepancies and denominators, tactic names, and the printed S11 rows.

## Reconstruct from the original data

Download the following three files from the COES *Observatory of Conflicts – Cumulative Dataset*, Harvard Dataverse, **version 9.0**. On each file page select **Access File → Download**, complete the guestbook and accept the COES conditions. Keep the original filenames and put the downloads together in `data_local/raw/`. [Version 9 dataset and access conditions](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/GKQXBR&version=9.0)

| File | Use |
|---|---|
| [Base_Observatorio_conflictos_2005-2024_v1.xlsx](https://dataverse.harvard.edu/file.xhtml?fileId=11982287&version=9.0) | Event workbook. Notebook 01 verifies SHA-256 `24b1870f1098d233674d6489a2df9ce2ba4e2fc74140015e01c555976e37075c`. |
| [User_Manual_OC_Dataset_ 2009_2019.pdf](https://dataverse.harvard.edu/file.xhtml?fileId=4625132&version=9.0) | First archived manual for the tactic-definition comparison. The filename includes a space before “2009”. |
| [Manual_Usuario_OCS_2020.pdf](https://dataverse.harvard.edu/file.xhtml?fileId=7099370&version=9.0) | Second archived manual for the same comparison. |

COES asks users to obtain the database directly from Dataverse, prohibits third-party transfer and commercial use of the database, and requires citation of the database and user guide. The workbook, manuals, event-level records, day-level extracts and simulation caches are kept outside this public repository.

Install a C++17 compiler (`g++` or `clang++`) for the independent sampler cross-check. From the repository root, using the same activated Python environment, run:

```bash
python -m pip install -r requirements.txt
python -m ipykernel install --user --name protest-tactics --display-name "Protest tactics (Python)"
python run_all.py --kernel protest-tactics --raw data_local/raw/Base_Observatorio_conflictos_2005-2024_v1.xlsx
```

The runner executes notebooks 01–08 in order in real Jupyter kernels, writes the executed copies to `executed/`, and creates local inputs and outputs beneath `data_local/` and `results/`. Pass another workbook path with `--raw` if the three downloaded files are together elsewhere. For a partial rerun use, for example, `python run_all.py --kernel protest-tactics --only 06 07` once the required upstream results have been produced. Open a notebook directly in Jupyter to change a cell and inspect its new inline output.

If your environment blocks Jupyter kernel sockets, use `python run_all.py --inprocess` with the same `--raw` or `--only` options. This mode runs a socket-free Jupyter kernel using the active Python environment and preserves native outputs.

| Notebook | Purpose |
|---|---|
| 01 | Verify the source workbook, reconstruct the study sample and check the two manuals. |
| 02 | Generate the six randomised references and check the sampler. |
| 03 | Estimate pair-level and family-level structure over the study period. |
| 04 | Estimate annual stability, sampling reliability and sensitivity. |
| 05 | Fit the log-linear models and calibrate departures with within-year variability. |
| 06 | Summarise robustness and identify the pairs printed in Table S11. |
| 07 | Generate the four manuscript figures and six supplementary figures. |
| 08 | Export the manuscript numbers and typeset tables to the local project. |

The original analysis specification and its two dated amendments are in `config/`. They preserve the decisions and terminology recorded when the analyses were conducted. Historical `frequency_share_*` column names refer to the relative model-fit measures defined above.

**Data citation.** Reproducible Research, Centre for Social Conflict and Cohesion Studies (COES), 2020. *Observatory of Conflicts – Cumulative Dataset*, version 9. Harvard Dataverse. [Dataset DOI](https://doi.org/10.7910/DVN/GKQXBR)
