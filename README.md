# Geophysics Data Visualization & Analysis Suite

An interactive desktop application built with Python and PyQt5 for visualizing and analyzing geophysical data. The project integrates tools for geostatistics, seismic analysis, thermodynamics, and atmospheric physics into a single, modular interface.

![Main Interface Placeholder](image.png)

## Key Features

### 1. Geostatistics
*   **Variogram Analysis:** Calculation and visualization of experimental variograms using the `scikit-gstat` library.
*   **Interpolation:** Implementation of kriging methods and data simulation.
*   **Interactivity:** Dynamic modeling parameter adjustments via sliders with real-time plot updates.

### 2. Seismic Analysis
*   **Reflectivity Modeling:** Synthesis of seismograms based on velocity, density, and quality factor (Q-factor) parameters.
*   **Physical Factor Modeling:** Simulation of multiples, absorption, and geometric spreading.
*   **Signal Processing:** Application of Wiener deconvolution to recover the impulse response of the medium.

### 3. Thermodynamics Modeling
*   **2D Heat Equation:** Solving the non-stationary heat equation in heterogeneous media.
*   **Multithreaded Calculations:** Offloading heavy numerical computations to a separate thread (`QThread`) to maintain UI responsiveness.
*   **Visualization:** Animated 2D temperature distribution maps with dynamic grid resizing.

### 4. Atmospheric Physics
*   **Skew-T Log-P Diagrams:** Visualization of upper-air data using the `MetPy` library.
*   **Analytical Isolines:** Interactive plotting of dry and moist adiabats, saturation mixing ratio lines, and isotherms.
*   **Line Manager:** A user-friendly interface to manage and toggle multiple analytical curves on the chart.

## Technology Stack

*   **GUI:** PyQt5 (modular Mixin-based architecture, styled with QSS).
*   **Scientific Computing:** NumPy, SciPy, Pandas, Scikit-learn.
*   **Specialized Libraries:** `metpy` (meteorology), `scikit-gstat` (geostatistics).
*   **Visualization:** Matplotlib (integrated into PyQt5 with custom canvas update decorators).

## Implementation Highlights

*   **Modularity:** Built on a mixin pattern, allowing for easy expansion with new scientific modules without modifying the core logic.
*   **Canvas Decorators:** Utilizes a custom `@PlotInterface.canvasDraw` decorator for automated plot lifecycle management.
*   **UX/UI:** Dark theme support and a responsive interface that adapts to window resizing.
*   **Performance:** Vectorized NumPy operations for high-speed computations.

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/GAGvozdik/PlotInterface.git
   cd PlotInterface/
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux/macOS
   # or
   venv\Scripts\activate     # for Windows
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python mainApp.py
   ```

---
*Developed for educational and research purposes in the field of geophysics.*
