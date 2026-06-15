# Transition from Bouncing to Rolling on a Horizontal Surface

> **DGIST — Physics Group Project | Group 7**  
> Based on: *"Transition from bouncing to rolling on a horizontal surface"*  
> Rod Cross, American Journal of Physics **92**, 571–575 (2024)

---

## Overview

This project provides a step-by-step pedagogical reconstruction of Rod Cross's paper on the bounce-to-roll transition. We derive the key equations, analyze limiting cases, and verify the analytical model through a physical tennis ball experiment.

The central question: **why does a bouncing ball eventually transition into rolling — and when?**

---

## Repository Structure

```
├── 코드 실행.py                  # Main Python simulation & visualization
├── README.md                    # This file
└── PHYSICS_GROUP_PROJECT_REPORT.pdf   # Full project report
```

---

## Physics Summary

A rigid ball bouncing obliquely on a surface is governed by two coefficients of restitution:

| Symbol | Meaning |
|--------|---------|
| `e_y` | Normal (vertical) coefficient of restitution |
| `e_x` | Tangential (horizontal) coefficient of restitution |

The spin ratio `S = Rω / v_x` tracks how close the ball is to the rolling condition `S = 1`.  
After each bounce, S evolves via:

$$S_2 = \frac{(k - e_x)S_1 + (1 + e_x)}{(1 - ke_x) + k(1 + e_x)S_1}$$

Rolling is reached when `v_x = Rω`, i.e. `S = 1`.

---

## Experiment

A tennis ball was dropped from **1.10 m** above a tabletop and filmed with a smartphone.  
Bounce heights were extracted frame-by-frame.

| Bounce | Max Height (m) | e_y |
|--------|---------------|-----|
| 0 → 1 | 0.52 | 0.688 |
| 1 → 2 | 0.30 | 0.760 |
| 2 → 3 | 0.19 | 0.796 |
| 3 → 4 | 0.12 | 0.795 |
| 4 → 5 | 0.09 | 0.866 |
| 5 → 6 | 0.07 | 0.882 |
| 6 → 7 | 0.05 | 0.845 |

**Average e_y = 0.804**

| | Time (s) |
|---|---|
| Predicted rolling onset | 3.52 |
| Observed rolling onset | 3.14 |
| Relative error | 12.1% |

---

## Python Simulation

### Requirements

```bash
pip install numpy matplotlib
```

### Run

```bash
python "코드 실행.py"
```

### Output

The script produces three visualizations:

1. **Ball trajectory animation** — the ball bounces (blue) and transitions to rolling (green)
2. **Bounce height decay** — experimental data vs. theoretical curve `h_n = h_0 · e_y^(2n)`
3. **Predicted vs. experimental** rolling onset time bar chart

---

## Key Results

- The analytical model predicts rolling onset within **~12%** of the experimental value.
- The discrepancy is attributed to non-constant `e_y`, manual height estimation, and uncontrolled initial spin.
- The model confirms that **higher energy dissipation** (lower `e_y`) accelerates the bounce-to-roll transition.

---

## Group Members

| Student ID | Name |
|-----------|------|
| 202011056 | 김종진 |
| 202111039 | 김지아 |
| 202611032 | 김보영 |
| 202611200 | 정지연 |

**Instructor:** Dr. Devecioglu Deniz Olgu  
**Department:** DGIST  
**Date:** June 2026
