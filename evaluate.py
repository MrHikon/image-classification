# evaluate.py - Height Classifier Evaluation
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from data_loader import load_data
from model import build_model, compile_model

# Aligned exactly with data_loader folders
CLASS_NAMES = ['moderate', 'short', 'tall']
SAVE_PATH   = 'best_model.keras'


def evaluate():

    print("=" * 50)
    print("  HEIGHT CLASSIFIER — EVALUATION")
    print("  Model: ConvNeXtTiny")
    print("=" * 50)

    if not os.path.exists(SAVE_PATH):
        print(f"Error: {SAVE_PATH} not found. Run train.py first.")
        return

    # Rebuild architecture then load weights
    print("\nRebuilding model architecture...")
    model, _ = build_model(num_classes=3)
    model     = compile_model(model)

    print("Loading saved weights...")
    model.load_weights(SAVE_PATH)
    print("Weights loaded successfully.")

    print("\nLoading validation data...")
    _, val_ds = load_data(data_dir='dataset')

    print("\nRunning predictions on validation set...")
    all_predictions = []
    all_true_labels = []

    for images, labels in val_ds:
        preds             = model.predict(images, verbose=0)
        predicted_classes = np.argmax(preds,          axis=1)
        true_classes      = np.argmax(labels.numpy(), axis=1)
        all_predictions.extend(predicted_classes)
        all_true_labels.extend(true_classes)

    all_predictions = np.array(all_predictions)
    all_true_labels = np.array(all_true_labels)

    accuracy = np.mean(all_predictions == all_true_labels)
    print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

    print("\nDetailed Classification Report:")
    print("-" * 45)
    print(classification_report(
        all_true_labels,
        all_predictions,
        target_names=CLASS_NAMES
    ))

    cm = confusion_matrix(all_true_labels, all_predictions)

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        linewidths=1
    )
    plt.title(
        'Confusion Matrix — ConvNeXtTiny\nRows=Actual  Columns=Predicted',
        fontsize=14
    )
    plt.ylabel('Actual Class',    fontsize=12)
    plt.xlabel('Predicted Class', fontsize=12)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
    print("Confusion matrix saved as confusion_matrix.png")
    plt.show()

    print("\nAccuracy Per Class:")
    print("-" * 30)
    for i, class_name in enumerate(CLASS_NAMES):
        mask  = all_true_labels == i
        if np.sum(mask) > 0:
            acc   = np.mean(all_predictions[mask] == all_true_labels[mask])
            count = np.sum(mask)
            print(f"  {class_name:10} {acc*100:.1f}%  ({count} images)")
        else:
            print(f"  {class_name:10} N/A (0 images)")

    print("\n" + "=" * 50)
    print("  SUMMARY")
    print("=" * 50)
    print(f"  Model        : ConvNeXtTiny")
    print(f"  Total images : {len(all_true_labels)}")
    print(f"  Correct      : {int(np.sum(all_predictions == all_true_labels))}")
    print(f"  Wrong        : {int(np.sum(all_predictions != all_true_labels))}")
    print(f"  Accuracy     : {accuracy * 100:.2f}%")
    print("=" * 50)
    print("\nEvaluation complete!")


if __name__ == "__main__":
    try:
        import seaborn
    except ImportError:
        os.system('pip install seaborn')
    evaluate()