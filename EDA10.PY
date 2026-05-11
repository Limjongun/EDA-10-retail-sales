import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('retail_sales_dataset.csv')

print("head datasests")
print(df.head())

print("tail datasests")
print(df.tail())

print("shape")
print(df.shape)

print("\ncolumn")
print(df.columns)

print("\ninfo")
print(df.info())

print("\ndescribe")
print(df.describe())

print("\n missing value")
print(df.isnull().sum())
missing_percentage = df.isnull().sum()/len(df)*100
print(missing_percentage)

print("duplicated : ",df.duplicated())

#ubah data jadi date time

df['Date'] = pd.to_datetime(df['Date'])
df['year']= df['Date'].dt.year
df['Month']= df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.month_name()
df['Day_Name'] = df['Date'].dt.day_name()

print("\nContoh Kolom Waktu")
print(df[['Date','year','Month','Month_Name','Day_Name']].head())

#analisis fitur kategorikal
kolom_kategorial = ['Gender','Product Category']
for column in kolom_kategorial:
    print(f"value kolom untuk {column}: ")
    print(df[column].value_counts())

    plt.figure(figsize=(7,4))
    sns.countplot(data= df, x = column,order=df[column].value_counts().index)
    plt.title(f"distribusi untuk {column}")
    plt.xlabel(column)
    plt.ylabel("jumblah")
    plt.xticks(rotation = 30)
    plt.show()
    #untuk gender perempuan lebih banyak 
    #produk paling banyak di beli clothing kemudian menyusul electronic
    #produk paling sedikit adalah beuaty

numeric_column = ['Age','Quantity','Price per Unit','Total Amount']
for column in numeric_column:
    plt.figure(figsize=(7,4))
    sns.histplot(data = df, x=column, kde=True)
    plt.title(f"distribusi {column}")
    plt.xlabel(column)
    plt.ylabel("frequency")
    plt.show()

    #data umur konsentrasi di 3 puncak tapi bukan hal yang extreme
    #data quantitas seimbang dari kiri sampai kanan
    #range harga 0-100 jauh lebih banyak dari lainya
    #totaal amount distrbusi di 0-250 membuat data ini skew right

#analisis total amount

print ("\n Statistik total amount :")
print(df['Total Amount'].describe())
plt.figure(figsize=(7,4))
sns.histplot(data = df, x='Total Amount', kde=True)
plt.title("distribusi Total Amount")
plt.xlabel('Total Amount')
plt.ylabel("frequency")
plt.show()
#totaal amount distrbusi di 0-250 membuat data ini skew right

#total sales bedasarkan produk category
sales_by_category = df.groupby('Product Category')['Total Amount'].sum().reset_index()
sales_by_category =  sales_by_category.sort_values(by='Total Amount', ascending= False)
print(sales_by_category)
plt.figure(figsize=(8,5))
sns.barplot(data=sales_by_category, x='Product Category',y='Total Amount')
plt.title("total sales bedasarkan kategori ")
plt.xlabel('product category')
plt.ylabel("total sales")
plt.xticks(rotation=30)
plt.show()
#penjual electronic paling tinggi sales
#jadi electronic punya kontribusi pada revenue tertinggi

sales_by_gender = df.groupby('Gender')['Total Amount'].sum().reset_index()
sales_by_gender =  sales_by_gender.sort_values(by='Total Amount', ascending= False)
print(sales_by_gender)
plt.figure(figsize=(8,5))
sns.barplot(data=sales_by_gender, x='Gender',y='Total Amount')
plt.title("total sales bedasarkan Gender ")
plt.xlabel('Gender')
plt.ylabel("total sales")
plt.xticks(rotation=30)
plt.show()

#gender wanita memberikan total sales yang lebih tinngi dari pada pria

#boxplot amount dan product category

plt.figure(figsize=(8,5))
sns.boxplot(data = df, x ='Product Category',y = 'Total Amount')
plt.title("distribusi total amount bedasarkan product category ")
plt.xlabel('product category')
plt.ylabel("total amount")
plt.xticks(rotation=30)
plt.show()
#electronic unngul dari lain tapi selisih dengan beauty sedikit

#scatter plot age vs total amount

plt.figure(figsize=(7,5))
sns.scatterplot(data = df, x ='Age',y = 'Total Amount',hue='Gender',alpha=0.7)
plt.title("age vs total amount ")
plt.xlabel('Age')
plt.ylabel("Total Amount")

plt.show()

