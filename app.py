from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def initialize_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            product_no TEXT,
            description TEXT,
            price REAL,
            image_url TEXT,
            category TEXT
                   
        )
    ''')

    products_data = [
        ('Siyah İnci ', 'Siyah-beyaz Pamuklu Düğmeli Biyeli Pijama Takım 7314', 185.91, 'https://cdn.dsmcdn.com/ty712/product/media/images/20230203/15/272837558/212232897/1/1_org_zoom.jpg', 'Pijama'),
        ('TRENDYOLMİLLA ', 'Siyah Toparlayıcı Beli Lastikli Yüksek Bel Örme Tayt TWOAW20TA0087', 199.99, 'https://cdn.dsmcdn.com/ty508/product/media/images/20220815/16/160229309/56696304/2/2_org_zoom.jpg', 'Tayt'),
        ('EnModaStyle', 'Nathia Outdoors Kadın Polo Yaka Çizgili Triko Kazak enmoda01', 88, 'https://cdn.dsmcdn.com/ty1016/product/media/images/prod/SPM/PIM/20231014/11/42111c69-13d2-3c3a-afe6-fbd7c99bd9b4/1_org_zoom.jpg', 'Kazak'),
        ('FV', 'Palazzo Pantolon Oversize Orjinal Kesim Plz', 249.99, 'https://cdn.dsmcdn.com/ty1009/product/media/images/prod/SPM/PIM/20231005/15/827227af-1a7d-343f-b893-940ace69b97b/1_org_zoom.jpg', 'Pantolon'),
         ('Color Socks', '5 Çift Termal Kadın Havlu Kışlık Çorap (ISI EMİCİ) colorkıs02', 89.90, 'https://cdn.dsmcdn.com/ty1019/product/media/images/prod/SPM/PIM/20231020/21/eede18cb-1d41-355b-ad01-a31d8bbbf0a5/1_org_zoom.jpg', 'Çorap'),
        ('HOLLY LOLLY', 'Çan Model A Kesim Mini Kaşe Mira Etek Gri HLFW24-00042', 769.90, 'https://cdn.dsmcdn.com/ty1098/product/media/images/prod/SPM/PIM/20231221/17/c721af4f-9a17-3ec9-8a95-824e067552cc/1_org_zoom.jpg', 'Etek'),
        ('XHAN', 'Çiçek Desenli Kruvaze Elbise 9YXK6-41729-02', 238.55, 'https://cdn.dsmcdn.com/ty1002/product/media/images/prod/SPM/PIM/20230922/12/3f1eda35-4b07-3f49-81ad-a53e3cb0f2b1/1_org_zoom.jpg', 'Elbise'),
        ('armonika', 'Kadın Siyah Bahçivan Tulum ARM-20K001117', 169.95, 'https://cdn.dsmcdn.com/ty989/product/media/images/prod/SPM/PIM/20230821/12/0b53646d-af63-396c-b8ab-4eaec266b12e/1_org_zoom.jpg', 'Tulum'),
        ('Pull & Bear', 'Basic oversize bisiklet yaka sweatshirt 07593309', 640, 'https://cdn.dsmcdn.com/ty981/product/media/images/20230808/15/401270561/987716289/1/1_org_zoom.jpg', 'Sweatshirt'),
        ('Stradivarius ', 'Regular Fit Denim Gömlek TYCKQ6X80N169165787012883', 455.97, 'https://cdn.dsmcdn.com/ty994/product/media/images/prod/SPM/PIM/20230831/11/e5f5206f-85a1-3226-865c-3e14bce6f4ec/1_org_zoom.jpg', 'Gömlek')

        
    ]

    cursor.execute('DELETE FROM products')
    cursor.executemany('''
        INSERT INTO products (product_no, description, price, image_url, category)
        VALUES (?, ?, ?, ?, ?)
    ''', products_data)

    conn.commit()
    conn.close()

initialize_database()

@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        query = request.form['query']
        searchQuert = 'SELECT * FROM products WHERE REPLACE(UPPER(product_no),\'İ\',\'I\') LIKE \'replace1\' OR UPPER(description) LIKE \'replace1\' OR UPPER(category) LIKE \'replace1\''
        searchQuert = searchQuert.replace('replace1','%'+query.upper().replace('İ','I')+'%')
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute(searchQuert)
        search_results = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', search_results=search_results)
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)





