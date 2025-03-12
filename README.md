# Mortgage Calculator with Prepayment Options

## Overview

This project is a Python-based mortgage calculator that computes monthly mortgage payments, generates a detailed amortization schedule, and allows users to incorporate prepayment options. The application supports both standard fixed-rate calculations and advanced scenarios where extra payments are applied—customizable either as a set schedule or calculated to achieve a desired payoff time. Mortgage details and prepayment configurations are persisted in JSON files, making it easier to reuse previously entered information.

## Features

- **Mortgage Payment Calculation:**  
  Uses the standard amortization formula to compute monthly payments.

- **Amortization Schedule:**  
  Generates a detailed month-by-month breakdown of interest, principal, and remaining balance.

- **Prepayment Options:**  
  - **Custom Prepayment Schedule:** Allows users to specify a lump-sum extra payment, its starting month, frequency, and number of intervals (with an option for "indefinite" prepayments until the loan is paid off).
  - **Target Payoff Calculation:** Computes the extra payment required to achieve a user-specified loan payoff time.
  
- **Data Persistence:**  
  Mortgage details and prepayment details are saved as JSON files in a top-level `data/` directory. Users can choose to reuse or redefine these details in subsequent runs.

- **Interactive User Prompts:**  
  The application uses interactive input prompts for data entry. (A CLI mode was explored but the current version is fully interactive.)

- **Unit Testing:**  
  Comprehensive tests are provided for mortgage calculations, mortgage details input, and prepayment functionality.

## Project Structure

- **data/ Directory:**
  Stores JSON files with mortgage and prepayment details. Keeping these files in a top-level folder separates non-code assets from your source code.

- **src/ Directory:**
  Contains all the application code. The code is organized into packages:
  - **The mortgage/ package holds the calculator and prepayment logic.**
  - **The utils/ package includes helper functions, such as those for loading/saving mortgage details.**

- **tests/ Directory:**
  Contains all unit tests to verify functionality.

- **.gitignore:**
  At the project root, this file prevents IDE-specific files (like workspace.xml) and other local files from being tracked.