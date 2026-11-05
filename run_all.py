"""Execute the research notebooks in dependency order, saving genuine Jupyter outputs."""
import argparse
from pathlib import Path
import os
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
NAMES = sorted((ROOT / "notebooks").glob("[0-9][0-9]_*.ipynb"))
WORKBOOK = "Base_Observatorio_conflictos_2005-2024_v1.xlsx"
MANUALS = ("User_Manual_OC_Dataset_ 2009_2019.pdf", "Manual_Usuario_OCS_2020.pdf")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path,
                        help="COES workbook (default: data_local/raw/ or PROTEST_RAW)")
    parser.add_argument("--only", choices=[f"{i:02}" for i in range(1, 9)], nargs="+",
                        help="Notebook numbers; earlier result files must already exist.")
    parser.add_argument("--kernel", default="python3", help="Installed Jupyter kernel name")
    parser.add_argument("--timeout", type=int, default=21600, help="Timeout in seconds per cell")
    args = parser.parse_args()
    selected = args.only or [f"{i:02}" for i in range(1, 9)]
    notebooks = [p for p in NAMES if p.name[:2] in selected]
    if len(notebooks) != len(set(selected)):
        parser.error("Missing notebook in notebooks/. Use a complete copy of this repository.")

    raw = args.raw or Path(os.environ.get("PROTEST_RAW", ROOT / "data_local" / "raw" / WORKBOOK))
    raw = raw.expanduser().resolve()
    if "01" in selected:
        missing = [p for p in (raw, *(raw.parent / n for n in MANUALS)) if not p.is_file()]
        if missing:
            parser.error("Download these files from COES (instructions in README.md): "
                         + ", ".join(p.name for p in missing))
    if "02" in selected and not (shutil.which("g++") or shutil.which("clang++")):
        parser.error("A C++17 compiler (g++ or clang++) is required for the independent sampler check.")
    os.environ["PROTEST_RAW"] = str(raw)
    os.environ["PROTEST_ROOT"] = str(ROOT)
    os.environ.pop("PROTEST_FROM_AGGREGATES", None)
    for var in ("OMP_NUM_THREADS", "NUMBA_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[var] = "2"
    from nbclient import NotebookClient
    import nbformat

    dest = ROOT / "executed"
    dest.mkdir(exist_ok=True)
    for source in notebooks:
        print(f"Executing {source.name}", flush=True)
        notebook = nbformat.read(source, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        client = NotebookClient(notebook, timeout=args.timeout, kernel_name=args.kernel,
                                resources={"metadata": {"path": str(source.parent)}})
        client.execute()
        target = dest / source.name
        with tempfile.NamedTemporaryFile(mode="w", dir=dest, suffix=".tmp", delete=False,
                                         encoding="utf-8") as handle:
            temporary = Path(handle.name)
            try:
                nbformat.write(notebook, handle)
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        temporary.replace(target)
        print(f"Saved {target.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
