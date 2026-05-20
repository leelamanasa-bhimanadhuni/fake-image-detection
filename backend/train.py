
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../image_detection_data')
MODEL_DIR = os.path.join(BASE_DIR, '../model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.h5')

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Data Parameters
IMG_HEIGHT = 256
IMG_WIDTH = 256
BATCH_SIZE = 32

def train_and_save_model():
    print("Setting up Data Generators...")
    
    # Rescale verification: 1./255.
    train_datagen = ImageDataGenerator(
        rescale=1./255.,
        horizontal_flip=True
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255.)

    train_dir = os.path.join(DATA_DIR, 'train')
    valid_dir = os.path.join(DATA_DIR, 'valid')
    
    if not os.path.exists(train_dir):
        print(f"Error: Train directory not found at {train_dir}")
        return

    train_ds = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    valid_ds = val_datagen.flow_from_directory(
        valid_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    print("Building DenseNet121 Model...")
    
    # Load DenseNet121 base model
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    )
    
    # Freeze base model
    base_model.trainable = False

    # Custom Classification Head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2), # Added dropout for regularization
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.summary()

    print("Starting Training (Quick Check Mode)...")
    # Limiting steps for quicker execution (DEMO purpose)
    # Remove 'steps_per_epoch' and 'validation_steps' parameters 
    # to train on the entire dataset in a real scenario.
    history = model.fit(
        train_ds,
        validation_data=valid_ds,
        epochs=1,
        steps_per_epoch=10,
        validation_steps=5
    )

    print(f"Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    print("Model saved successfully.")

if __name__ == '__main__':
    train_and_save_model()
