# 😊 Day 7 — Sentiment Classifier

## 🎯 Objective

Build a basic sentiment classification model that predicts whether a movie review is positive or negative.

## ✅ Tasks Completed

- Created a small labelled dataset of movie reviews.
- Assigned positive and negative sentiment labels.
- Converted text into numerical features using CountVectorizer.
- Split the dataset into training and testing sets.
- Trained a Multinomial Naive Bayes classifier.
- Evaluated the model using accuracy.
- Tested the model on new sentences.
- Used prediction probabilities to examine model confidence.

## 🔄 Classification Pipeline

Movie Reviews  
↓  
CountVectorizer  
↓  
Bag-of-Words Features  
↓  
Train / Test Split  
↓  
Multinomial Naive Bayes  
↓  
Positive / Negative Prediction

## 📊 Prediction

- `1` → Positive
- `0` → Negative

## 💡 Key Learning

Text classification becomes possible after converting text into numerical features.

The experiment also showed that a small dataset has limitations. The model can struggle with mixed opinions, negation, unfamiliar vocabulary, and subtle language.

## 🛠️ Technologies Used

- Python 3
- Google Colab
- Scikit-learn
- CountVectorizer
- Multinomial Naive Bayes
- Accuracy Score

---

📌 Day 7 of the ABTalks 60-Day AI Challenge — Artificial Intelligence Track
