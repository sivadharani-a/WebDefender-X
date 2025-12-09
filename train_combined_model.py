# train_combined_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # For saving the model

# Load the dataset (replace with your dataset file path)
DATASET_PATH = 'C:/Users/sivad/Desktop/WebDefender-X(final)/datasets/combined_attacks.csv'

# Function to load and preprocess dataset
def load_dataset(filepath):
    try:
        df = pd.read_csv(filepath)
        print("[✓] Dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"[!] Error loading dataset: {e}")
        return None

# Reduce dataset size by sampling (e.g., use 10% of the data)
def sample_dataset(df, frac=0.1):
    print(f"[✓] Sampling {frac * 100}% of the dataset...")
    return df.sample(frac=frac, random_state=42)

# Preprocess dataset: Handle missing values, categorical data, and scaling
def preprocess_data(df):
    print("[✓] Preprocessing data...")
    
    # Print column names to check for the 'Attack Type' column
    print(f"[✓] Dataset Columns: {df.columns.tolist()}")
    
    # Check if 'Attack Type' column exists (update with the correct name)
    if 'Attack Type' not in df.columns:
        raise KeyError("The dataset does not contain 'Attack Type' column. Please check the dataset.")
    
    # Drop columns that are not needed for the model
    df = df.drop(columns=['Event ID', 'Timestamp', 'Source IP', 'Destination IP'])
    
    # Handle categorical columns (e.g., encode them)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    print(f"[✓] Categorical columns: {categorical_cols}")
    
    # Apply label encoding for categorical columns (e.g., 'Attack Type', 'User Agent')
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    
    # Extract features and target variable
    X = df.drop(columns=['Attack Type'])  # 'Attack Type' is the target column
    y = df['Attack Type']
    
    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Train the model using RandomForestClassifier
def train_model(X_train, y_train):
    print("[✓] Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate the model on the test set
def evaluate_model(model, X_test, y_test):
    print("[✓] Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"[✓] Model accuracy: {accuracy:.4f}")
    return accuracy

# Main code
if __name__ == "__main__":
    df = load_dataset(DATASET_PATH)
    if df is not None:
        # Sample the dataset if it's too large
        df = sample_dataset(df, frac=0.1)  # Use 10% of the dataset
        
        # Preprocess the data
        try:
            X_train, X_test, y_train, y_test = preprocess_data(df)
            
            # Train the model
            model = train_model(X_train, y_train)
            
            # Evaluate the model
            accuracy = evaluate_model(model, X_test, y_test)
            
            # Save the trained model
            joblib.dump(model, 'trained_model.pkl')  # Save the model
            print("[✓] Model saved as 'trained_model.pkl'")

        except KeyError as e:
            print(f"[!] {e}")
