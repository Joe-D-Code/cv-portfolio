# Cat vs Dog Image Classifier

> A binary image classifier that distinguishes cats from dogs using transfer learning with a pretrained ResNet50 model, built in PyTorch and trained on Google Colab.

**Validation accuracy: ~98%**

---

## Overview

Using transfer learning rather than training from scratch, this project applies a ResNet50 backbone pretrained on ImageNet to classify cat and dog images with high accuracy. The backbone is first frozen so that only a custom classification head is trained, before optionally unfreezing the full network for additional fine-tuning. The dataset, sourced from Hugging Face, loads automatically without any manual download.

---

## What I Learned

This project served as a hands-on introduction to several core computer vision and deep learning concepts:

- **Transfer learning**, where reusing a model pretrained on ImageNet dramatically reduces training time and data requirements
- **Fine-tuning**, which involves freezing a backbone network and training only a custom classification head before optionally unfreezing the whole network for extra accuracy
- **Data augmentation**, applying random flips, rotations, and colour jitter to artificially increase dataset variety and improve generalisation
- **The training loop**, covering forward pass, loss calculation, backpropagation, and optimiser steps
- **Train/validation split**, holding back 20% of data to measure how well the model generalises to unseen images
- **Learning rate scheduling**, using cosine annealing to gradually reduce the learning rate as training converges

---

## Dataset

The notebook uses the [Microsoft Cats vs Dogs](https://huggingface.co/datasets/microsoft/cats_vs_dogs) dataset loaded via Hugging Face, which provides approximately 25,000 labelled images of cats and dogs without requiring any manual download.

---

## Model Architecture

| Component | Detail |
|---|---|
| Base model | ResNet50 pretrained on ImageNet |
| Strategy | Freeze backbone, train head, optional full fine-tune |
| Classifier head | Dropout, Linear(2048, 256), ReLU, Dropout, Linear(256, 2) |
| Loss function | CrossEntropyLoss |
| Optimiser | AdamW |
| LR scheduler | Cosine Annealing |

---

## How to Run

The notebook is designed to run on **Google Colab** with a free T4 GPU.

1. Open [Google Colab](https://colab.research.google.com/)
2. Upload `Cat_Vs_Dog.ipynb`
3. Set the runtime via **Runtime → Change runtime type → T4 GPU**
4. Run all cells in order

The dataset downloads automatically on first run (approximately 800 MB, cached after that).

### Running locally

```bash
pip install -r requirements.txt
jupyter notebook Cat_Vs_Dog.ipynb
```

Note that local CPU training is significantly slower, taking roughly one to two hours compared to around fifteen minutes on a GPU.

---

## Project Structure

```
computer-vision/
├── Cat_Vs_Dog.ipynb       # Main notebook
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

After training, a `best_cat_dog_model.pth` file will be saved containing the best model weights.

---

## Making Predictions

Once trained, the notebook includes a `predict()` function that accepts either a local file path or a URL, loading the saved model weights and returning the predicted class with a confidence score.

```python
predict('https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_November_2010-1a.jpg')
```

---

## AI Assistance

This project was built with assistance from [Claude](https://claude.ai) (Anthropic), which helped generate the initial notebook structure, debug errors, and explain concepts along the way. The techniques used, including transfer learning, ResNet50, data augmentation, and the PyTorch training loop, are standard and well-established approaches in computer vision. The goal was to understand and apply those techniques hands-on, using AI as a learning aid rather than a shortcut.

---

## Next Steps

- Add a confusion matrix and per-class metrics
- Try EfficientNet-B0 as a lighter alternative backbone
- Extend to breed classification using the [Oxford-IIIT Pet Dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/)
- Export the model to ONNX for deployment
- Build a Gradio web demo