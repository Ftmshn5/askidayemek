"""
Askıda Yemek (Food Bridge) - Algoritmalar

Teknik Rapor - Bölüm 4: Sistem Çalışma Mantığı ve Algoritmalar

İçerik:
    1. Öncelik Skoru (Priority Score) Hesaplama
    2. heapq ile Min-Heap Önceliklendirme (SKT bazlı)
    3. Greedy Matching Algoritması (Batch Matching)
    4. Otomatik SKT Kontrolü (Hibrid İlan Sistemi)
"""

import heapq
from datetime import datetime, timezone, timedelta
from models import db, Product, Transaction, User


def calculate_priority_score(user, request_time, window_start_time):
    """
    Öncelik Skoru (P) hesaplama.
    Teknik Rapor - Bölüm 4.2:

    P = (W_type × 0.6) + (W_time × 0.4)

    W_type: Kullanıcı tipi puanı
        - Hamile/Engelli: 100
        - Öğrenci: 80
        - Standart: 50

    W_time: Talebin yapıldığı anın önceliği (ilk gelen avantajı)
        - Pencere başlangıcına yakın → yüksek puan

    Args:
        user: User nesnesi
        request_time: Talebin yapıldığı zaman (datetime)
        window_start_time: Talep toplama penceresinin başlangıcı (datetime)

    Returns:
        float: Öncelik skoru (0-100 arası)
    """
    # W_type: Kullanıcı tipi ağırlığı
    w_type = user.user_type_weight

    # W_time: Zaman bazlı öncelik (ilk gelen avantajı)
    # Pencere başlangıcından ne kadar erken geldiyse o kadar yüksek
    elapsed = (request_time - window_start_time).total_seconds()
    max_window = 900  # 15 dakika = 900 saniye
    w_time = max(0, 100 - (elapsed / max_window) * 100)

    # Formül: P = (W_type × 0.6) + (W_time × 0.4)
    priority = (w_type * 0.6) + (w_time * 0.4)

    return round(priority, 2)


def get_urgent_products_heap(restaurant_id=None):
    """
    heapq tabanlı Min-Heap ile en acil ürünleri önceliklendirme.
    Teknik Rapor - Bölüm 3: heapq (Min-Heap kullanılarak en acil gıdaların önceliklendirilmesi)

    SKT'ye en yakın ürünler en üstte yer alır.

    Args:
        restaurant_id: Belirli bir restoranın ürünleri için filtre (opsiyonel)

    Returns:
        list: (skt_timestamp, product_id, product) tuple listesi (heap sıralı)
    """
    query = Product.query.filter(Product.status == 'suspended')

    if restaurant_id:
        query = query.filter(Product.restaurant_id == restaurant_id)

    products = query.all()

    # Min-Heap oluştur: (SKT timestamp, product_id, product)
    heap = []
    for product in products:
        skt = product.skt_date.replace(tzinfo=timezone.utc) if product.skt_date.tzinfo is None else product.skt_date
        skt_timestamp = skt.timestamp()
        heapq.heappush(heap, (skt_timestamp, product.id, product))

    return heap


def greedy_matching(product_id):
    """
    Greedy Matching Algoritması.
    Teknik Rapor - Bölüm 4.2:

    "Süre sonunda Greedy Matching algoritması, en yüksek puanlı kullanıcıları
     en yakın tarihli ürünlerle eşleştirir."

    Bu fonksiyon belirli bir ürün için bekleyen talepleri alır,
    öncelik skoruna göre sıralar ve en yüksek skorlu kullanıcıyı eşleştirir.

    Args:
        product_id: Eşleştirme yapılacak ürün ID'si

    Returns:
        Transaction veya None: Eşleştirilen işlem
    """
    # Ürünü al
    product = Product.query.get(product_id)
    if not product or product.status != 'suspended':
        return None

    # Bu ürün için bekleyen talepleri al
    pending_transactions = Transaction.query.filter_by(
        product_id=product_id,
        status='pending'
    ).all()

    if not pending_transactions:
        return None

    # Öncelik skoruna göre sırala (en yüksek önce)
    pending_transactions.sort(key=lambda t: t.priority_score, reverse=True)

    # En yüksek puanlı kullanıcıyı eşleştir
    winner = pending_transactions[0]
    now = datetime.now(timezone.utc)

    winner.status = 'matched'
    winner.matched_at = now

    # Ürünü eşleştirildi olarak işaretle
    product.status = 'matched'

    # Kullanıcıya puan ekle
    user = User.query.get(winner.user_id)
    if user:
        user.points += 10

    # Diğer talepleri iptal et
    for transaction in pending_transactions[1:]:
        transaction.status = 'cancelled'

    db.session.commit()

    return winner


