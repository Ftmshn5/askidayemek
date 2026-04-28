"""
Askıda Yemek (Food Bridge) - Ana Flask Uygulaması

Fırat Üniversitesi Teknoloji Fakültesi
Yazılım Mühendisliği Bölümü
YMH220 İleri Programlama Teknikleri

localhost:5000 adresinde web browser'da çalışır.
"""

import io
import csv
import json
from datetime import datetime, timezone, timedelta

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session, make_response
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)

from config import Config
from models import db, User, Restaurant, Product, Transaction
from algorithms import (
    calculate_priority_score,
    get_urgent_products_heap,
    greedy_matching,
    run_batch_matching,
    auto_suspend_expiring_products,
    get_impact_stats
)
from seed_data import seed_database

# ============================================
# UYGULAMA OLUŞTURMA
# ============================================

app = Flask(__name__)
app.config.from_object(Config)

# Veritabanı başlatma
db.init_app(app)

# Login Manager başlatma
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login için kullanıcı yükleme."""
    return User.query.get(int(user_id))


# ============================================
# ÇOKLU DİL DESTEĞİ (i18n)
# ============================================

with open('translations.json', 'r', encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

def get_lang():
    """Kullanıcının seçtiği dili döndürür."""
    return session.get('lang', 'tr')

def get_translations():
    """Aktif dilin çeviri sözlüğünü döndürür."""
    lang = get_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS['tr'])

@app.context_processor
def inject_translations():
    """Tüm template'lere otomatik olarak `t` ve `lang` değişkeni gönderir."""
    return {'t': get_translations(), 'lang': get_lang()}

@app.route('/set_lang/<lang_code>')
def set_lang(lang_code):
    """Dil değiştirme."""
    if lang_code in ['tr', 'en']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))


# ============================================
# ANA ROUTE'LAR
# ============================================

