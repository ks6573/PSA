from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib

# Load the dataset
data_folder = "/Users/karan/PycharmProjects/Data"
dataset_path = f"{data_folder}/dataset.csv"
dataset = pd.read_csv(dataset_path)

# Feature engineering
dataset['char_diversity'] = dataset['password'].apply(lambda x: sum(1 for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:,.<>?/~`' if c in x))
features = dataset[['length', 'entropy', 'char_diversity']]
target = dataset['class_strength']

# Encode target
label_encoder = LabelEncoder()
target_encoded = label_encoder.fit_transform(target)

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, target_encoded, test_size=0.2, random_state=42)

# Train the model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the model and label encoder
model_path = f"{data_folder}/rf_model.pkl"
encoder_path = f"{data_folder}/label_encoder.pkl"
joblib.dump(rf_model, model_path)
joblib.dump(label_encoder, encoder_path)
print(f"Model saved to {model_path}")
print(f"Label encoder saved to {encoder_path}")