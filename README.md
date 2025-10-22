🚀 Girişim Fikri Değerlendirme Chatbot
RAG (Retrieval-Augmented Generation) tabanlı, Claude AI ile güçlendirilmiş, startup ve girişim fikirlerinizi profesyonel bir şekilde analiz eden chatbot.

📋 İçindekiler

Özellikler
Nasıl Çalışır?
Kurulum
Kullanım
Hugging Face'e Deploy
Proje Yapısı
Teknolojiler
Lisans

✨ Özellikler

🤖 Claude 3.5 Sonnet ile güçlendirilmiş yapay zeka
📚 RAG (Retrieval-Augmented Generation) teknolojisi ile belge tabanlı analiz
🎯 Startup odaklı değerlendirme - Y Combinator, Paul Graham, a16z kaynaklı bilgiler
🔍 6 kapsamlı analiz kategorisi:

Asansör Sunumu ve Değer Önermesi
Problem Analizi
Çözüm ve Ürün Konsepti
Pazar Potansiyeli
Kurucu ve Ekip Potansiyeli
İlk Adım ve Doğrulama Stratejisi


🎨 Kullanıcı dostu Gradio arayüzü
⚡ Otomatik vektör veritabanı oluşturma
📄 PDF belgelerden öğrenme

🔧 Nasıl Çalışır?

Vektör Veritabanı Oluşturma: data/ klasöründeki PDF'ler chunklara ayrılır ve embeddings oluşturulur
Soru Gönderme: Kullanıcı girişim fikrini chatbot'a yazar
Retrieval: En alakalı bilgiler vektör veritabanından çekilir
Generation: Claude AI, bu bilgileri kullanarak profesyonel analiz oluşturur
Sonuç: Detaylı startup değerlendirme raporu kullanıcıya sunulur

🛠️ Kurulum
Gereksinimler

Python 3.10 veya üstü
Anthropic API Key (Claude)

Adımlar

Repoyu klonlayın

bashgit clone https://github.com/KULLANICI_ADINIZ/girisim-chatbot.git
cd girisim-chatbot

Sanal ortam oluşturun (önerilir)

bashpython -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

Bağımlılıkları yükleyin

bashpip install -r requirements.txt

API anahtarını ayarlayın

.env dosyası oluşturun:
envANTHROPIC_API_KEY=your_api_key_here

PDF belgelerinizi ekleyin

data/ klasörü oluşturun ve startup ile ilgili PDF belgelerinizi bu klasöre atın:
bashmkdir data
# PDF dosyalarınızı data/ klasörüne kopyalayın

Vektör veritabanını oluşturun

İlk kullanımda PDF'lerden vektör veritabanı oluşturmanız gerekiyor:
bashpython build_db.py
Bu işlem PDF'lerinizin boyutuna göre birkaç dakika sürebilir. İşlem tamamlandığında chroma_db_colab/ klasörü oluşacaktır.

Uygulamayı başlatın

bashpython app.py
Tarayıcınızda http://127.0.0.1:7860 adresine gidin.

💡 Not: app.py otomatik olarak veritabanı yoksa oluşturacaktır, ancak ilk kullanımda manuel olarak build_db.py çalıştırmanız önerilir.

🎮 Kullanım
Örnek Sorular
"Sokak hayvanları için akıllı mama kapları geliştiren bir sosyal girişim fikrim var."

"Öğrencilerin ikinci el ders kitaplarını kolayca satıp alabileceği bir mobil uygulama."

"Yapay zeka destekli kişisel finans asistanı geliştirmek istiyorum."
Veritabanını Yeniden Oluşturma
PDF'lerinizi güncellediyseniz veya yeni belgeler eklediyseniz, veritabanını yeniden oluşturun:
bashpython build_db.py
Bu komut eski veritabanını silip yeniden oluşturacaktır.
