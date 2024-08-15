import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import json

# Check if the mydb.json file exists
file_path = 'mydb.json'

if os.path.exists(file_path):
    print(f"File {file_path} exists!")
    df = pd.read_json(file_path)
else:
    print(f"File {file_path} does NOT exist!")
    raise FileNotFoundError(f"File {file_path} does not exist. Please check the path and try again.")

# Flatten the lists in 'patterns' and 'responses'
df['patterns'] = df['patterns'].apply(lambda x: ' '.join(x))
df['responses'] = df['responses'].apply(lambda x: ' '.join(x))

# Initialize the LabelEncoder
le = LabelEncoder()

# Preprocess data
df['patterns'] = le.fit_transform(df['patterns'])  # Convert text to numbers
df['responses'] = le.fit_transform(df['responses'])  # Convert responses to numbers

X = df[['patterns']]  # Features
y = df['responses']   # Target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = Sequential([
    Dense(10, activation='relu', input_dim=X_train.shape[1]),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Fit the model and store training history
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save the model
model.save('trained/chatbot_model.h5')

# Save the training history
with open('training_history.json', 'w') as f:
    json.dump(history.history, f)
