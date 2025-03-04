import tkinter as tk
from tkinter import ttk
import math
import joblib
import pandas as pd
import os

# Set the paths for model, encoder, and dataset
data_folder = "/Users/karan/PycharmProjects/Data"
model_path = os.path.join(data_folder, "rf_model.pkl")
encoder_path = os.path.join(data_folder, "label_encoder.pkl")
dataset_path = os.path.join(data_folder, "dataset.csv")

# Load the pre-trained model and label encoder
rf_model = joblib.load(model_path)
label_encoder = joblib.load(encoder_path)

# Feature engineering for password analysis
def calculate_character_diversity(password):
    char_sets = {
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'digits': '0123456789',
        'special': '!@#$%^&*()-_=+[]{}|;:,.<>?/~`'
    }
    diversity = {
        'lowercase': any(c in char_sets['lowercase'] for c in password),
        'uppercase': any(c in char_sets['uppercase'] for c in password),
        'digits': any(c in char_sets['digits'] for c in password),
        'special': any(c in char_sets['special'] for c in password)
    }
    return sum(diversity.values())

def calculate_entropy(password):
    char_set_size = 0
    char_sets = {
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'digits': '0123456789',
        'special': '!@#$%^&*()-_=+[]{}|;:,.<>?/~`'
    }
    if any(c in char_sets['lowercase'] for c in password):
        char_set_size += 26
    if any(c in char_sets['uppercase'] for c in password):
        char_set_size += 26
    if any(c in char_sets['digits'] for c in password):
        char_set_size += 10
    if any(c in char_sets['special'] for c in password):
        char_set_size += len(char_sets['special'])
    return len(password) * math.log2(char_set_size) if char_set_size > 0 else 0

# Main application class
class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Analyzer")
        self.geometry("550x300")

        # History storage
        self.history = []

        # Create notebook (tab view)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Add pages
        self.create_home_page()
        self.create_history_page()

    def create_home_page(self):
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Home")

        # Password entry
        ttk.Label(home_frame, text="Enter Password:").pack(pady=10)
        self.password_entry = ttk.Entry(home_frame, width=50)
        self.password_entry.pack(pady=5)

        # Analyze button
        analyze_button = ttk.Button(
            home_frame, text="Analyze Passwords", command=self.analyze_passwords
        )
        analyze_button.pack(pady=10)

        # Output display
        self.result_label = ttk.Label(home_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def create_history_page(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")

        # History table
        self.history_table = ttk.Treeview(
            history_frame, columns=("Password", "Strength"), show="headings", height=15
        )
        self.history_table.heading("Password", text="Password")
        self.history_table.heading("Strength", text="Strength")
        self.history_table.bind("<Double-1>", self.show_selected_password_details)
        self.history_table.pack(expand=True, fill='both', pady=10)

    def analyze_passwords(self):
        # Get password inputs
        passwords = self.password_entry.get().split(',')
        passwords = [p.strip() for p in passwords if p.strip()]

        if not passwords:
            self.result_label.config(text="Please enter at least one password.")
            return

        # Analyze each password
        for password in passwords:
            if len(password) < 6:
                self.history.append((password, "Too short", 0, 0))
                continue

            # Feature extraction
            entropy = calculate_entropy(password)
            char_diversity = calculate_character_diversity(password)
            password_length = len(password)

            # Prepare input for the model
            features = pd.DataFrame([[password_length, entropy, char_diversity]],
                                     columns=['length', 'entropy', 'char_diversity'])

            # Predict password strength
            strength_index = rf_model.predict(features)[0]
            strength_label = label_encoder.inverse_transform([strength_index])[0]

            # Save to history
            self.history.append((password, strength_label, entropy, char_diversity))

        # Update history table
        self.update_history_page()

        # Display success message
        self.result_label.config(text="Password analyzed and added to history.")

    def update_history_page(self):
        # Clear table
        for item in self.history_table.get_children():
            self.history_table.delete(item)

        # Add updated history
        for idx, (password, strength, _, _) in enumerate(self.history):
            self.history_table.insert("", "end", iid=idx, values=(password, strength))

    def show_selected_password_details(self, event):
        selected_item = self.history_table.selection()
        if selected_item:
            index = int(selected_item[0])
            password, strength, entropy, diversity = self.history[index]

            # Display detailed information in a pop-up
            popup = tk.Toplevel(self)
            popup.title("Password Details")
            popup.geometry("400x250")

            ttk.Label(popup, text=f"Password: {password}", font=("Arial", 12)).pack(pady=10)
            ttk.Label(popup, text=f"Strength: {strength}", font=("Arial", 12)).pack(pady=5)
            ttk.Label(popup, text=f"Entropy (bits): {entropy:.2f}", font=("Arial", 12)).pack(pady=5)
            ttk.Label(popup, text=f"Character Diversity: {diversity}", font=("Arial", 12)).pack(pady=5)
            ttk.Label(popup, text=f"Length: {len(password)}", font=("Arial", 12)).pack(pady=5)

            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

# Run the application
if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
