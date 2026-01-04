# SMBNA  Secure Multi-Belief Navigation Arbitration

**Safe, explainable navigation for drones in GPS-degraded, GPS-denied and adversarial environments**

---

## Why this repository exists

Modern navigation systems fail in a dangerous way:  
they can become **confident while wrong**.

Accuracy alone is not sufficient when GPS jamming, spoofing, and signal degradation become routine (not exceptional). Autonomous systems must reason explicitly about **trust**, **consistency**, and **when to refuse**.

**SMBNA (Secure Multi-Belief Navigation Arbitration)** is a research-grade navigation framework that treats navigation as an *epistemic problem*, not a sensor problem.

> When the environment lies, the system must know it is being lied to.

---

## What SMBNA is

SMBNA is a **belief-centric navigation architecture** for uncrewed aerial vehicles operating in GPS-degraded or GPS-denied conditions.

Instead of early sensor fusion, SMBNA:
- Maintains **parallel navigation beliefs**
- Evaluates them using **invariant-based consistency checks**
- Dynamically arbitrates trust
- Emits explicit **NAV_UNSAFE** refusal signals when certainty collapses

This design prioritizes **safety, interpretability, and graceful degradation** over brittle accuracy.

---

## What SMBNA is *not*

- ❌ Not a new GPS signal  
- ❌ Not classified or restricted technology  
- ❌ Not a hardware or sensor replacement  
- ❌ Not an autonomy or flight-control stack  

SMBNA operates strictly at the **navigation reasoning layer** and is compatible with existing and future sensors, including quantum inertial and magnetic systems.

---

## Core idea (in one diagram)

Sensors
↓
Independent Belief Engines
↓
Invariant Scoring (plausibility, physics, coherence)
↓
Trust Arbitration
↓
Pose | Confidence | NAV_UNSAFE | Explanation


> Never fuse before you trust.

---

## Key principles

- **Beliefs before fusion**  
- **Refusal is a valid and desirable outcome**  
- **Explainability is structural, not post-hoc**  
- **Safety beats false confidence**  

If the system cannot navigate reliably, it should say that clearly and early.

---

## Architecture overview

### Belief Engines (parallel, independent)
- GPS-only belief
- Inertial (INS) belief
- Magnetic map-matching belief
- LEO ranging belief (optional)
- Dead-reckoning fallback

Each belief produces:
- State estimate
- Covariance
- Internal confidence

No belief consumes another belief’s output.

---

### Invariant Scoring Layer (core contribution)

Beliefs are evaluated using **representation-level invariants**, including:
- Temporal smoothness
- Cross-belief coherence
- Earth-field structural consistency
- Physics feasibility
- Covariance honesty

Invariant violations reduce trust *even when sensors appear confident*.

---

### Trust Arbitration & Safety

- Dynamic belief weighting
- Explicit confidence collapse detection
- Hard safety thresholds
- `NAV_UNSAFE` refusal signaling

Every decision includes a **machine-readable explanation**.

---

## Why this matters

Most navigation failures are not caused by noise, they are caused by **false certainty**.

SMBNA directly addresses this failure mode by reframing navigation as a problem of *epistemic discipline*: deciding which beliefs deserve trust, under uncertainty, in real time.

This makes SMBNA especially relevant for:
- GPS-contested environments
- Safety-critical autonomy
- Long-duration or remote operations
- Future hybrid classical + quantum navigation stacks

---

## Repository structure

smbna/
├── beliefs/ # Independent belief engines
├── invariants/ # Consistency and plausibility checks
├── arbitration/ # Trust & safety logic
├── baselines/ # EKF and classical comparators
├── simulation/ # GPS degradation & spoofing scenarios
├── visualization/ # Failure-focused dashboards
├── figures/ # Paper-ready figure generators
├── tests/ # Unit & scenario tests
└── scripts/ # Reproducible experiments


---

## Baselines included

For fair comparison, the repo includes:
- Classical EKF sensor fusion
- INS + GPS fallback
- Best-single-sensor strategies

These baselines intentionally **lack spoof detection or refusal**, highlighting SMBNA’s safety advantage.

---

## Running a simulation

```bash
python scripts/run_simulation.py --scenario spoofed_gps

Outputs include:
- Position error traces
- Belief trust timelines
- Invariant violation heatmaps
- Safety/refusal events
- Evaluation focus

Primary metrics:
- Position error under degradation
- Time-to-detect spoofing
- False confidence duration

Safety metrics:
- Correct NAV_UNSAFE triggering
- Late vs early refusal rates

## Research status

✔ Architecture complete

✔ Simulation-validated

✔ Baselines implemented

✔ Paper-ready figures

✔ Grant / proposal ready

This repository corresponds to a 3 page workshop paper and is intended as a foundation for further research, funding, or collaboration.

## Intended audience

- Robotics and autonomy researchers
- Safety-critical systems engineers
- Navigation and sensor-fusion practitioners
- Defense and civil autonomy programs
- AI safety and trustworthy systems researchers

## Author’s note

This project reflects a long-standing design philosophy:

- Robust systems know when they should not act.
- SMBNA is built for environments where certainty is rare, signals lie, and safety is a top priority.

## License & use

This project is released for research and evaluation purposes.
It contains no classified material and no restricted signal processing.

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for a detailed list of changes, updates, and version history.

## Contact / collaboration

If you are interested in the following, open an issue or reach out via the repository:

- extending SMBNA to new sensors
- formal safety guarantees
- hardware-in-the-loop validation
- grant or residency collaboration

Knowing when not to trust yourself is the first step toward trustworthy autonomy.


---

## Cite this work

If you use this framework, ideas, or code in academic work, please cite:

```bibtex
@misc{SMBNA2026,
  title        = {SMBNA: Secure Multi-Belief Navigation Arbitration for Safe Autonomous Systems},
  author       = {MoniGarr},
  year         = {2026},
  howpublished = {\url{https://github.com/monigarr/SMBNA}},
  note         = {Belief-centric navigation with invariant-based trust arbitration and explicit refusal under uncertainty}
}
