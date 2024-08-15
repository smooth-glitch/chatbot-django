import matplotlib.pyplot as plt
import json
import numpy as np

# Load the history from the JSON file
with open('training_history.json', 'r') as f:
    history = json.load(f)

# Plotting Accuracy
plt.figure(figsize=(12, 6))

# Training vs Validation Accuracy
plt.subplot(1, 2, 1)
plt.plot(history['accuracy'], label='Training Accuracy')
plt.plot(history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

# Plotting Loss
plt.subplot(1, 2, 2)
plt.plot(history['loss'], label='Training Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.tight_layout()
plt.show()

# Additional Plots

# 1. Difference Between Training and Validation Accuracy
plt.figure(figsize=(6, 6))
accuracy_diff = np.array(history['accuracy']) - np.array(history['val_accuracy'])
plt.plot(accuracy_diff, label='Training - Validation Accuracy Difference')
plt.xlabel('Epoch')
plt.ylabel('Difference')
plt.title('Difference Between Training and Validation Accuracy')
plt.legend()
plt.show()

# 2. Cumulative Accuracy Plot
plt.figure(figsize=(6, 6))
cumulative_accuracy = np.cumsum(history['accuracy']) / (np.arange(len(history['accuracy'])) + 1)
plt.plot(cumulative_accuracy, label='Cumulative Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Cumulative Accuracy')
plt.title('Cumulative Training Accuracy Over Epochs')
plt.legend()
plt.show()

# 3. Validation Accuracy with Smoothing (Moving Average)
window_size = 3
smoothed_val_accuracy = np.convolve(history['val_accuracy'], np.ones(window_size)/window_size, mode='valid')
plt.figure(figsize=(6, 6))
plt.plot(history['val_accuracy'], label='Validation Accuracy')
plt.plot(range(window_size-1, len(smoothed_val_accuracy) + window_size-1), smoothed_val_accuracy, label='Smoothed Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Validation Accuracy')
plt.title('Validation Accuracy with Smoothing')
plt.legend()
plt.show()
