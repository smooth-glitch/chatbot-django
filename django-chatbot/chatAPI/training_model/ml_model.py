import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load and prepare the dataset
df = pd.read_csv('Mydataset.csv')

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

# Fit the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save the model
model.save('trained/chatbot_model.h5')
