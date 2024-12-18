# test_model_eval.py
# author: Marek Boulerice
# date: 2024-12-15

import pytest
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.datasets import make_classification

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.model_eval import eval_model

# Test data setup

# Create synthetic dataset
X, y = make_classification(
    n_samples=100, 
    n_features=10, 
    n_informative=5, 
    n_redundant=2, 
    random_state=42
)
# Convert to DataFrame for compatibility
X = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
y = pd.DataFrame(np.where(y == 1, '> 50% diameter narrowing', '<= 50% diameter narrowing'), columns=["target"])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#create dummy model to use to test function, and fit model
dummy = DummyClassifier()
dummy.fit(X_train, y_train)    


# Test Case 1: wrong type passed to function returns an error
X_train_as_np = X_train.copy().to_numpy()
def test_valid_data_type():
    with pytest.raises(TypeError):
        eval_model(dummy, X_train_as_np, y_train, X_test, y_test)

# Test Case 2: empty data frame
case_empty_data_frame = X_test.copy().iloc[0:0]
def test_valid_data_empty_data_frame():
    with pytest.raises(ValueError):
        eval_model(dummy, X_train, y_train, case_empty_data_frame, y_test)

# Test case 3: given appropriate imput the function outputs a dataframe of correct dimensions
def test_success():
    output_df = eval_model(dummy, X_train, y_train, X_test, y_test)
    assert isinstance(output_df, pd.DataFrame), "Output is not a pandas DataFrame"
    assert output_df.shape == (3, 3), "Output does not have the shape (3, 3)"

print("All tests passed.")


