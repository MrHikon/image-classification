import tensorflow as tf
import os
import matplotlib.pyplot as plt
from model import build_model, compile_model
from data_loader import load_data

# ── SETTINGS ──────────────────────────────────────────────────────────────────
EPOCHS_PHASE1 = 30   # Phase 1 — frozen base
EPOCHS_PHASE2 = 20   # Phase 2 — fine tuning
SAVE_PATH     = 'best_model.keras'
CLASS_NAMES   = ['moderate', 'short', 'tall']


# ── CALLBACKS ─────────────────────────────────────────────────────────────────
def get_callbacks(patience=8):
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=patience,
        restore_best_weights=True,
        verbose=1
    )
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.3,
        patience=4,
        min_lr=1e-8,
        verbose=1
    )
    return [early_stop, checkpoint, reduce_lr]


# ── PLOT ──────────────────────────────────────────────────────────────────────
def plot_history(history, title='Training Results'):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(history.history['accuracy'],
             label='Training', color='blue', linewidth=2)
    ax1.plot(history.history['val_accuracy'],
             label='Validation', color='orange', linewidth=2)
    ax1.set_title('Accuracy Over Epochs', fontsize=14)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(history.history['loss'],
             label='Training', color='blue', linewidth=2)
    ax2.plot(history.history['val_loss'],
             label='Validation', color='orange', linewidth=2)
    ax2.set_title('Loss Over Epochs', fontsize=14)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)

    plt.suptitle(title, fontsize=15)
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
    print('Graph saved as training_results.png')
    plt.show()


# ── MAIN ──────────────────────────────────────────────────────────────────────
def train():

    print("=" * 55)
    print("  HEIGHT CLASSIFIER — ConvNeXt Tiny TRAINING")
    print("=" * 55)

    # STEP 1 — Load data
    print("\nSTEP 1: Loading dataset...")
    train_ds, val_ds = load_data(data_dir='dataset')

    # STEP 2 — Build model
    print("\nSTEP 2: Building ConvNeXt Tiny model...")
    model, base_model = build_model(num_classes=3)

    # Slightly lower learning rate for more careful learning
    model = compile_model(model, learning_rate=0.0005)
    print("Model ready.")

    # STEP 3 — Phase 1 Training (frozen base)
    # Base model frozen — only our Dense layers train
    print(f"\nSTEP 3: Phase 1 Training — {EPOCHS_PHASE1} epochs max")
    print("Base model frozen. Training classification head only.\n")

    history1 = model.fit(
        train_ds,
        epochs=EPOCHS_PHASE1,
        validation_data=val_ds,
        callbacks=get_callbacks(patience=8),
        verbose=1
    )

    # Print Phase 1 best result
    best_val = max(history1.history['val_accuracy'])
    print(f"\nPhase 1 best validation accuracy: {best_val*100:.2f}%")

    # STEP 4 — Phase 2 Fine Tuning (unfreeze more layers)
    print(f"\nSTEP 4: Phase 2 Fine-tuning — {EPOCHS_PHASE2} epochs max")
    print("Unfreezing top 40 layers of ConvNeXtTiny...\n")

    base_model.trainable = True

    # Unfreeze top 40 layers this time — more than before
    for layer in base_model.layers[:-40]:
        layer.trainable = False

    # Very small learning rate — too large and it destroys the pretrained knowledge
    model = compile_model(model, learning_rate=0.00005)

    history2 = model.fit(
        train_ds,
        epochs=EPOCHS_PHASE2,
        validation_data=val_ds,
        callbacks=get_callbacks(patience=8),
        verbose=1
    )

    # STEP 5 — Results
    print("\nSTEP 5: Plotting fine-tuning results...")
    plot_history(history2, title='Fine-Tuning Results — ConvNeXtTiny Height Classifier')

    # Final score
    print("\n" + "=" * 55)
    print("  FINAL RESULTS")
    print("=" * 55)
    loss, accuracy = model.evaluate(val_ds, verbose=0)
    print(f"Validation Accuracy: {accuracy * 100:.2f}%")
    print(f"Validation Loss:     {loss:.4f}")

    phase1_best = max(history1.history['val_accuracy']) * 100
    phase2_best = max(history2.history['val_accuracy']) * 100
    overall_best = max(phase1_best, phase2_best)

    print(f"\nPhase 1 best: {phase1_best:.2f}%")
    print(f"Phase 2 best: {phase2_best:.2f}%")
    print(f"Overall best: {overall_best:.2f}%")
    print(f"\nModel saved to: {SAVE_PATH}")
    print("Training complete!")


if __name__ == "__main__":
    train()