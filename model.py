# model.py - ConvNeXtTiny FIXED
import tensorflow as tf
from tensorflow.keras.applications import ConvNeXtTiny
from tensorflow.keras.applications.convnext import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization, Lambda
from tensorflow.keras.models import Model

def build_model(num_classes=3):

    # Input expects 0-1 range coming from data_loader
    inputs = tf.keras.Input(shape=(224, 224, 3))

    # Convert back to 0-255 then apply ConvNeXt's own preprocessing
    # This is the critical fix — ConvNeXtTiny needs its specific preprocessing
    x = Lambda(lambda img: preprocess_input(img * 255))(inputs)

    # Load ConvNeXtTiny pretrained on ImageNet
    base_model = ConvNeXtTiny(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False

    # Pass through base model
    x = base_model(x)

    # Our custom classification head
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.4)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    output = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=output)

    return model, base_model


def compile_model(model, learning_rate=0.001):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


if __name__ == "__main__":
    model, base = build_model(num_classes=3)
    model = compile_model(model)
    model.summary()
    print("\nConvNeXtTiny model built successfully!")
    print(f"Total layers: {len(model.layers)}")