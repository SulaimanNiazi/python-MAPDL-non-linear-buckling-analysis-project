# AI-Based Expert System for Critical Structural Analysis

This project is an AI-based expert system designed for critical structural analysis, specifically focusing on the buckling analysis of aircraft structures. The system takes user inputs for various parameters, generates an input file for analysis, and processes the results to determine critical buckling loads and probabilities of failure.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)

## Features

- **User Input**: Prompts the user for various parameters related to the aircraft structure.
- **Input File Generation**: Generates an `.inp` file for structural analysis based on user inputs.
- **Analysis Execution**: Waits for the analysis to complete and processes the results.
- **Error Handling**: Handles timeouts and errors during the analysis process.
- **Result Display**: Displays the critical buckling loads and probabilities of failure.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/structural-analysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd structural-analysis
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Python script:
```bash
python main.py
```

The program will prompt for the path of the para-geometry file and various dimensions and material properties of the aircraft's body. After providing the required inputs, the program will generate an `.inp` file and wait for the analysis to complete. Once the analysis is done, the results will be displayed.

## Requirements

- Python 3.7 or higher
- Required Python libraries (install using `requirements.txt`)

---

Feel free to reach out for collaboration or if you have any questions!