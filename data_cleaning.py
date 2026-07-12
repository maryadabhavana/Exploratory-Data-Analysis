"""
Data Cleaning Module
Author: Maryada Bhavana Reddy

Description:
This script loads the raw dataset, cleans the data,
handles missing values, removes duplicates,
standardizes formats, and exports a cleaned dataset.
"""

import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load dataset from Excel."""
        self.df = pd.read_excel(self.file_path)
        print("Dataset Loaded Successfully")
        print(f"Rows: {self.df.shape[0]}")
        print(f"Columns: {self.df.shape[1]}")

    def dataset_info(self):
        """Display dataset information."""
        print("\nDataset Information")
        print("-" * 50)
        print(self.df.info())

    def missing_values(self):
        """Display missing values."""
        print("\nMissing Values")
        print("-" * 50)
        print(self.df.isnull().sum())

    def clean_missing_values(self):
        """Handle missing values."""

        numeric_columns = self.df.select_dtypes(include=np.number).columns
        categorical_columns = self.df.select_dtypes(include="object").columns

        # Fill numerical columns with median
        for col in numeric_columns:
            self.df[col].fillna(self.df[col].median(), inplace=True)

        # Fill categorical columns with mode
        for col in categorical_columns:
            mode = self.df[col].mode()
            if not mode.empty:
                self.df[col].fillna(mode[0], inplace=True)
            else:
                self.df[col].fillna("Unknown", inplace=True)

        print("Missing values handled successfully.")

    def remove_duplicates(self):
        """Remove duplicate rows."""

        before = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        after = self.df.shape[0]

        print(f"Removed {before-after} duplicate rows.")

    def clean_text(self):
        """Remove extra spaces."""

        object_columns = self.df.select_dtypes(include="object").columns

        for col in object_columns:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )

    def convert_dates(self):
        """Convert date columns."""

        for col in self.df.columns:

            if "date" in col.lower():

                self.df[col] = pd.to_datetime(
                    self.df[col],
                    errors="coerce"
                )

        print("Date columns standardized.")

    def remove_duplicate_ids(self):

        possible_ids = [
            "OrderID",
            "Order ID",
            "CustomerID",
            "Customer ID",
            "ID"
        ]

        for col in possible_ids:

            if col in self.df.columns:

                before = len(self.df)

                self.df.drop_duplicates(
                    subset=col,
                    inplace=True
                )

                after = len(self.df)

                print(f"{before-after} duplicate IDs removed from {col}")

    def save_dataset(self, output_file):
        """Save cleaned dataset."""

        self.df.to_csv(output_file, index=False)

        print(f"\nCleaned dataset saved to:\n{output_file}")

    def run(self):

        self.load_data()

        self.dataset_info()

        self.missing_values()

        self.clean_missing_values()

        self.remove_duplicates()

        self.remove_duplicate_ids()

        self.clean_text()

        self.convert_dates()

        self.save_dataset("../data/processed/cleaned_data.csv")


if __name__ == "__main__":

    cleaner = DataCleaner(
        "../data/raw/Dataset for Data Analytics.xlsx"
    )

    cleaner.run()
