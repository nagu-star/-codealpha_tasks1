import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 1. Load your existing scraped dataset
input_file = 'books_scraped_data.csv'
df = pd.read_csv(input_file)

# Ensure target columns exist in the dataframe
target_columns = ['UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Number of Reviews']
for col in target_columns:
    if col not in df.columns:
        df[col] = None

print(f"Starting to scrape product details for {len(df)} books...\n")

# 2. Iterate through every row with error handling
for index, row in df.iterrows():
    url = row['Product URL']
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Locate the product information table on the page
            table = soup.find('table', {'class': 'table table-striped'})
            if table:
                rows = table.find_all('tr')
                details = {}
                for tr in rows:
                    th = tr.find('th').text.strip()
                    td = tr.find('td').text.strip()
                    details[th] = td
                
                # Map HTML table labels to your CSV column names
                df.at[index, 'UPC'] = details.get('UPC')
                df.at[index, 'Product Type'] = details.get('Product Type')
                df.at[index, 'Price (excl. tax)'] = details.get('Price (excl. tax)')
                df.at[index, 'Price (incl. tax)'] = details.get('Price (incl. tax)')
                df.at[index, 'Tax'] = details.get('Tax')
                df.at[index, 'Number of Reviews'] = details.get('Number of reviews')
                
        else:
            print(f"Failed to fetch {url} (Status code: {response.status_code})")
            
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        
    # Print progress every 50 books and save an incremental backup
    if (index + 1) % 50 == 0:
        print(f"Processed {index + 1} / {len(df)} books...")
        df.to_csv('books_scraped_data_in_progress.csv', index=False)
        
    # Be polite to the server to prevent getting blocked
    time.sleep(0.5)

# 3. Save the fully updated final dataset
output_file = 'books_scraped_data_complete.csv'
df.to_csv(output_file, index=False)
print(f"\nScraping complete! Saved successfully as '{output_file}'.")