def run_batch_matching():
    """
    Toplu (Batch) Eşleştirme.
    Teknik Rapor - Bölüm 4.2:

    "Talep açıldıktan sonra 15 dakikalık bir Talep Toplama süreci başlar."

    Süresi dolmuş tüm bekleyen talepleri kontrol eder ve eşleştirme yapar.

    Returns:
        list: Eşleştirilen işlemler listesi
    """
    now = datetime.now(timezone.utc)

    # Askıda olan tüm ürünler için bekleyen talepleri kontrol et
    suspended_products = Product.query.filter_by(status='suspended').all()

    matched_transactions = []

    for product in suspended_products:
        pending = Transaction.query.filter_by(
            product_id=product.id,
            status='pending'
        ).all()

        if not pending:
            continue

        # En eski talebin zamanını kontrol et (toplama süresi doldu mu?)
        oldest_request = min(pending, key=lambda t: t.created_at)
        oldest_created = oldest_request.created_at.replace(tzinfo=timezone.utc) if oldest_request.created_at.tzinfo is None else oldest_request.created_at
        elapsed = (now - oldest_created).total_seconds()

        # Eğer en az 60 saniye geçtiyse eşleştirme yap (demo için kısa süre)
        if elapsed >= 60:
            result = greedy_matching(product.id)
            if result:
                matched_transactions.append(result)

    return matched_transactions


def auto_suspend_expiring_products():
    """
    Otomatik SKT Kontrolü.
    Teknik Rapor - Bölüm 4.1 (Hibrid İlan Sistemi):

    "Restoran envanterindeki ürünlerin SKT'sine 6 saatten az kaldığında
     sistem ürünü otomatik olarak 'Askıda' statüsüne geçirir."

    Returns:
        list: Askıya alınan ürünler listesi
    """
    now = datetime.now(timezone.utc)
    threshold = now + timedelta(hours=6)

    # SKT'sine 6 saatten az kalan ve hâlâ satışta olan ürünler
    expiring_products = Product.query.filter(
        Product.status == 'on_sale',
        Product.skt_date <= threshold,
        Product.skt_date > now  # Henüz süresi geçmemiş
    ).all()

    suspended = []
    for product in expiring_products:
        product.status = 'suspended'
        suspended.append(product)

    if suspended:
        db.session.commit()

    return suspended


def get_impact_stats(user_id=None, restaurant_id=None):
    """
    Etki Raporu İstatistikleri.
    Wireframe: Toplumsal Etki ekranı
        - Önlenen gıda atığı (kg)
        - Mutlu kullanıcı sayısı
        - CO2 tasarrufu (kg)

    Args:
        user_id: Belirli kullanıcı için filtre (opsiyonel)
        restaurant_id: Belirli restoran için filtre (opsiyonel)

    Returns:
        dict: İstatistik verileri
    """
    query = Transaction.query.filter(
        Transaction.status.in_(['matched', 'completed'])
    )

    if user_id:
        query = query.filter_by(user_id=user_id)
    if restaurant_id:
        query = query.filter_by(restaurant_id=restaurant_id)

    transactions = query.all()

    total_matched = len(transactions)

    # Her porsiyon ortalama 0.5 kg olarak hesaplanır
    total_food_saved_kg = total_matched * 0.5

    # CO2 tasarrufu: her kg gıda israfı ortalama 2.2 kg CO2 üretir
    co2_saved_kg = round(total_food_saved_kg * 2.2, 1)

    # Benzersiz mutlu kullanıcı sayısı
    unique_users = len(set(t.user_id for t in transactions))

    # Son 7 günlük dağılım
    daily_stats = {}
    for i in range(7):
        day = datetime.now(timezone.utc) - timedelta(days=6 - i)
        day_str = day.strftime('%Y-%m-%d')
        daily_stats[day_str] = 0

    for t in transactions:
        day_str = t.created_at.strftime('%Y-%m-%d')
        if day_str in daily_stats:
            daily_stats[day_str] += 1

    return {
        'total_matched': total_matched,
        'food_saved_kg': round(total_food_saved_kg, 1),
        'co2_saved_kg': co2_saved_kg,
        'happy_users': unique_users,
        'daily_stats': daily_stats
    }
