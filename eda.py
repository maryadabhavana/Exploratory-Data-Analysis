"""
Exploratory Data Analysis (EDA)

Author: Maryada Bhavana Reddy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

plt.style.use("ggplot")


class ExploratoryDataAnalysis:

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def dataset_overview(self):

        print("=" * 60)

        print("Dataset Overview")

        print("=" * 60)

        print(self.df.head())

        print("\nShape")

        print(self.df.shape)

        print("\nColumns")

        print(self.df.columns)

    def summary_statistics(self):

        print("=" * 60)

        print("Summary Statistics")

        print(self.df.describe(include="all"))

    def missing_values(self):

        missing = self.df.isnull().sum()

        print(missing)

        plt.figure(figsize=(12,6))

        sns.barplot(
            x=missing.index,
            y=missing.values
        )

        plt.xticks(rotation=90)

        plt.title("Missing Values")

        plt.tight_layout()

        plt.savefig("../visualizations/missing_values.png")

        plt.close()

    def missing_matrix(self):

        msno.matrix(self.df)

        plt.savefig("../visualizations/missing_matrix.png")

        plt.close()

    def correlation_matrix(self):

        numeric = self.df.select_dtypes(include="number")

        if numeric.empty:
            print("No numeric columns found.")
            return

        plt.figure(figsize=(10,8))

        sns.heatmap(
            numeric.corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Matrix")

        plt.tight_layout()

        plt.savefig(
            "../visualizations/correlation_heatmap.png"
        )

        plt.close()

    def histograms(self):

        numeric = self.df.select_dtypes(include="number")

        numeric.hist(
            figsize=(14,10),
            bins=20
        )

        plt.tight_layout()

        plt.savefig("../visualizations/histograms.png")

        plt.close()

    def boxplots(self):

        numeric = self.df.select_dtypes(include="number")

        for col in numeric.columns:

            plt.figure(figsize=(6,4))

            sns.boxplot(x=self.df[col])

            plt.title(col)

            plt.savefig(
                f"../visualizations/{col}_boxplot.png"
            )

            plt.close()

    def categorical_analysis(self):

        categorical = self.df.select_dtypes(include="object")

        for col in categorical.columns[:5]:

            plt.figure(figsize=(8,5))

            self.df[col].value_counts().head(10).plot(
                kind="bar"
            )

            plt.title(col)

            plt.tight_layout()

            plt.savefig(
                f"../visualizations/{col}_countplot.png"
            )

            plt.close()

    def outliers(self):

        numeric = self.df.select_dtypes(include="number")

        print("\nPotential Outliers")

        for col in numeric.columns:

            q1 = self.df[col].quantile(0.25)

            q3 = self.df[col].quantile(0.75)

            iqr = q3 - q1

            outliers = self.df[
                (self.df[col] < q1 - 1.5 * iqr) |
                (self.df[col] > q3 + 1.5 * iqr)
            ]

            print(f"{col}: {len(outliers)}")

    def run(self):

        self.dataset_overview()

        self.summary_statistics()

        self.missing_values()

        self.missing_matrix()

        self.correlation_matrix()

        self.histograms()

        self.boxplots()

        self.categorical_analysis()

        self.outliers()


if __name__ == "__main__":

    analysis = ExploratoryDataAnalysis(
        "../data/processed/cleaned_data.csv"
    )

    analysis.run()
