# This file loads images from your dataset folders

import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np

# ── SETTINGS ──────────────────────────────────────────────────────────────────
# Every image gets resized to 224x224 pixels
IMG_SIZE = 224

# The number of images to process at one time before updating the model
BATCH_SIZE = 32

# The 3 classes we are classifying
CLASS_NAMES = ['moderate', 'short', 'tall']


# ── MAIN FUNCTION ─────────────────────────────────────────────────────────────
def load_data(data_dir='dataset'):
    #Loads training and validation images from the dataset folder.

    train_dir = os.path.join(data_dir, 'train')
    val_dir   = os.path.join(data_dir, 'val')

    # Check folders exist before trying to load
    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Training folder not found: {train_dir}")
    if not os.path.exists(val_dir):
        raise FileNotFoundError(f"Validation folder not found: {val_dir}")

    # ── TRAINING DATA ──────────────────────────────────────────────────────────
    # We apply augmentation to training data only
    # Augmentation creates variations of images — flipped, rotated, zoomed
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        train_dir,

        # Shuffle training data so the model doesn't learn order
        shuffle=True,
        seed=42,

        # Resize every image to 224x224
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,

        # one_hot gives labels as [1,0,0] [0,1,0] [0,0,1]
        label_mode='categorical'
    )

    # ── VALIDATION DATA ────────────────────────────────────────────────────────
    # No augmentation on validation data. we are testing on clean images 

    val_dataset = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        shuffle=False,
        seed=42,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )

    # ── SCALE PIXEL VALUES ─────────────────────────────────────────────────────
    # Images come in with pixel values from 0 to 255
    # We are to scale them down to 0.0 to 1.0
    # Neural networks learn much faster with small numbers
    rescale = tf.keras.layers.Rescaling(1.0 / 255)

    train_dataset = train_dataset.map(
        lambda images, labels: (rescale(images), labels)
    )

    val_dataset = val_dataset.map(
        lambda images, labels: (rescale(images), labels)
    )

    # ── AUGMENTATION ──────────────────────────────────────────────────────────
    # Apply only to training data
    # RandomFlip  — mirrors the image left to right randomly
    # RandomRotation — tilts the image slightly
    # RandomZoom  — zooms in or out slightly
    # Stronger augmentation for small datasets creates more variation from limited images
    augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.05),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1),
    ])

    train_dataset = train_dataset.map(
        lambda images, labels: (augmentation(images, training=True), labels)
    )

    # ── PERFORMANCE OPTIMISATION ───────────────────────────────────────────────
    # prefetch loads the next batch while the model is training on the current one
    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    val_dataset   = val_dataset.prefetch(buffer_size=AUTOTUNE)

    # Print a summary of what was loaded
    print(f"\nDataset loaded successfully!")
    print(f"Class names: {CLASS_NAMES}")
    print(f"Image size:  {IMG_SIZE}x{IMG_SIZE}")
    print(f"Batch size:  {BATCH_SIZE}")

    return train_dataset, val_dataset


# ── VISUALISE FUNCTION ─────────────────────────────────────────────────────────
def show_sample_images(dataset, class_names=CLASS_NAMES):
    """
    Displays a grid of sample images from the dataset.
    Call this to visually confirm your images loaded correctly.
    """

    plt.figure(figsize=(12, 6))

    # Get one batch of images
    for images, labels in dataset.take(1):
        for i in range(min(9, len(images))):
            plt.subplot(3, 3, i + 1)

            # Convert back to 0-255 range for display
            img = images[i].numpy()
            img = (img * 255).astype(np.uint8)

            plt.imshow(img)

            # Get the class name from the one-hot label
            label_index = np.argmax(labels[i])
            plt.title(class_names[label_index], fontsize=12)
            plt.axis('off')

    plt.suptitle('Sample Training Images', fontsize=16)
    plt.tight_layout()
    plt.show()


# ── TEST THIS FILE ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading dataset...")
    train_ds, val_ds = load_data(data_dir='dataset')
    print("\nShowing sample images...")
    show_sample_images(train_ds)