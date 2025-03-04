# Password Strength Analyzer

This is currently a locally hosted tool that can be used to verify the strength of any password. The passwords entered are only saved for the session in which the tool is used and are immediately erased from memory for privacy purposes.

## Reasoning:

We live in an era where internet privacy is not as enforced as it should be. I frequently see reports and threads (on Reddit/X) where users mention that their online gaming, professional, and even school accounts have fallen prey to malicious actors. It is often discovered that they had weak, suggested, or self-created passwords. Additionally, society is regressing to a mindset where many people no longer care about their online security (e.g., "Companies and bad actors already have my information" or "If you use these apps/services, your personal information is already owned by someone else").

I'm working on streamlining the process so that future iterations require less effort from the user.

The next iteration of this tool is to create a .dmg/.exe file to develop an application with the exact same functionality.

# Setup & Execution Guide

## Step 1: Clone the Repository
To get the latest version of the project, clone the GitHub repository to your local machine.

```bash
git clone https://github.com/ks6573/PSA.git
cd PSA
```
This will download the repository and navigate into the project directory.

---

## Step 2: Set Up a Virtual Environment (Recommended)
A virtual environment helps to isolate dependencies and prevent conflicts with system-wide packages.

```bash
python -m venv venv
```

To activate the virtual environment:
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

---

## Step 3: Install Dependencies
Install all required packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, manually install dependencies:

```bash
pip install pandas scikit-learn joblib tkinter
```

This ensures that all necessary Python packages are installed.

---

## Step 4: Train the Machine Learning Model
Before using the password strength checker, train the machine learning model to make predictions.

```bash
python Password_Checker_Training.py
```

This script:
- Loads `dataset.csv`
- Extracts password features such as length, entropy, and character diversity
- Trains a **Random Forest Classifier**
- Saves the trained model as `rf_model.pkl` and the label encoder as `label_encoder.pkl` in the `data/` directory

Ensure `rf_model.pkl` and `label_encoder.pkl` exist in `data/` before proceeding to the next step.

---

## Step 5: Run the Password Strength Checker GUI
Once the model is trained, launch the GUI application to analyze password strength.

```bash
python Password_Checker.py
```

This script:
- Loads the trained model (`rf_model.pkl`)
- Accepts user password input
- Predicts password strength using machine learning
- Displays results in a GUI window

---

## Keeping Your Project Up to Date
To ensure you have the latest updates from the repository, run:

```bash
git pull origin main
```

Replace `main` with the correct branch name if necessary.

If new dependencies are added, update them with:

```bash
pip install -r requirements.txt
```

Now your project is fully set up and ready to use.

If you encounter any issues, double-check the steps above or reach out for further assistance.


