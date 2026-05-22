# app.py - Height Classifier Web App
# Model: ConvNeXtTiny | Framework: TensorFlow + Streamlit

import streamlit as st
from PIL import Image
import os
from predict import predict_single_image

st.set_page_config(
    page_title="Height Classifier AI",
    page_icon="📏",
    layout="centered"
)

st.title("📏 Height Classifier")
st.markdown(
    "### Upload a full body photo — AI predicts: **Short · Moderate · Tall**"
)
st.markdown("---")

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ About This App")
    st.write("""
    This AI model uses **ConvNeXtTiny** architecture
    with Transfer Learning trained on a custom
    height classification dataset.

    It analyzes visual body proportions to classify
    a person as **Short**, **Moderate**, or **Tall**.
    """)
    st.markdown("---")
    st.write("**Model:** ConvNeXtTiny (2022)")
    st.write("**Framework:** TensorFlow + Keras")
    st.write("**Technique:** Transfer Learning")
    st.write("**Classes:** Short · Moderate · Tall")
    st.write("**Enhancement:** Test Time Augmentation")
    st.markdown("---")
    st.caption("Built with Streamlit")

# ── UPLOAD ────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📁 Upload a full body image of a person",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    help="Best results with full body standing photos on a clear background"
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Uploaded Image", use_column_width=True)

    st.markdown("")

    if st.button("🔍 Classify Height", type="primary", use_container_width=True):

        temp_path = "temp_uploaded_image.jpg"

        # Convert to RGB before saving as JPEG
        # This prevents crashes with PNG images that have transparency
        image_rgb = image.convert("RGB")
        image_rgb.save(temp_path)

        with st.spinner("Analyzing image with AI (Test Time Augmentation)..."):
            try:
                # predict_single_image returns lowercase values matching CLASS_NAMES
                predicted_class, confidence = predict_single_image(
                    temp_path, show_plot=False
                )
                confidence = float(confidence)

                st.markdown("---")
                st.markdown("### 🎯 Prediction Result")

                # Emoji and color check matches lowercase outputs
                if predicted_class.lower() == "tall":
                    emoji = "🟢"
                elif predicted_class.lower() == "moderate":
                    emoji = "🟡"
                else:
                    emoji = "🔴"

                st.success(
                    f"{emoji} **Predicted Class: {predicted_class.upper()}**"
                )
                st.metric(label="Confidence Score", value=f"{confidence:.1f}%")

                # Confidence interpretation
                if confidence >= 70:
                    st.info("✅ High confidence prediction")
                elif confidence >= 50:
                    st.warning(
                        "⚠️ Moderate confidence — try a clearer full body photo"
                    )
                else:
                    st.error(
                        "❌ Low confidence — use a clear full body standing photo"
                    )

                st.markdown("")
                st.caption(
                    "Result averaged from 6 predictions using "
                    "Test Time Augmentation for improved accuracy."
                )

            except FileNotFoundError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                st.info(
                    "Make sure best_model.keras exists in this folder. "
                    "Run train.py first if needed."
                )

        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

else:
    st.info("👆 Upload a full body photo above to get started")
    st.markdown("")
    st.markdown("**Tips for best results:**")
    st.write("• Use a clear full body photo showing the entire person")
    st.write("• Person should be standing upright")
    st.write("• Clear or plain background works best")
    st.write("• Good lighting improves accuracy significantly")
    st.write("• Avoid group photos — one person only")

st.markdown("---")
st.caption(
    "Height Classifier AI | Model: ConvNeXtTiny | "
    "Run with: `streamlit run app.py`"
)