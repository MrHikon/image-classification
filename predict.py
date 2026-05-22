# predict.py - Height Classifier Prediction
# Includes Test Time Augmentation for better accuracy

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from model import build_model, compile_model

CLASS_NAMES = ['moderate', 'short', 'tall']
SAVE_PATH   = 'best_model.keras'
IMG_SIZE    = 224

_cached_model = None


def get_model():
    """Load model once and cache it for reuse."""
    global _cached_model
    if _cached_model is None:
        if not os.path.exists(SAVE_PATH):
            raise FileNotFoundError(
                f"Model not found at {SAVE_PATH}. Run train.py first."
            )
        print("Loading model (first time only)...")
        _cached_model, _ = build_model(num_classes=3)
        _cached_model     = compile_model(_cached_model)
        _cached_model.load_weights(SAVE_PATH)
        print("Model loaded and cached.")
    return _cached_model


def predict_single_image(image_path, show_plot=False):
    """
    Takes any image path.
    Uses Test Time Augmentation for better accuracy.
    Returns (predicted_class, confidence).
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    model = get_model()

    # Load and prepare image
    img_raw   = tf.io.read_file(image_path)
    img       = tf.io.decode_image(
                    img_raw, channels=3,
                    expand_animations=False
                )
    img       = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    img       = tf.cast(img, tf.float32) / 255.0
    img_batch = tf.expand_dims(img, axis=0)

    # Test Time Augmentation layers
    augment = tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomZoom(0.05),
        tf.keras.layers.RandomRotation(0.05),
        tf.keras.layers.RandomContrast(0.05),
    ])

    all_probs = []

    # Prediction 1 — original image
    all_probs.append(model.predict(img_batch, verbose=0)[0])

    # Predictions 2-6 — augmented versions
    for _ in range(5):
        aug_img = augment(img_batch, training=True)
        all_probs.append(model.predict(aug_img, verbose=0)[0])

    probs = np.mean(all_probs, axis=0)

    predicted_index = np.argmax(probs)
    predicted_class = CLASS_NAMES[predicted_index]
    confidence      = float(np.max(probs) * 100)

    # Print to terminal
    print("\n" + "=" * 50)
    print(f"  RESULT     : {predicted_class.upper()}")
    print(f"  CONFIDENCE : {confidence:.1f}%")
    print("=" * 50)
    print(f"\n  Moderate : {probs[0]*100:.1f}%")
    print(f"  Short    : {probs[1]*100:.1f}%")
    print(f"  Tall     : {probs[2]*100:.1f}%")
    print(f"\n  (Averaged from 6 predictions using TTA)")

    display_img = tf.cast(img * 255, tf.uint8).numpy()
    plt.figure(figsize=(6, 7))
    plt.imshow(display_img)
    color = 'green' if confidence > 60 else 'orange'
    plt.title(
        f"Prediction: {predicted_class.capitalize()}\nConfidence: {confidence:.1f}%",
        fontsize=14, fontweight='bold', color=color
    )
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('prediction_result.png', dpi=150, bbox_inches='tight')
    print("\nResult saved as prediction_result.png")

    if show_plot:
        plt.show()
    plt.close()

    return predicted_class, confidence


if __name__ == "__main__":
    if len(sys.argv) > 1:
        predict_single_image(sys.argv[1], show_plot=True)
    else:
        image_path = None
        for folder in ['dataset/val/short',
                       'dataset/val/moderate',
                       'dataset/val/tall']:
            if os.path.exists(folder):
                files = [f for f in os.listdir(folder)
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if files:
                    image_path = os.path.join(folder, files[0])
                    break

        if image_path:
            predict_single_image(image_path, show_plot=True)
        else:
            print("No image found.")
            print("Usage: python predict.py path\\to\\image.jpg")