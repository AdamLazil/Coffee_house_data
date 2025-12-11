# ☕ Retail Data Extraction & Analysis for a Closed Coffe House

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)]()
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blue?logo=pandas)]()
[![PDF Processing](https://img.shields.io/badge/PDF-Parsing-orange?logo=adobeacrobatreader)]()
[![Status](https://img.shields.io/badge/Status-In_Progress-yellow)]()
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-lightgrey?logo=postgresql)]()

---

## 📌 Project Overview

This project focuses on **retail analysis for a café that has already been closed**, using **real historical data**.  
The dataset is fragmented, unstructured, and stored in formats that **cannot be downloaded or processed in bulk**, which requires building automated tools for extraction and cleaning.

The final goal is to build a **repeatable ETL pipeline** that processes all available data and prepares it for deeper financial and retail analytics.

---

## 🚀 Main Objectives

### **1. Bulk Email Data Extraction**

The core data exists **only inside email messages**, and the provider does not allow bulk export.  
➡️ We develop a Python script using

- `imapclient`
- `email` module

to automatically fetch and store all relevant files.

---

### **2. Automated PDF Parsing**

All business records (daily sales, product groups, rastr data, etc.) are provided **only in PDF format**.

➡️ We build a dedicated parser to extract structured information such as:

- product categories
- daily revenue
- rastr breakdown
- item-level statistics
- dates and metadata

---

...
