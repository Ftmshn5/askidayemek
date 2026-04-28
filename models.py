"""
Askıda Yemek (Food Bridge) - Veritabanı Modelleri
SQLAlchemy ORM ile tanımlanan tüm veritabanı tabloları.

Tablolar:
    - User: Kullanıcı bilgileri (hem ihtiyaç sahibi hem restoran sahibi)
    - Restaurant: Restoran bilgileri ve koordinatları
    - Product: Ürün envanteri, SKT ve durum bilgileri
    - Transaction: Talep ve eşleştirme işlemleri
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Kullanıcı modeli.
    Teknik Rapor - Bölüm 6: Users Table
    Wireframe: Auth Screen'de rol seçimi (Restoran/İhtiyaç Sahibi)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False, default='')

    # Rol: 'owner' (restoran sahibi) veya 'user' (ihtiyaç sahibi)
    role = db.Column(db.String(20), nullable=False, default='user')

    # Kullanıcı tipi: student, disabled, pregnant, standard
    # Öncelik Skoru hesaplamasında kullanılır (Teknik Rapor - Bölüm 4.2)
    user_type = db.Column(db.String(20), nullable=False, default='standard')

    # Kullanıcı puanı
    points = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # İlişkiler
    restaurants = db.relationship('Restaurant', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def set_password(self, password):
        """Şifreyi hash'leyerek kaydet."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Şifre doğrulama."""
        return check_password_hash(self.password_hash, password)

    @property
    def user_type_display(self):
        """Kullanıcı tipini Türkçe olarak döndür."""
        type_map = {
            'student': 'Öğrenci',
            'disabled': 'Engelli',
            'pregnant': 'Hamile',
            'standard': 'Standart'
        }
        return type_map.get(self.user_type, 'Standart')

    @property
    def user_type_weight(self):
        """
        Kullanıcı tipi ağırlığı (W_type).
        Teknik Rapor - Bölüm 4.2:
        Hamile/Engelli: 100, Öğrenci: 80, Standart: 50
        """
        weight_map = {
            'pregnant': 100,
            'disabled': 100,
            'student': 80,
            'standard': 50
        }
        return weight_map.get(self.user_type, 50)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Restaurant(db.Model):
    """
    Restoran modeli.
    Teknik Rapor - Bölüm 6: Restaurants Table
    Wireframe: Harita üzerinde marker olarak gösterilir
    """
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=4.0)
    address = db.Column(db.String(300), default='')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # İlişkiler
    products = db.relationship('Product', backref='restaurant', lazy=True)

    @property
    def suspended_count(self):
        """Askıda olan ürün sayısı."""
        return Product.query.filter_by(
            restaurant_id=self.id, status='suspended'
        ).count()

    @property
    def total_products(self):
        """Toplam ürün sayısı."""
        return Product.query.filter_by(restaurant_id=self.id).count()

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Product(db.Model):
    """
    Ürün modeli.
    Teknik Rapor - Bölüm 6: Products Table
    Wireframe: Envanter tablosu ve askıdaki menü listesi

    Durum (status):
        - on_sale: Satışta (normal ürün)
        - suspended: Askıda/Bağış (ihtiyaç sahiplerine açık)
        - matched: Eşleştirildi (bir kullanıcıya atandı)
        - completed: Teslim edildi
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    original_price = db.Column(db.Float, default=0.0)
    price = db.Column(db.Float, default=0.0)
    skt_date = db.Column(db.DateTime, nullable=False)

    # Durum: on_sale, suspended, matched, completed
    status = db.Column(db.String(20), nullable=False, default='on_sale')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # İlişkiler
    transactions = db.relationship('Transaction', backref='product', lazy=True)

    @property
    def status_display(self):
        """Durumu Türkçe olarak döndür."""
        status_map = {
            'on_sale': 'Satışta',
            'suspended': 'Askıda / Bağış',
            'matched': 'Eşleştirildi',
            'completed': 'Teslim Edildi'
        }
        return status_map.get(self.status, self.status)

    @property
    def status_css_class(self):
        """Durum için CSS sınıfı."""
        class_map = {
            'on_sale': 'status-on-sale',
            'suspended': 'status-suspended',
            'matched': 'status-matched',
            'completed': 'status-completed'
        }
        return class_map.get(self.status, '')

    def __repr__(self):
        return f'<Product {self.name} ({self.status})>'


class Transaction(db.Model):
    """
    İşlem/Talep modeli.
    Teknik Rapor - Bölüm 6: Transactions Table
    Wireframe: Eşleştirme ve teslimat takibi

    Durum (status):
        - pending: Talep beklemede (15 dk toplama süresi)
        - matched: Eşleştirildi
        - completed: Teslim edildi
        - cancelled: İptal edildi
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # Öncelik skoru (Teknik Rapor - Bölüm 4.2)
    priority_score = db.Column(db.Float, default=0.0)

    # Durum: pending, matched, completed, cancelled
    status = db.Column(db.String(20), nullable=False, default='pending')

    # Teslimat Doğrulama PIN Kodu (Örn: '4825')
    pin_code = db.Column(db.String(10), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    matched_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    # İlişki
    restaurant = db.relationship('Restaurant', backref='transactions')

    def __repr__(self):
        return f'<Transaction #{self.id} - {self.status}>'