plt.figure(figsize=(7,5))
sns.scatterplot(data = df, x ='Quantity',y = 'Total Amount',hue='Gender',alpha=0.7)
plt.title("Quantity vs total amount ")
plt.xlabel('Quantity')
plt.ylabel("Total Amount")

plt.show()

#totaal sales perbulan

sales_bulanan = df.groupby('Month')['Total Amount'].sum().reset_index()
print("sales bulanan")
print(sales_bulanan)

plt.figure(figsize=(10,5))
sns.lineplot(data = sales_bulanan, x ='Month',y = 'Total Amount',hue='Gender',alpha=0.7)
plt.title("Total sales bulanan : ")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.show()

transaksi_bulanan = df.groupby('Month')['Transaction ID'].count().reset_index()
transaksi_bulanan.rename(column={'Transaction ID' : 'Transaction Count'}, inplace= True)
print("jumblah transaaksi bulanan : ")
print(transaksi_bulanan)
plt.figure(figsize=(10,5))
sns.lineplot(data = transaksi_bulanan, x ='Month',y = 'Transaction Count',marker='o')
plt.title("Transaksi per bulan : ")
plt.xlabel("Month")
plt.ylabel("Transaction Count")

plt.show()

numeric_df = df.select_dtypes(include=['int64','float64'])
corelation = numeric_df.corr()
print("\n corelation matrix")
print(corelation)

plt.figure(figsize=(8,5))
sns.heatmap(corelation , annot= True ,fmt=".2f")
plt.title("corelaation heatmap retail sales : ")
plt.show

# cek validasi total amount 

df['Calculated Total'] = df['Quantity'] * df['Price per Unit']
df['Total Match'] =  df['Calculated Total']==df['Total Amount']

print("\n cek apakah total amount sesuai quantity x price per units")
print(df['Total Match'].value_counts())
missmatch = df[df['Total Match'] == False]
print("\n data yang total amount nya tidak sesuai")
print(missmatch)


print("""

Ringkasan Insight yang Didapatkan

1. Dataset memiliki 1.000 baris dan 9 kolom.
2. Tidak terdapat missing value pada dataset.
3. Tidak terdapat data duplikat pada dataset.
4. Dataset terdiri dari 5 kolom numerik dan 4 kolom kategorikal.
5. Kolom Gender didominasi oleh Female sebanyak 510 data, sedangkan Male sebanyak 490 data.
6. Kolom Product Category didominasi oleh Clothing sebanyak 351 data, diikuti Electronics sebanyak 342 data, dan Beauty sebanyak 307 data.
7. Distribusi Age memiliki beberapa puncak, terutama pada rentang usia sekitar 20, 40, dan 60 tahun.
8. Distribusi Quantity terlihat cukup merata dari nilai rendah hingga tinggi.
9. Distribusi Price per Unit cenderung right-skewed, dengan jumlah data terbanyak berada pada rentang harga 0–100.
10. Distribusi Total Amount juga cenderung right-skewed, dengan konsentrasi data terbanyak pada rentang 0–250.
11. Berdasarkan total sales, kategori Electronics memberikan kontribusi revenue tertinggi.
12. Berdasarkan Gender, pelanggan Female memberikan total sales lebih tinggi dibandingkan Male, tetapi selisihnya tidak terlalu besar.
13. Pada boxplot Total Amount berdasarkan Product Category, kategori Electronics menunjukkan median yang relatif lebih tinggi dibandingkan kategori lain.
14. Scatter plot Age vs Total Amount tidak menunjukkan pola hubungan yang jelas.
15. Scatter plot Quantity vs Total Amount menunjukkan hubungan positif, tetapi Total Amount tetap dipengaruhi juga oleh Price per Unit.
16. Analisis bulanan dapat digunakan untuk melihat tren penjualan dan jumlah transaksi dari bulan ke bulan.
17. Correlation heatmap membantu melihat hubungan antar fitur numerik dalam dataset.
18. Validasi Total Amount menunjukkan apakah nilai Total Amount sudah sesuai dengan hasil Quantity × Price per Unit.

Kesimpulan:
Dataset retail sales ini cukup bersih karena tidak memiliki missing value maupun duplikasi.
Dari hasil EDA, kategori Electronics menjadi penyumbang total sales tertinggi.
Pelanggan Female sedikit lebih dominan dalam jumlah maupun kontribusi penjualan.
Secara umum, Total Amount lebih dipengaruhi oleh kombinasi Quantity dan Price per Unit,
sedangkan Age tidak menunjukkan hubungan yang kuat terhadap nilai transaksi.

""")
