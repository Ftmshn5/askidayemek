"""
Askıda Yemek (Food Bridge) - Demo Verileri (Seed Data)

Projeyi ilk çalıştırdığında test edilebilmesi için
örnek kullanıcılar, restoranlar ve ürünler oluşturur.
Koordinatlar Elazığ / Fırat Üniversitesi çevresi olarak ayarlanmıştır.
"""

from datetime import datetime, timezone, timedelta
from models import db, User, Restaurant, Product, Transaction


def seed_database():
    """Veritabanına demo veriler ekle."""

    # Mevcut veri varsa ekleme
    if User.query.first():
        return False

    # ============================================
    # KULLANICILAR
    # ============================================

    # Restoran sahipleri (Owner)
    owner1 = User(
        username='lezzet_sofrasi',
        full_name='Mehmet Kaya',
        role='owner',
        user_type='standard',
        points=0
    )
    owner1.set_password('123456')

    owner2 = User(
        username='kampus_lokantasi',
        full_name='Ayşe Demir',
        role='owner',
        user_type='standard',
        points=0
    )
    owner2.set_password('123456')

    owner3 = User(
        username='dayanisma_mutfagi',
        full_name='Ali Yıldız',
        role='owner',
        user_type='standard',
        points=0
    )
    owner3.set_password('123456')

    # İhtiyaç sahipleri (User)
    user1 = User(
        username='ahmet_yilmaz',
        full_name='Ahmet Yılmaz',
        role='user',
        user_type='student',
        points=840
    )
    user1.set_password('123456')

    user2 = User(
        username='fatma_ozkan',
        full_name='Fatma Özkan',
        role='user',
        user_type='disabled',
        points=560
    )
    user2.set_password('123456')

    user3 = User(
        username='elif_celik',
        full_name='Elif Çelik',
        role='user',
        user_type='pregnant',
        points=320
    )
    user3.set_password('123456')

    user4 = User(
        username='can_aksoy',
        full_name='Can Aksoy',
        role='user',
        user_type='standard',
        points=120
    )
    user4.set_password('123456')

    db.session.add_all([owner1, owner2, owner3, user1, user2, user3, user4])
    db.session.flush()

    # ============================================
    # RESTORANLAR (Elazığ / Fırat Üniversitesi çevresi)
    # ============================================

    restaurant1 = Restaurant(
        owner_id=owner1.id,
        name='Lezzet Sofrası',
        latitude=38.6748,
        longitude=39.1860,
        rating=4.5,
        address='Üniversite Mah. Fırat Üniversitesi Kampüsü, Elazığ'
    )

    restaurant2 = Restaurant(
        owner_id=owner2.id,
        name='Kampüs Lokantası',
        latitude=38.6780,
        longitude=39.1920,
        rating=4.2,
        address='Kampüs Yolu Cad. No:12, Elazığ'
    )

    restaurant3 = Restaurant(
        owner_id=owner3.id,
        name='Dayanışma Mutfağı',
        latitude=38.6710,
        longitude=39.1980,
        rating=4.8,
        address='Merkez Mah. Dayanışma Sok. No:5, Elazığ'
    )

    db.session.add_all([restaurant1, restaurant2, restaurant3])
    db.session.flush()

    # ============================================
    # ÜRÜNLER
    # ============================================
    now = datetime.now(timezone.utc)

    products = [
        # Lezzet Sofrası ürünleri
        Product(
            restaurant_id=restaurant1.id,
            name='Mercimek Çorbası',
            quantity=5,
            original_price=45.0,
            price=35.0,
            skt_date=now + timedelta(hours=4),  # 4 saat kaldı → otomatik askıya alınacak
            status='suspended'
        ),
        Product(
            restaurant_id=restaurant1.id,
            name='Sebzeli Pilav',
            quantity=3,
            original_price=65.0,
            price=50.0,
            skt_date=now + timedelta(hours=2),
            status='on_sale'
        ),
        Product(
            restaurant_id=restaurant1.id,
            name='Karışık Sandviç',
            quantity=10,
            original_price=85.0,
            price=68.0,
            skt_date=now + timedelta(days=2),
            status='on_sale'
        ),
        Product(
            restaurant_id=restaurant1.id,
            name='Günün Tatlısı',
            quantity=4,
            original_price=55.0,
            price=40.0,
            skt_date=now + timedelta(days=3),
            status='suspended'
        ),

        # Kampüs Lokantası ürünleri
        Product(
            restaurant_id=restaurant2.id,
            name='Tavuk Döner',
            quantity=8,
            original_price=95.0,
            price=75.0,
            skt_date=now + timedelta(hours=5),
            status='suspended'
        ),
        Product(
            restaurant_id=restaurant2.id,
            name='Ayran',
            quantity=20,
            original_price=20.0,
            price=15.0,
            skt_date=now + timedelta(days=5),
            status='on_sale'
        ),
        Product(
            restaurant_id=restaurant2.id,
            name='Lahmacun',
            quantity=6,
            original_price=70.0,
            price=55.0,
            skt_date=now + timedelta(hours=3),
            status='suspended'
        ),

        # Dayanışma Mutfağı ürünleri
        Product(
            restaurant_id=restaurant3.id,
            name='Kuru Fasulye',
            quantity=7,
            original_price=75.0,
            price=60.0,
            skt_date=now + timedelta(hours=8),
            status='on_sale'
        ),
        Product(
            restaurant_id=restaurant3.id,
            name='Çorba + Ekmek',
            quantity=15,
            original_price=40.0,
            price=30.0,
            skt_date=now + timedelta(hours=1),
            status='suspended'
        ),
        Product(
            restaurant_id=restaurant3.id,
            name='Makarna',
            quantity=4,
            original_price=55.0,
            price=42.0,
            skt_date=now + timedelta(days=1),
            status='on_sale'
        ),
    ]

    db.session.add_all(products)
    db.session.flush()

    # ============================================
    # ÖRNEK İŞLEMLER (Geçmiş eşleştirmeler)
    # ============================================
    sample_transactions = []
    for i in range(15):
        day_offset = i % 7
        t = Transaction(
            user_id=user1.id if i % 3 == 0 else (user2.id if i % 3 == 1 else user3.id),
            product_id=products[i % len(products)].id,
            restaurant_id=products[i % len(products)].restaurant_id,
            priority_score=75.0 + (i * 2),
            status='completed',
            created_at=now - timedelta(days=day_offset, hours=i),
            matched_at=now - timedelta(days=day_offset, hours=i - 1),
            completed_at=now - timedelta(days=day_offset, hours=i - 2)
        )
        sample_transactions.append(t)

    db.session.add_all(sample_transactions)
    db.session.commit()

    print("✅ Demo veriler başarıyla eklendi!")
    print(f"   → {User.query.count()} kullanıcı")
    print(f"   → {Restaurant.query.count()} restoran")
    print(f"   → {Product.query.count()} ürün")
    print(f"   → {Transaction.query.count()} işlem")

    return True
