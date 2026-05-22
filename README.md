# Human Height Classification Engine using ConvNeXtTiny Architecture

An advanced, production-ready Deep Learning classification pipeline that analyzes full-body human images to predict whether an individual's height classification falls into one of three categories: **Short**, **Moderate**, or **Tall**. 

This system leverages Transfer Learning via a state-of-the-art **ConvNeXtTiny** core pretrained on ImageNet, coupled with a custom deep regularization head and **Test Time Augmentation (TTA)** to achieve stable, high-confidence predictions. The project features an interactive deployment interface powered by a Streamlit web application.

---

## 📐 System Architecture Overview

The system processes input images through a heavily optimized computer vision pipeline:
1. **Dynamic Input Pipeline:** Standardizes images to $224 \times 224 \times 3$ resolution, dynamically converting inputs to match the precise internal normalization criteria required by ConvNeXt.
2. **Feature Extraction Core:** Uses a frozen `ConvNeXtTiny` base layer to capture rich global and spatial visual hierarchies from full-body visual profiles.
3. **Classification Head:** Implements Global Average Pooling 2D, Batch Normalization, and stacked Dense layers ($256 \to 128$) with progressive Dropout scaling (`0.4` and `0.3`) to prevent overfitting.
4. **Optimization Strategy:** Employs a multi-phase training structure (Frozen Base Feature Extraction followed by selective Unfrozen Top-40 Layer Fine-Tuning) controlled by adaptive learning rate reduction triggers (`ReduceLROnPlateau`).

---

## 📂 Repository Structure & Components

* **`model.py`** – Definition of the core deep neural network architecture and compilation configurations.
* **`data_loader.py`** – Handles directory stream loading, batch management (`Batch Size = 32`), and automated training data augmentations.
* **`clean_images.py`** – A defense utility script that parses dataset directories to find, isolate, and remove corrupt image structures before training.
* **`train.py`** – The primary training execution script orchestrating the dual-phase frozen and fine-tuning optimization workflows.
* **`evaluate.py`** – Evaluates validation dataset metrics, generates micro/macro statistics, and saves a high-resolution performance Confusion Matrix plot.
* **`predict.py`** – Production inference engine featuring a 6-factor Test Time Augmentation (TTA) wrapper that computes average prediction confidences.
* **`app.py`** – User interface layer running an interactive Streamlit web dashboard for real-time photo uploads and predictions.
* **`requirements.txt`** – Explicit manifest listing all upstream package versions needed to execute this repository.

---

## 🛠️ Installation & Environment Setup

### 1. Prerequisites
Ensure you have Python 3.8 to 3.11 installed along with a functional terminal shell.

### 2. Clone and Navigate to the Repository
```bash
git clone <your-github-repository-link-here>
cd <repository-folder-name>