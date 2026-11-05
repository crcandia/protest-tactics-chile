"""Regenerate Figure 4 with published inputs and optionally S11 with local N2 results."""
import argparse
from contextlib import chdir, redirect_stdout
import csv
import io
import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
PUBLISHED = ROOT / "published"
S11_OUTPUT = "departure_pairs_flagged_years_N2"
S11_INPUTS = ("aggregates/eligible_primary.npy", "aggregates/null_N2.npz",
              "tables/annual_departure_F.csv")


def execute_section(prefix, index, marker):
    path, = (ROOT / "notebooks").glob(f"{prefix}_*.ipynb")
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    namespace = {"__name__": "__main__"}
    for i in (1, index):
        source = "".join(cells[i]["source"])
        if cells[i]["cell_type"] != "code" or (i == index and marker not in source):
            raise ValueError(f"The selected section moved in {path.name}; update the verifier.")
        # Keep console output concise when the notebook displays figures and tables.
        with redirect_stdout(io.StringIO()):
            exec(compile(source, f"{path.name}:cell{i}", "exec"), namespace)
    return namespace


def check_chart(axes):
    import numpy as np
    import pandas as pd
    fits = pd.read_csv(PUBLISHED / "fig4_fit.csv").set_index("reference").loc[
        ["N2", "N1", "N2_clean"]]
    raw = 100 * (1 - fits.D_M1 / fits.D_MA)
    floor = fits.pooled_dispersion_within * fits.df_residual_M1
    adjusted = 100 * (1 - (fits.X2_M1 - floor) / (fits.X2_MA - floor))
    np.testing.assert_allclose([s.get_width() for s in axes[1].patches[:3]], adjusted)
    np.testing.assert_allclose(axes[1].lines[0].get_xdata(), raw)
    if axes[1].get_xlabel() != "Relative reduction in model discrepancy (%)":
        raise ValueError("Figure 4(b) has an unexpected axis label.")
    phi = pd.read_csv(PUBLISHED / "fig4_phi.csv")
    for j, (ref, offset) in enumerate([("N2", -0.15), ("N1", 0.15)]):
        series = phi[phi.reference == ref]
        np.testing.assert_allclose(axes[0].lines[j].get_xdata(), series.year + offset)
        np.testing.assert_allclose(axes[0].lines[j].get_ydata(), series.phi)
        intervals = np.stack(axes[0].collections[j].get_segments())
        np.testing.assert_allclose(intervals[:, 0, 1], series.phi_lo)
        np.testing.assert_allclose(intervals[:, 1, 1], series.phi_hi)
    return {"raw_percent": raw.to_dict(), "dispersion_adjusted_percent": adjusted.to_dict()}


def check_s11(table_dir):
    import numpy as np
    import pandas as pd
    results = pd.read_csv(table_dir / f"{S11_OUTPUT}.csv")
    residuals = results.pearson_residual
    positive = results.direction.eq("more_than_common_structure")
    if not np.isfinite(residuals).all() or not (residuals[positive] > 0).all() or not (residuals[~positive] < 0).all():
        raise ValueError("Unexpected sign or nonfinite residual in S11.")
    with (PUBLISHED / "s11.csv").open(newline="", encoding="utf-8") as handle:
        expected = list(csv.reader(handle))[1:]
    actual = [[str(r.year), "more" if r.direction == "more_than_common_structure" else "fewer",
               f"{r.label_i} / {r.label_j}", str(r.observed), f"{r.predicted_common_structure:.1f}",
               f"{r.pearson_residual:.1f}"] for r in results.itertuples()]
    if len(actual) != 64 or actual != expected:
        raise ValueError("The regenerated S11 entries differ from the 64 printed rows.")
    return {"published_rows_reproduced": len(actual), "years": sorted(results.year.unique().tolist())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path,
                        help="Existing results/ from the full run or the private reviewer package; enables S11.")
    parser.add_argument("--output", type=Path, default=Path("verification"),
                        help="New output folder (must not already exist)")
    args = parser.parse_args()
    if args.results:
        missing = [name for name in S11_INPUTS if not (args.results / name).is_file()]
        if missing:
            parser.error("Missing S11 inputs inside --results: " + ", ".join(missing))
    out = args.output.resolve()
    if out.exists():
        parser.error(f"Output already exists: {out}. Give a new --output folder.")
    out.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=out.parent, prefix="check-protest-") as tmp:
        base = Path(tmp)
        os.environ.update(PROTEST_ROOT=str(base), MPLBACKEND="Agg",
                          MPLCONFIGDIR=str(base / "mpl-cache"))
        shutil.copytree(ROOT / "config", base / "config")
        notebooks = base / "notebooks"
        tables = base / "results" / "tables"
        tables.mkdir(parents=True)
        notebooks.mkdir()
        for src, dest in [("fig4_phi.csv", "unidiff_phi_by_year.csv"),
                          ("fig4_fit.csv", "loglinear_decomposition.csv"),
                          ("tactics.csv", "tactic_dictionary.csv")]:
            # If a full reconstruction is provided, test its figure inputs against the
            # published display. The reviewer cache also supports this path.
            original = args.results / "tables" / dest if args.results else None
            shutil.copyfile(original if original and original.is_file() else PUBLISHED / src,
                            tables / dest)
        checked = {}
        if args.results:
            for rel in S11_INPUTS:
                dest = base / "results" / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(args.results / rel, dest)
            with chdir(notebooks):
                execute_section("06", 7, "fit_M1")
            checked["S11"] = check_s11(tables)
        with chdir(notebooks):
            state = execute_section("07", 9, "unidiff_phi_by_year")
        checked["Figure4"] = check_chart(state["axes"])
        exports = base / "export"
        exports.mkdir()
        for kind in ("pdf", "png", "tiff"):
            shutil.copyfile(base / f"results/figures/Fig4.{kind}", exports / f"Fig4.{kind}")
        if args.results:
            for kind in ("csv", "tex"):
                name = f"{S11_OUTPUT}.{kind}"
                shutil.copyfile(tables / name, exports / name)
        (exports / "checks.json").write_text(json.dumps(checked, indent=2) + "\n", encoding="utf-8")
        exports.rename(out)
    print("Verified: " + ", ".join(checked) + f". Outputs: {out}")
    if not args.results:
        print("To regenerate S11 as well, supply local N2 inputs with --results; see README.md.")


if __name__ == "__main__":
    main()
