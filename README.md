# 🎵 Music Recommendation Tool Using Cosine Similarity

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://semver.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A graphical user interface (GUI) application built in Python to recommend songs based on the cosine similarity between a user-input text sample and data from a music dataset.

> Project using `TF-IDF`, `cosine_similarity`, `NLTK`, and `CustomTkinter`.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)](https://numpy.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge\&logo=scikit-learn\&logoColor=white)](https://scikit-learn.org/)
[![NLTK](https://img.shields.io/badge/NLTK-4B8BBE?style=for-the-badge\&logo=python\&logoColor=white)](https://www.nltk.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-FFCC00?style=for-the-badge\&logo=python\&logoColor=black)](https://docs.python.org/3/library/tkinter.html)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-4CAF50?style=for-the-badge\&logo=python\&logoColor=white)](https://github.com/TomSchimansky/CustomTkinter)

---

## 📋 Table of Contents

* [💡 Overview](#💡-overview)
* [🧠 Technologies Used](#🧠-technologies-used)
* [⚙️ Installation](#⚙️-installation)
* [🚀 How to Use](#🚀-how-to-use)
* [📌 Features](#📌-features)
* [📁 Folder Structure](#📁-folder-structure)
* [📄 License](#📄-license)

---

## 💡 Overview

This application allows the user to input a text sample and find the 5 most similar songs based on the dataset descriptions, using **TF-IDF** + **Cosine Similarity**.

The tool loads a CSV file (`Songs.csv`) containing information such as title and artist, and allows selecting specific columns to compare against the provided input.

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** You can generate the `requirements.txt` with:
>
> ```bash
> pip freeze > requirements.txt
> ```

4. Run the application:

```bash
python your_script_name.py
```

---

## 🚀 How to Use

1. On app start, select the **CSV column** to analyze.
2. Enter your **text sample** in the input box.
3. Click **"Calculate"** to generate recommendations.
4. The tool will display the 5 most similar songs with similarity percentages and angles.

---

## 📌 Features

* Automatic reading of the dataset (`Songs.csv`)
* Dynamic selection of columns for analysis
* Modern interface using **CustomTkinter**
* Similarity calculation using **TF-IDF + cosine\_similarity**
* Displays the 5 songs most similar to the input sample
* Indicator showing the total number of elements analyzed

---

## 📁 Folder Structure

```bash
Music-Recommendation-Tool/
│
├── DataFrame/
│   └── Songs.csv                # Music dataset
│
├── img/
│   └── favicon.ico              # Application icon
│
├── main.py                     # Main file with application logic
├── README.md                   # This file
└── requirements.txt            # Python dependencies (optional)
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
