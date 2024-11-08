
#main.py

from utilsPackage.utils import get_db_connection  # Importing the connection function from utils
import pyodbc #For Question 2
import random

def fetch_data(query):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
        return None

def main():
    # 1
    query_products = """
    SELECT ProductID, [UPC-A], Description, ManufacturerID, BrandID 
    FROM tProduct
    """
    products = fetch_data(query_products)

    # 2
    if products:
        selected_product = random.choice(products) 
        ProductID = selected_product[0]  
        Description = selected_product[2]  
        ManufacturerID = selected_product[3]  
        BrandID = selected_product[4]  

    # 3
        query_manufacturer = f"""
        SELECT Manufacturer
        FROM tManufacturer
        WHERE ManufacturerID = {ManufacturerID}
        """
       
    # 4 Manufacturer name
        manufacturer = fetch_data(query_manufacturer)
        manufacturer_name = manufacturer[0][0] if manufacturer else "Unknown Manufacturer"

    # 5 
        query_brand = f"""
        SELECT Brand
        FROM tBrand
        WHERE BrandID = {BrandID}
        """
        # Fetch brand name
        brand = fetch_data(query_brand)
        brand_name = brand[0][0] if brand else "Unknown Brand"
    # 6
        query_sales = f"""
        SELECT TOP (100) PERCENT SUM(dbo.tTransactionDetail.QtyOfProduct) AS NumberOfItemsSold
        FROM dbo.tTransactionDetail
        INNER JOIN dbo.tTransaction ON dbo.tTransactionDetail.TransactionID = dbo.tTransaction.TransactionID
        WHERE (dbo.tTransaction.TransactionTypeID = 1) AND (dbo.tTransactionDetail.ProductID = {ProductID})
        """
       
        # Total quantity sold
        sales_data = fetch_data(query_sales)
        total_sold = sales_data[0][0] if sales_data else 0 

    # 7
        output_sentence = (
            f"The product '{Description}' from {manufacturer_name} under the brand '{brand_name}' "
            f"has sold a total of {total_sold} items."
        )

        # Print the string sentence
        print(output_sentence)
    else:
        print("No products found.")


if __name__ == "__main__":
    main()