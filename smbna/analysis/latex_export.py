"""
===============================================================================
SMBNA Analysis - LaTeX Export Utilities
===============================================================================

DESCRIPTION
-----------
Exports analysis results to LaTeX table format for inclusion in papers and
reports. Formats DataFrames as publication-ready LaTeX tables with proper
formatting and styling.

USAGE
-----
    from smbna.analysis.latex_export import dataframe_to_latex
    from smbna.simulation.experiment_io import write_results
    
    df = write_results(rows, name="ablation_refusal")
    dataframe_to_latex(df, "ablation_refusal")
    # Generates results/latex/ablation_refusal.tex

OUTPUT
------
LaTeX .tex files in results/latex/ directory

DEPENDENCIES
------------
- pandas

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

import pandas as pd
from pathlib import Path


def dataframe_to_latex(
    df: pd.DataFrame,
    name: str,
    out_dir: str = "results/latex",
    float_fmt="%.2f"
):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    tex = df.to_latex(
        index=False,
        float_format=float_fmt,
        caption=name.replace("_", " ").title(),
        label=f"tab:{name}",
    )

    path = out / f"{name}.tex"
    path.write_text(tex)

    return path