@app.route('/')
def index():
    """Ana sayfa - Login'e yönlendir."""
    if current_user.is_authenticated:
        if current_user.role == 'owner':
            return redirect(url_for('owner_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('owner_dashboard') if current_user.role == 'owner' else url_for('user_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(username=username, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Hoş geldiniz, {user.full_name}!', 'success')
            return redirect(url_for('owner_dashboard') if role == 'owner' else url_for('user_dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kayıt sayfası."""
    if current_user.is_authenticated:
        return redirect(url_for('owner_dashboard') if current_user.role == 'owner' else url_for('user_dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        restaurant_name = request.form.get('restaurant_name')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Bu kullanıcı adı zaten alınmış.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            full_name=full_name,
            role=role,
            user_type='standard'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        if role == 'owner' and restaurant_name:
            # Rastgele koordinatlarla restoran oluştur (Elazığ merkez)
            import random
            lat = 38.6748 + random.uniform(-0.02, 0.02)
            lon = 39.1920 + random.uniform(-0.02, 0.02)
            new_restaurant = Restaurant(
                owner_id=new_user.id,
                name=restaurant_name,
                latitude=lat,
                longitude=lon,
                address='Elazığ Merkez'
            )
            db.session.add(new_restaurant)
            db.session.commit()

        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Çıkış yap."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/guest/dashboard')
def guest_dashboard():
    """
    Misafir Kullanıcı Dashboard (Sadece Görüntüleme).
    """
    # Otomatik SKT kontrolü
    auto_suspend_expiring_products()
    return render_template('user/dashboard.html', is_guest=True)

# ============================================
# KULLANICI (İHTİYAÇ SAHİBİ) ROUTE'LARI
# ============================================

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """
    Harita Keşfi Dashboard.
    Wireframe: Map Dashboard - OpenStreetMap harita + restoran marker'ları
    """
    if current_user.role != 'user':
        return redirect(url_for('owner_dashboard'))

    return render_template('user/dashboard.html')


@app.route('/user/profile')
@login_required
def user_profile():
    """
    Kullanıcı Profil Sayfası.
    Wireframe: Profil Bilgileri - isim, tip, puan, talep sayısı
    """
    if current_user.role != 'user':
        return redirect(url_for('owner_dashboard'))

    total_requests = Transaction.query.filter_by(user_id=current_user.id).count()
    
    # Teslim Alınmayı Bekleyen (PIN ile) Talepler
    active_transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        status='matched'
    ).order_by(Transaction.matched_at.desc()).all()

    # Teslim Alınmış ama Puanlanmamış Talepler
    completed_transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        status='completed',
        user_rating=None
    ).order_by(Transaction.completed_at.desc()).limit(5).all()

    return render_template(
        'user/profile.html', 
        total_requests=total_requests,
        active_transactions=active_transactions,
        completed_transactions=completed_transactions
    )


@app.route('/user/report')
@login_required
def user_report():
    """
    Etki Raporu.
    Wireframe: Toplumsal Etki - istatistikler + grafik
    """
    if current_user.role != 'user':
        return redirect(url_for('owner_dashboard'))

    stats = get_impact_stats(user_id=current_user.id)

    return render_template('user/report.html', stats=stats)


# ============================================
# RESTORAN SAHİBİ (OWNER) ROUTE'LARI
# ============================================

@app.route('/owner/dashboard')
@login_required
def owner_dashboard():
    """
    Restoran Yönetim Paneli.
    Wireframe: Genel Bakış + Envanter tablosu
    """
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()

    if not restaurant:
        flash('Henüz bir restoranınız bulunmuyor.', 'warning')
        return render_template('owner/dashboard.html', restaurant=None, products=[])

    products = Product.query.filter_by(restaurant_id=restaurant.id).order_by(
        Product.skt_date.asc()
    ).all()

    # İstatistikler (Wireframe: Genel Bakış kartları)
    total_products = len(products)
    suspended_count = sum(1 for p in products if p.status == 'suspended')
    today_donations = Transaction.query.filter(
        Transaction.restaurant_id == restaurant.id,
        Transaction.status.in_(['matched', 'completed']),
        Transaction.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    ).count()
    now_utc = datetime.now(timezone.utc)
    critical_skt = sum(
        1 for p in products
        if p.status == 'on_sale' and
        (p.skt_date.replace(tzinfo=timezone.utc) if p.skt_date.tzinfo is None else p.skt_date) <= now_utc + timedelta(hours=6)
    )

    stats = {
        'total_products': total_products,
        'suspended_count': suspended_count,
        'today_donations': today_donations,
        'critical_skt': critical_skt
    }

    # Teslimat Bekleyen Talepler
    pending_transactions = Transaction.query.filter(
        Transaction.restaurant_id == restaurant.id,
        Transaction.status == 'matched'
    ).order_by(Transaction.matched_at.desc()).all()

    return render_template(
        'owner/dashboard.html',
        restaurant=restaurant,
        products=products,
        stats=stats,
        pending_transactions=pending_transactions
    )


@app.route('/owner/product/add', methods=['POST'])
@login_required
def owner_add_product():
    """
    Yeni ürün ekleme.
    Wireframe: Yeni Ürün Ekle modal formu
    """
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        flash('Restoran bulunamadı!', 'error')
        return redirect(url_for('owner_dashboard'))

    name = request.form.get('name', '').strip()
    quantity = int(request.form.get('quantity', 1))
    original_price = float(request.form.get('original_price', 0))
    price = float(request.form.get('price', 0))
    skt_date_str = request.form.get('skt_date', '')
    status = request.form.get('status', 'on_sale')

    if not name or not skt_date_str:
        flash('Ürün adı ve SKT zorunludur!', 'error')
        return redirect(url_for('owner_dashboard'))

    try:
        skt_date = datetime.strptime(skt_date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except ValueError:
        flash('Geçersiz tarih formatı!', 'error')
        return redirect(url_for('owner_dashboard'))

    product = Product(
        restaurant_id=restaurant.id,
        name=name,
        quantity=quantity,
        original_price=original_price,
        price=price,
        skt_date=skt_date,
        status=status
    )

    db.session.add(product)
    db.session.commit()

    flash(f'"{name}" başarıyla eklendi!', 'success')
    return redirect(url_for('owner_dashboard'))


@app.route('/owner/product/toggle/<int:product_id>', methods=['POST'])
@login_required
def owner_toggle_product(product_id):
    """
    Ürün durumunu değiştir (Satışta ↔ Askıda).
    Wireframe: Envanter tablosundaki durum toggle
    """
    product = Product.query.get_or_404(product_id)

    # Yetki kontrolü
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant or product.restaurant_id != restaurant.id:
        flash('Bu ürünü değiştirme yetkiniz yok!', 'error')
        return redirect(url_for('owner_dashboard'))

    if product.status == 'on_sale':
        product.status = 'suspended'
        flash(f'"{product.name}" askıya alındı.', 'success')
    elif product.status == 'suspended':
        product.status = 'on_sale'
        flash(f'"{product.name}" satışa alındı.', 'info')

    db.session.commit()
    return redirect(url_for('owner_dashboard'))


@app.route('/owner/delete_product/<int:product_id>', methods=['POST'])
@login_required
def owner_delete_product(product_id):
    """Ürün sil."""
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    product = Product.query.get_or_404(product_id)
    if product.restaurant.owner_id != current_user.id:
        flash('Yetkisiz işlem.', 'error')
        return redirect(url_for('owner_dashboard'))

    db.session.delete(product)
    db.session.commit()
    flash('Ürün silindi.', 'success')
    return redirect(url_for('owner_dashboard'))


@app.route('/owner/verify_pin', methods=['POST'])
@login_required
def owner_verify_pin():
    """Teslimat için PIN kodu doğrula."""
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    pin_code = request.form.get('pin_code')
    transaction_id = request.form.get('transaction_id')
    
    if not pin_code or not transaction_id:
        flash('Geçersiz istek.', 'error')
        return redirect(url_for('owner_dashboard'))
        
    transaction = Transaction.query.get_or_404(transaction_id)
    
    if transaction.restaurant.owner_id != current_user.id:
        flash('Yetkisiz işlem.', 'error')
        return redirect(url_for('owner_dashboard'))
        
    if transaction.status != 'matched':
        flash('Bu işlem teslimat bekleyen durumunda değil.', 'error')
        return redirect(url_for('owner_dashboard'))
        
    if transaction.pin_code != pin_code:
        flash('Hatalı PIN kodu!', 'error')
        return redirect(url_for('owner_dashboard'))
        
    # Başarılı Teslimat
    transaction.status = 'completed'
    transaction.completed_at = datetime.now(timezone.utc)
    transaction.product.status = 'completed'
    
    # Kullanıcıya güven puanı ver
    if transaction.user:
        transaction.user.points += 10
        
    db.session.commit()
    flash('PIN Doğrulandı! Teslimat başarılı, kullanıcıya +10 Güven Puanı eklendi.', 'success')
    return redirect(url_for('owner_dashboard'))


@app.route('/owner/report')
@login_required
def owner_report():
    """
    Raporlama ve Analiz Ekranı.
    Wireframe: Toplumsal Etki + grafik + CSV indirme
    """
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    stats = get_impact_stats(
        restaurant_id=restaurant.id if restaurant else None
    )

    return render_template('owner/report.html', stats=stats, restaurant=restaurant)


@app.route('/owner/profile')
@login_required
def owner_profile():
    """
    Owner Profil Sayfası.
    Wireframe: Profil - isim, tip, puan
    """
    if current_user.role != 'owner':
        return redirect(url_for('user_dashboard'))

    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    total_donations = 0
    if restaurant:
        total_donations = Transaction.query.filter(
            Transaction.restaurant_id == restaurant.id,
            Transaction.status.in_(['matched', 'completed'])
        ).count()

    return render_template(
        'owner/profile.html',
        restaurant=restaurant,
        total_donations=total_donations
    )


# ============================================
# API ROUTE'LARI
# ============================================

@app.route('/api/restaurants')
def api_restaurants():
    """
    Harita için restoran verilerini JSON olarak döndür.
    Wireframe: Map Dashboard - marker'lar için veri
    """
    restaurants = Restaurant.query.all()
    data = []
    for r in restaurants:
        suspended = Product.query.filter_by(
            restaurant_id=r.id, status='suspended'
        ).count()

        data.append({
            'id': r.id,
            'name': r.name,
            'lat': r.latitude,
            'lon': r.longitude,
            'rating': r.rating,
            'address': r.address,
            'suspended_count': suspended,
            'has_suspended': suspended > 0
        })

    return jsonify(data)


@app.route('/api/products/<int:restaurant_id>')
def api_products(restaurant_id):
    """
    Belirli bir restoranın askıdaki ürünlerini döndür.
    Wireframe: Ürün Detay ve Talep Modalı
    """
    restaurant = Restaurant.query.get_or_404(restaurant_id)

    products = Product.query.filter_by(
        restaurant_id=restaurant_id,
        status='suspended'
    ).order_by(Product.skt_date.asc()).all()

    # Mevcut talep sayısı (kuyruk)
    queue_count = Transaction.query.filter(
        Transaction.product_id.in_([p.id for p in products]),
        Transaction.status == 'pending'
    ).count() if products else 0

    data = {
        'restaurant': {
            'id': restaurant.id,
            'name': restaurant.name,
            'rating': restaurant.rating,
            'address': restaurant.address
        },
        'products': [{
            'id': p.id,
            'name': p.name,
            'quantity': p.quantity,
            'original_price': p.original_price,
            'price': p.price,
            'skt_date': p.skt_date.strftime('%Y-%m-%d %H:%M'),
        } for p in products],
        'queue_count': queue_count
    }

    return jsonify(data)


@app.route('/api/request', methods=['POST'])
@login_required
def api_create_request():
    """
    Talep oluşturma.
    Wireframe: "Seçimleri Kaydet" butonu

    Teknik Rapor - Bölüm 4.2:
    Kullanıcının tipi üzerinden Öncelik Skoru hesaplanır.
    """
    if current_user.role != 'user':
        return jsonify({'error': 'Yetkiniz yok'}), 403

    data = request.get_json()
    product_ids = data.get('product_ids', [])

    if not product_ids:
        return jsonify({'error': 'En az bir ürün seçmelisiniz'}), 400

    if len(product_ids) > 3:
        return jsonify({'error': 'Tek seferde en fazla 3 ürün seçebilirsiniz'}), 400
        
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Günlük 3 İstek Limiti (Anti-Spam)
    daily_requests = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.created_at >= today_start
    ).count()
    
    if daily_requests >= 3:
        return jsonify({'error': 'Günlük maksimum 3 restoran talep limitine ulaştınız.'}), 400


    created_transactions = []

    for pid in product_ids:
        product = Product.query.get(pid)
        if not product or product.status != 'suspended':
            continue

        # Aynı ürüne daha önce talep var mı kontrol et
        existing = Transaction.query.filter_by(
            user_id=current_user.id,
            product_id=pid,
            status='pending'
        ).first()

        if existing:
            continue

        # Öncelik skoru hesapla
        priority = calculate_priority_score(current_user, now, now)

        transaction = Transaction(
            user_id=current_user.id,
            product_id=pid,
            restaurant_id=product.restaurant_id,
            priority_score=priority,
            status='pending',
            created_at=now
        )

        db.session.add(transaction)
        created_transactions.append({
            'id': pid,
            'name': product.name,
            'priority_score': priority
        })

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'{len(created_transactions)} ürün için talep oluşturuldu.',
        'transactions': created_transactions,
        'matched_count': 0
    })

@app.route('/api/rate_transaction', methods=['POST'])
@login_required
def api_rate_transaction():
    """Kullanıcının teslim aldığı işlemi puanlaması."""
    if current_user.role != 'user':
        return jsonify({'error': 'Yetkiniz yok'}), 403

    data = request.get_json()
    transaction_id = data.get('transaction_id')
    rating = data.get('rating')

    if not transaction_id or not rating:
        return jsonify({'error': 'Eksik veri'}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except ValueError:
        return jsonify({'error': 'Geçersiz puan'}), 400

    transaction = Transaction.query.get(transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        return jsonify({'error': 'İşlem bulunamadı'}), 404

    if transaction.status != 'completed':
        return jsonify({'error': 'Sadece teslim alınmış işlemleri puanlayabilirsiniz'}), 400

    if transaction.user_rating:
        return jsonify({'error': 'Bu işlemi zaten puanladınız'}), 400

    transaction.user_rating = rating
    current_user.points += 5  # Puan verdiği için ödül puan
    
    db.session.commit()

    return jsonify({'success': True, 'message': 'Puanınız kaydedildi, +5 Güven Puanı kazandınız!'})


@app.route('/api/export/csv')
@login_required
def api_export_csv():
    """
    CSV dışa aktarma.
    Wireframe: "CSV İndir" butonu
    Teknik Rapor - Bölüm 3: Pandas ile raporlama ve CSV çıktısı
    """
    import pandas as pd

    if current_user.role == 'owner':
        restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
        query = Transaction.query.filter_by(restaurant_id=restaurant.id) if restaurant else Transaction.query
    else:
        query = Transaction.query.filter_by(user_id=current_user.id)

    transactions = query.filter(
        Transaction.status.in_(['matched', 'completed'])
    ).all()

    # Pandas DataFrame oluştur
    data_rows = []
    for t in transactions:
        product = Product.query.get(t.product_id)
        user = User.query.get(t.user_id)
        restaurant = Restaurant.query.get(t.restaurant_id)

        data_rows.append({
            'İşlem ID': t.id,
            'Tarih': t.created_at.strftime('%Y-%m-%d %H:%M'),
            'Kullanıcı': user.full_name if user else '-',
            'Restoran': restaurant.name if restaurant else '-',
            'Ürün': product.name if product else '-',
            'Miktar': product.quantity if product else 0,
            'Öncelik Skoru': t.priority_score,
            'Durum': t.status,
            'Eşleşme Tarihi': t.matched_at.strftime('%Y-%m-%d %H:%M') if t.matched_at else '-'
        })

    df = pd.DataFrame(data_rows)

    # CSV oluştur
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')

    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = 'attachment; filename=askida_yemek_rapor.csv'

    return response


# ============================================
# UYGULAMA BAŞLATMA VE SCHEDULER
# ============================================

from apscheduler.schedulers.background import BackgroundScheduler
import os

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Uygulama context'ine ihtiyaç duyulduğu için, app objesini içine pass eden sarmalayıcılar
    def suspend_job():
        with app.app_context():
            auto_suspend_expiring_products()
            
    def match_job():
        with app.app_context():
            run_batch_matching()
            
    scheduler.add_job(func=suspend_job, trigger="interval", minutes=5, id="check_skt")
    scheduler.add_job(func=match_job, trigger="interval", minutes=1, id="greedy_match")
    scheduler.start()

with app.app_context():
    db.create_all()
    seed_database()

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  🍽️  ASKIDA YEMEK (FOOD BRIDGE)")
    print("  📍 http://localhost:5000")
    print("=" * 50)
    print("\n  Demo Hesaplar:")
    print("  ─────────────────────────────────")
    print("  👨‍🍳 Restoran:  lezzet_sofrasi / 123456")
    print("  👤 Kullanıcı: ahmet_yilmaz / 123456")
    print("=" * 50 + "\n")

    # Prevent running scheduler twice in debug mode
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_scheduler()

    app.run(debug=True, host='0.0.0.0', port=5000)
