"""
===============================================================================
SMBNA Figures - Architecture Diagram Generator
===============================================================================

DESCRIPTION
-----------
Generates Figure 1: System architecture diagram showing the flow from sensors
through belief engines, invariant scoring, trust arbitration, to final output.
Uses Graphviz to create publication-ready architecture diagrams.

USAGE
-----
    from smbna.figures.figure1_architecture import generate_architecture
    
    generate_architecture()
    # Generates figure1_architecture.pdf

OUTPUT
------
PDF file: figure1_architecture.pdf
Shows: Sensors → Belief Engines → Invariant Scoring → Trust Arbitration → Output

DEPENDENCIES
------------
- graphviz

AUTHOR
------
MoniGarr
GitHub: https://github.com/monigarr/SMBNA

VERSION
-------
1.0.0
===============================================================================
"""

from graphviz import Digraph

def generate_architecture():
    dot = Digraph()

    dot.node("S", "Sensors")
    dot.node("B", "Belief Engines")
    dot.node("I", "Invariant Scoring")
    dot.node("T", "Trust Arbitration")
    dot.node("O", "Pose | Confidence | NAV_UNSAFE")

    dot.edges([("S","B"), ("B","I"), ("I","T"), ("T","O")])

    dot.render("figure1_architecture", format="pdf")
