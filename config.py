"""
Askıda Yemek (Food Bridge) - Konfigürasyon Dosyası
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Ana konfigürasyon sınıfı."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'askida-yemek-gizli-anahtar-2026')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'askida_yemek.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Eşleştirme süresi (saniye) - Teknik raporda 15 dakika (900 saniye)
    # Demo için 60 saniye olarak ayarlandı
    MATCHING_WINDOW_SECONDS = 60

    # SKT otomatik askıya alma eşiği (saat)
    SKT_THRESHOLD_HOURS = 6
