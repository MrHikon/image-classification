import os
import tensorflow as tf

folders = [
    'dataset/train/short',
    'dataset/train/moderate',
    'dataset/train/tall',
    'dataset/val/short',
    'dataset/val/moderate',
    'dataset/val/tall'
]

removed = 0

for folder in folders:
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        # Skip non-image files immediately
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
        if not filename.lower().endswith(valid_extensions):
            print(f'Removing non-image file: {filename}')
            os.remove(filepath)
            removed += 1
            continue

        # Try to read with TensorFlow exactly like data_loader does
        try:
            img_raw = tf.io.read_file(filepath)
            tf.io.decode_image(img_raw, channels=3, expand_animations=False)
        except Exception as e:
            print(f'Removing bad file: {filename} — {str(e)[:50]}')
            os.remove(filepath)
            removed += 1

print(f'\nDone. Removed {removed} bad files.')
print('Your folders are now clean.')