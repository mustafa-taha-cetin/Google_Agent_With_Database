# ---------------------------- Ana Kütüphane İçe Aktarımları ----------------------------
import pyodbc
from typing import List, Dict
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext



# ------------------- SQL Server bağlantı bilgileri -------------------

server = 'DESKTOP-H6SIL9M\SQLEXPRESS'
database = 'Akakce'


# ----------------- Ürünleri Veritabanından Çekme Fonksiyonu -----------------

def get_products() -> List[Dict]:
    """
    SQL Server'daki 'Table_Arcelik' tablosundan ürün bilgilerini çeker.
    Bağlantı hatalarını yakalar ve ürün listesini döndürür.
    """
    conn = None
    cursor = None
    products = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Sorguyu çalıştır
        cursor.execute("""
            SELECT 
            Name, Price, Seller, Product_Type, Brand
            FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        # Çekilen veriyi listeye dönüştür
        for row in rows:
            products.append({
                "name": row[0],
                "price": row[1],
                "seller": row[2],
                "product_type": row[3],
                "brand": row[4]
            })

    except pyodbc.Error as ex:
        # Veritabanı bağlantısı veya sorgu hatası durumunda hata mesajını yazdır
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        # Hata durumunda boş liste döndür veya duruma göre özel bir hata fırlat
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return products





# ----------------- Ürünlerin Satıcılarını Bulma Fonksiyonu -----------------

def find_seller() -> List[Dict]:

    conn = None
    cursor = None
    sellers = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Sorguyu çalıştır
        cursor.execute("""
            SELECT Seller FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        # Çekilen veriyi listeye dönüştür
        for row in rows:
            sellers.append({
                "seller": row[0]
            })

    except pyodbc.Error as ex:
        # Veritabanı bağlantısı veya sorgu hatası durumunda hata mesajını yazdır
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        # Hata durumunda boş liste döndür veya duruma göre özel bir hata fırlat
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return sellers






# ----------------- Ürünlerin Markalarını Bulma Fonksiyonu -----------------

def find_brand() -> List[Dict]:

    conn = None
    cursor = None
    brands = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Sorguyu çalıştır
        cursor.execute("""
            SELECT Brand FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        # Çekilen veriyi listeye dönüştür
        for row in rows:
            brands.append({
                "brand": row[0]
            })

    except pyodbc.Error as ex:
        # Veritabanı bağlantısı veya sorgu hatası durumunda hata mesajını yazdır
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        # Hata durumunda boş liste döndür veya duruma göre özel bir hata fırlat
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return brands






# ----------------- Ürünlerin Markalarını Bulma Fonksiyonu -----------------

def find_product_type() -> List[Dict]:

    conn = None
    cursor = None
    product_types = []
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = conn.cursor()

        # Sorguyu çalıştır
        cursor.execute("""
            SELECT Product_Type FROM Table_Arcelik
        """)
        rows = cursor.fetchall()

        # Çekilen veriyi listeye dönüştür
        for row in rows:
            product_types.append({
                "brand": row[0]
            })

    except pyodbc.Error as ex:
        # Veritabanı bağlantısı veya sorgu hatası durumunda hata mesajını yazdır
        sqlstate = ex.args[0]
        print(f"Database error: {sqlstate} - {ex}")
        # Hata durumunda boş liste döndür veya duruma göre özel bir hata fırlat
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return product_types









# ---------------------------- Data Base Agent Tanımı ----------------------------
data_base_agent = Agent(

    model='gemini-2.0-flash-001',

    name='similarty_base_agent',

    description="""A helpful assistant for collecting or selecting data in
    local databases; also, this agent can pull all data from databases.""",

    tools=[get_products, find_seller, find_brand, find_product_type],

    # Ajana hangi durumda hangi aracı kullanacağını belirten talimat

    instruction="""If the user asks for products or data from the database,
                   use the 'get_products' tool to retrieve them don't use any other tools.
                   After fetching, present the product details including
                   Name, Price, Seller, Product Type, and Brand in a clear, readable list format.
                   If no products are found, inform the user that no products were found in the database.
                   On the other hand user can asks for sellers if user asks just seller, use the 'find_seller'
                   for finding sellers but all varibale writed once I mean I don't want to write same seller again,
                   just ordered all sellers, Uppercase or lowercase letters do not prevent them 
                   from being the same group and don't remember that you should remember this is true for all ordered groups.
                   Sometimes user want to see sellers products, In this case you should use
                   'get_products' tool but also use 'find_seller' for understanding all variables and if user ask about
                   both sellers and products firstly you order all seller and find seller's product to use 'get_products' tool
                   then adapt seller order. If user take out one or more row variable you should find it all and then you
                   must don't add lists unless the user states otherwise. If user want to ordered by price you must adapt that
                   I mean you ordered list by price lowest to greatest, if you find same price this is not problem just go ahead your order
                   which one list value upper doesn't matter. User sometimes wants to categorize products ordered by Brand, in this case
                   you should use 'find_brand' tool for categorized products. Also user wants to categorize products ordered by product type,
                   in this case you should use 'find_product_type' tool for categorized products. When user asks all orders like brand and product type
                   you should remember that firstly you categorize ordered by brand then you can ordered by product type and finally you can ordered by
                   seller this is hierarchy and use this hierarchy when user wants two or more order requests.
                   For any other questions, respond politely that this agent specializes in database queries."""

)

root_agent = data_base_agent


