import pandas as pd

# Load dataset
df = pd.read_csv("books_scraped_data_complete.csv")

print(df.head())
print("Original shape:", df.shape)


# Select useful columns
custom_df = df[
    [
        "Title",
        "Price",
        "Rating",
        "Availability",
        "Product Type"
    ]
].copy()


# Clean Price
custom_df["Price"] = (
    custom_df["Price"]
    .str.replace("Â£", "", regex=False)
    .str.strip()
    .astype(float)
)


# Check custom dataset
print("\nCustom Dataset:")
print(custom_df.head())

print("\nShape:")
print(custom_df.shape)

print("\nData Types:")
print(custom_df.dtypes)

print("\nMissing Values:")
print(custom_df.isnull().sum())


# Save custom dataset
custom_df.to_csv(
    "books_custom_analysis_dataset.csv",
    index=False
)

print("\nCustom dataset created successfully!")