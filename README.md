# 🚀 Girişim Fikri Değerlendirme Chatbot - RAG Tabanlı Akıllı Asistan
Projenin çalışan halinin videosu: https://drive.google.com/file/d/1vxwcMb9XKCf_YP1opGKWKYQIGtfBxTt8/view?usp=sharing

> **Not:** Bu proje Akbank & Global AI Hub **Generative AI Bootcamp** kapsamında geliştirilmiştir. RAG (Retrieval-Augmented Generation) mimarisi kullanılarak, startup ve girişim fikirlerinizi profesyonel bir şekilde analiz eden akıllı bir chatbot sistemidir.

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [RAG Mimarisi](#-rag-mimarisi-nedir)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [RAG Sistemi Detayları](#-rag-sistemi-detayları)
- [Hugging Face Deployment](#-hugging-facee-deployment)
- [Proje Yapısı](#-proje-yapısı)
- [Performans Optimizasyonu](#-performans-optimizasyonu)
- [Troubleshooting](#-troubleshooting)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

---

## 🎯 Proje Hakkında

Bu proje, **RAG (Retrieval-Augmented Generation)** teknolojisini kullanarak startup ve girişim fikirlerinizi değerlendiren akıllı bir chatbot sistemidir. Sistem, PDF belgelerden öğrenerek (Y Combinator, Paul Graham, a16z gibi kaynaklardan), girişim fikirlerinizi 6 kapsamlı kategori altında analiz eder ve detaylı geri bildirim sunar.

### 🎓 Bootcamp Proje Gereksinimleri

Bu proje aşağıdaki gereksinimleri karşılamaktadır:

✅ **RAG Mimarisi:** Retrieval-Augmented Generation sisteminin tam implementasyonu  
✅ **Veri Kaynağı:** PDF belgelerden oluşan knowledge base  
✅ **Vektör Veritabanı:** ChromaDB ile semantic search  
✅ **Embedding Model:** HuggingFace sentence-transformers  
✅ **LLM Entegrasyonu:** Claude 3.5 Sonnet API  
✅ **Web Arayüzü:** Gradio ile kullanıcı dostu chatbot interface  
✅ **Deployment:** Hugging Face Spaces'e deploy edilebilir  
✅ **Dokümantasyon:** Kapsamlı README ve kod açıklamaları  

---

## ✨ Özellikler

### 🤖 Yapay Zeka Özellikleri
- **Claude 3.5 Sonnet** ile güçlendirilmiş doğal dil işleme
- **RAG Teknolojisi** ile belge tabanlı, doğru ve güvenilir yanıtlar
- **Semantic Search** ile en alakalı bilgilerin bulunması
- **Context-Aware Responses** - Bağlama duyarlı, tutarlı cevaplar
- **Hallucination Prevention** - Sadece kaynaklara dayalı bilgi üretimi

### 📊 Değerlendirme Kategorileri
1. **Asansör Sunumu ve Değer Önermesi**
2. **Problem Analizi**
3. **Çözüm ve Ürün Konsepti**
4. **Pazar Potansiyeli**
5. **Kurucu ve Ekip Potansiyeli (Founder-Market Fit)**
6. **İlk Adım ve Doğrulama Stratejisi**

### 🎨 Kullanıcı Deneyimi
- Sezgisel Gradio arayüzü
- Gerçek zamanlı yanıt üretimi
- Kaynak takibi ve şeffaflık
- Örnek sorularla kolay başlangıç

---

## 🔍 RAG Mimarisi Nedir?

RAG (Retrieval-Augmented Generation), 2020 yılında Patrick Lewis tarafından tanıtılan ve LLM'lerin yanıt kalitesini artıran yenilikçi bir tekniktir.

### RAG'ın Çalıştığı 3 Temel Adım:

```
1. RETRIEVE (Bilgiyi Getir)
   ↓
   Kullanıcının sorusuna en alakalı dokümanları vektör veritabanından bul
   
2. AUGMENT (Zenginleştir)
   ↓
   Bulunan bilgileri LLM'e context olarak ekle
   
3. GENERATE (Üret)
   ↓
   LLM, hem kendi bilgisi hem de verilen context'i kullanarak cevap üret
```

### RAG'ın Avantajları

| Özellik | Açıklama |
|---------|----------|
| 🎯 **Doğruluk** | Kaynaklara dayalı, güvenilir bilgi |
| 🔄 **Güncellik** | Dinamik veri ile çalışma imkanı |
| 💰 **Maliyet** | Model fine-tuning'e göre ekonomik |
| 📚 **Domain Specific** | Alana özel bilgi sağlama |
| 🚫 **No Hallucination** | Uydurma bilgi riskini azaltma |

---

## 🛠 Teknoloji Yığını

### Core Technologies
- **Python 3.10+** - Ana programlama dili
- **LangChain** - RAG orchestration ve chain management
- **Claude 3.5 Sonnet** - Ana LLM (API)
- **ChromaDB** - Vektör veritabanı
- **HuggingFace Transformers** - Embedding modeli
- **Gradio** - Web arayüzü
- **PyPDF** - PDF işleme

### LangChain Modülleri
```python
langchain-core          # Core functionality
langchain-community     # Community integrations
langchain-anthropic     # Claude entegrasyonu
langchain-huggingface   # HF model entegrasyonu
langchain-chroma        # ChromaDB entegrasyonu
langchain-text-splitters # Text chunking
```

---

## 📦 Kurulum

### Ön Gereksinimler

- Python 3.10 veya üstü
- pip (Python paket yöneticisi)
- Git
- Anthropic API Key ([buradan alın](https://console.anthropic.com/))

### Adım 1: Repoyu Klonlayın

```bash
git clone https://github.com/KULLANICI_ADINIZ/girisim-chatbot.git
cd girisim-chatbot
```

### Adım 2: Sanal Ortam Oluşturun (Önerilir)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

**İçerik:**
```txt
langchain
langchain-core
langchain-community
langchain-anthropic
langchain-huggingface
langchain-chroma
langchain-text-splitters
pypdf
python-dotenv
sentence-transformers
gradio
anthropic
```

### Adım 4: API Anahtarını Ayarlayın

`.env` dosyası oluşturun:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx_your_api_key_here
```

⚠️ **Önemli:** `.env` dosyanızı asla GitHub'a yüklemeyin!

### Adım 5: PDF Belgelerinizi Ekleyin

```bash
mkdir data
# PDF dosyalarınızı data/ klasörüne kopyalayın
```

**Nereden Veri Bulabilirim?**
- Kendi kullandığım veri kaynakları: https://drive.google.com/drive/folders/1i6HZCQkGk3kq1JjK6zv9GGzGezowzXwE?usp=sharing
- 📚 [Hugging Face Datasets](https://huggingface.co/datasets)
- 📄 Kendi PDF dokümanlarınız
- 🌐 Web scraping (legal olduğundan emin olun)
- 📝 Ders notları, araştırma makaleleri

### Adım 6: Vektör Veritabanını Oluşturun

```bash
python build_db.py
```

**Bu işlem:**
- PDF'leri okur
- Metinleri chunk'lara böler (chunking)
- Embedding'leri oluşturur
- ChromaDB'ye kaydeder

⏱️ **Süre:** PDF boyutuna göre 2-10 dakika

**Çıktı:**
```
📚 BÖLÜM 1: Yapılandırma ve Modelleri Yükleme
✅ Embedding modeli yüklendi
⏳ PDF dosyaları okunuyor...
✅ Toplam 150 sayfa okundu
⏳ Metinler parçalanıyor...
✅ 450 adet chunk oluşturuldu
✅ Vektör veritabanı oluşturuldu (450 vektör)
```

### Adım 7: Uygulamayı Başlatın

```bash
python app.py
```

Tarayıcınızda otomatik olarak açılacak veya şu adrese gidin:  
👉 **http://127.0.0.1:7860**

---

## 🎮 Kullanım

### Web Arayüzünden

1. Tarayıcıda chatbot arayüzünü açın
2. Girişim fikrinizi yazın
3. "Submit" butonuna tıklayın
4. Detaylı analiz raporunu alın

### Örnek Sorular

```
💡 "Sokak hayvanları için akıllı mama kapları geliştiren bir sosyal girişim fikrim var."

💡 "Öğrencilerin ikinci el ders kitaplarını kolayca satıp alabileceği bir mobil uygulama."

💡 "Yapay zeka destekli kişisel finans asistanı geliştirmek istiyorum."

💡 "Küçük işletmeler için inventory yönetim sistemi."
```

### Veritabanını Güncelleme

PDF'lerinizi güncellediyseniz:

```bash
python build_db.py
```

Bu komut:
- Eski `chroma_db_colab/` klasörünü siler
- Yeni PDF'leri işler
- Veritabanını yeniden oluşturur

---

## 🔬 RAG Sistemi Detayları

### 1️⃣ Knowledge Base (Bilgi Tabanı)

```
data/
├── yc_startup_guide.pdf
├── paul_graham_essays.pdf
├── a16z_playbook.pdf
└── lean_startup.pdf
```

### 2️⃣ Text Chunking (Metni Bölme)

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Her chunk 1000 karakter
    chunk_overlap=200     # Chunk'lar arası 200 karakter örtüşme
)
```

**Neden Chunking?**
- LLM'ler token limiti ile kısıtlı
- Küçük parçalarda arama daha etkili
- Semantic search performansı artar


### 3️⃣ Embedding Model

```python
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

**Popüler Embedding Modelleri:**
- `all-MiniLM-L6-v2` - Hızlı, 384 boyut
- `all-mpnet-base-v2` - Daha yüksek kalite, 768 boyut
- `multilingual-e5-base` - Çok dilli destek

**Embedding Seçimi:**
- Veri boyutu küçükse → MiniLM
- Yüksek kalite gerekiyorsa → MPNet
- Türkçe veri varsa → Multilingual model

### 4️⃣ Vector Store (ChromaDB)

```python
from langchain_chroma import Chroma

vector_store = Chroma(
    persist_directory="chroma_db_colab",
    embedding_function=embedding_model
)
```

**Similarity Search:**
```python
# Kullanıcı sorusu
query = "Startup için pazar analizi nasıl yapılır?"

# En benzer 5 chunk'ı bul
docs = vector_store.similarity_search(query, k=5)
```

**Benzerlik Metrikleri:**
- Cosine Similarity (varsayılan)
- Euclidean Distance
- Dot Product

### 5️⃣ Retrieval & Generation

```python
# RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

response = rag_chain.invoke("Girişim fikrim...")
```

**Akış:**
```
User Query → Embedding → Vector Search → Top K Docs
                                              ↓
                                    Format as Context
                                              ↓
                          Context + Query → LLM Prompt
                                              ↓
                                    Claude API Call
                                              ↓
                                  Generated Response
```

---


## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.


--
## 🙏 Teşekkürler

- **Akbank & Global AI Hub** - Bootcamp organizasyonu


