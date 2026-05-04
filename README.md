# Lumen Conscius (Experimental Prototype)

This repository contains a minimal reproducible implementation of the **Lumen Conscius** architecture, a computational model that explores the relationship between affective dynamics and an integration proxy (Φ̂).

## 🧠 Overview

The system simulates transitions between three cognitive regimes:

- Inconscious
- Pre-conscious
- Conscious (Ego)

These transitions are governed by the inequality:

(B - M) × C > L

Where:
- B = positive affective input
- M = negative affective input
- C = internal consciousness level
- L = threshold

An integration proxy (Φ̂) is computed to track system dynamics.

## ⚙️ Features

- Self-Organizing Map (SOM) with 707 affective states
- Dynamic simulation over time (30 timesteps)
- Integration proxy (Φ̂) varying with system state
- Automatic generation of:
  - Graph (`fig2_phi_moral.png`)
  - Console table of results

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt