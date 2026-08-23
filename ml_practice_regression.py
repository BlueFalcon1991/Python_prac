"""
ml_practice_regression.py

Companion script for the ml_practice MySQL database.
Run ml_practice_db.sql in MySQL Workbench FIRST, then run this.

pip install mysql-connector-python sqlalchemy pandas scikit-learn matplotlib

Structure (simple -> complex):
  1. Simple Linear Regression      -> experience_salary
  2. Multiple Linear Regression    -> advertising_sales
  3. Logistic Regression           -> customer_churn
  4. YoY Projection (feature eng.) -> yearly_revenue
"""

import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error, r2_score,
    accuracy_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
# Update credentials to match your MySQL Workbench connection
DB_USER = "root"
DB_PASSWORD = "asd123456"
DB_HOST = "localhost"
DB_NAME = "ml_practice"

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


# ===========================================================================
# 1. SIMPLE LINEAR REGRESSION -- experience_salary
#    1 feature -> 1 target, matches: model.predict([[6]])
# ===========================================================================
def simple_linear_regression():
    print("\n=== 1. Simple Linear Regression: years_experience -> salary ===")

    df = pd.read_sql("SELECT years_experience, salary FROM experience_salary", engine)

    X = df[["years_experience"]]
    y = df["salary"]

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[6]])
    print(f"Predicted salary at 6 years experience: {prediction[0]:,.2f}")
    print(f"Coefficient (slope): {model.coef_[0]:,.2f}")
    print(f"Intercept: {model.intercept_:,.2f}")
    print(f"R^2 on training data: {model.score(X, y):.4f}")


# ===========================================================================
# 2. MULTIPLE LINEAR REGRESSION -- advertising_sales
#    3 features -> 1 target, with a proper train/test split
# ===========================================================================
def multiple_linear_regression():
    print("\n=== 2. Multiple Linear Regression: ad spend -> sales ===")

    df = pd.read_sql(
        "SELECT tv_spend, radio_spend, newspaper_spend, sales FROM advertising_sales",
        engine
    )

    X = df[["tv_spend", "radio_spend", "newspaper_spend"]]
    y = df["sales"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Coefficients (tv, radio, newspaper):", model.coef_.round(4))
    print(f"Intercept: {model.intercept_:.4f}")
    print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.4f}")
    print(f"R^2: {r2_score(y_test, y_pred):.4f}")

    # example prediction: $150k TV, $20k radio, $10k newspaper spend
    example = pd.DataFrame([[150, 20, 10]], columns=["tv_spend", "radio_spend", "newspaper_spend"])
    print(f"Predicted sales for example spend: {model.predict(example)[0]:.2f}")


# ===========================================================================
# 3. LOGISTIC REGRESSION -- customer_churn
#    Mixed numeric + categorical features -> binary target (is_churned)
# ===========================================================================
def logistic_regression_churn():
    print("\n=== 3. Logistic Regression: predicting customer churn ===")

    df = pd.read_sql(
        """SELECT tenure_months, monthly_charges, total_charges,
                  contract_type, support_calls, is_churned
           FROM customer_churn""",
        engine
    )

    X = df.drop(columns=["is_churned"])
    y = df["is_churned"]

    numeric_features = ["tenure_months", "monthly_charges", "total_charges", "support_calls"]
    categorical_features = ["contract_type"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first"), categorical_features),
        ],
        remainder="passthrough"
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=1000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred))

    # example: month-to-month customer, 3 months tenure, high monthly charge, 4 support calls
    example = pd.DataFrame([{
        "tenure_months": 3,
        "monthly_charges": 95.0,
        "total_charges": 285.0,
        "contract_type": "Month-to-month",
        "support_calls": 4
    }])
    churn_prob = pipeline.predict_proba(example)[0][1]
    print(f"Predicted churn probability for example customer: {churn_prob:.2%}")


# ===========================================================================
# 4. YoY PROJECTION -- yearly_revenue
#    Feature engineering: turn (year, quarter) into a numeric time index,
#    one-hot encode region, then project forward.
# ===========================================================================
def yoy_revenue_projection():
    print("\n=== 4. YoY Revenue Projection ===")

    df = pd.read_sql(
        "SELECT yr, quarter, region, marketing_spend, revenue FROM yearly_revenue",
        engine
    )

    # engineered feature: continuous time index (e.g. 2018 Q1 = 0, 2018 Q2 = 1, ...)
    df["time_index"] = (df["yr"] - df["yr"].min()) * 4 + (df["quarter"] - 1)

    X = df[["time_index", "quarter", "region", "marketing_spend"]]
    y = df["revenue"]

    preprocessor = ColumnTransformer(
        transformers=[("region_ohe", OneHotEncoder(drop="first"), ["region"])],
        remainder="passthrough"
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:,.2f}")
    print(f"R^2: {r2_score(y_test, y_pred):.4f}")

    # project next 4 quarters (2026) for the North region
    next_time_index = df["time_index"].max() + [1, 2, 3, 4]
    future = pd.DataFrame({
        "time_index": next_time_index,
        "quarter": [1, 2, 3, 4],
        "region": "North",
        "marketing_spend": df.loc[df["region"] == "North", "marketing_spend"].mean()
    })
    future_pred = pipeline.predict(future)
    for q, val in zip([1, 2, 3, 4], future_pred):
        print(f"Projected 2026 Q{q} revenue (North): {val:,.2f}")


if __name__ == "__main__":
    simple_linear_regression()
    multiple_linear_regression()
    logistic_regression_churn()
    yoy_revenue_projection()
