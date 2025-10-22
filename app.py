import os
import subprocess # build_db.py'yi çalıştırmak için eklendi
import gradio as gr
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic

# ================================================================
# BÖLÜM 1: YAPILANDIRMA VE MODELLERİ YÜKLEME
# ================================================================
print("📚 BÖLÜM 1: Yapılandırma ve Modelleri Yükleme")
print("="*70)

# .env dosyasındaki API anahtarını yükle (Hugging Face Secret'ları için de çalışır)
load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    # HF Secret'larında ANTHROPIC_API_KEY olup olmadığını kontrol et
    print("UYARI: .env dosyasında ANTHROPIC_API_KEY bulunamadı.")
    print("Hugging Face Secret'ları kontrol ediliyor...")
    # api_key zaten None ise, HF secret'ı da yoktur
    if os.environ.get("HF_TOKEN"): # HF ortamında olduğumuzu varsayalım
        raise EnvironmentError("❌ ANTHROPIC_API_KEY bulunamadı. Lütfen Hugging Face Space 'Settings' > 'Secrets' bölümünden ekleyin.")
    else:
        raise EnvironmentError("❌ ANTHROPIC_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")

print(f"✅ Claude API Anahtarı yüklendi (Başlangıcı: {api_key[:15]}...).")

# Ayarlar
DB_DIRECTORY = "chroma_db_colab"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# === YENİ BÖLÜM: OTOMATİK VERİTABANI OLUŞTURMA ===
if not os.path.exists(DB_DIRECTORY):
    print(f"🌀 '{DB_DIRECTORY}' veritabanı klasörü bulunamadı.")
    print("Veritabanı 'build_db.py' çalıştırılarak oluşturuluyor...")
    print("Bu işlem (PDF'lerinizin boyutuna bağlı olarak) birkaç dakika sürebilir.")
    
    # build_db.py script'ini çalıştır
    try:
        # Hugging Face'in Python 3.10 kullandığını varsayarak 'python3.10'
        # Yerelde 'python' da çalışır
        try:
            subprocess.run(["python", "build_db.py"], check=True, capture_output=True, text=True)
        except FileNotFoundError:
             # HF Spaces gibi ortamlarda 'python3' veya 'python3.10' gerekebilir
             print("'python' komutu bulunamadı, 'python3' ile deneniyor...")
             subprocess.run(["python3", "build_db.py"], check=True, capture_output=True, text=True)

        print("✅ Veritabanı başarıyla oluşturuldu.")
    except subprocess.CalledProcessError as e:
        print(f"❌ HATA: Veritabanı oluşturulamadı.")
        print("Lütfen 'build_db.py' script'inin çalıştığından emin olun.")
        print("Hata Detayı:", e.stderr)
        exit()
else:
    print(f"✅ Hazır veritabanı '{DB_DIRECTORY}' bulundu.")
# === OTOMATİK OLUŞTURMA BÖLÜMÜ SONU ===


print(f"⏳ Embedding modeli yükleniyor ({EMBEDDING_MODEL})...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
print("✅ Embedding modeli yüklendi.")

print(f"⏳ Hazır vektör veritabanı ('{DB_DIRECTORY}') yükleniyor...")
vector_store = Chroma(
    persist_directory=DB_DIRECTORY,
    embedding_function=embedding_model
)
print(f"✅ Vektör veritabanı yüklendi ({vector_store._collection.count()} vektör).")

# ================================================================
# BÖLÜM 2: RAG ZİNCİRİ (CLAUDE İLE)
# ================================================================
print("\n📚 BÖLÜM 2: RAG Zinciri Oluşturuluyor (Claude API)")
print("="*70)

def format_docs(docs):
    """Retriever'dan gelen dökümanları string'e çevirir"""
    if not docs:
        return "İlgili bilgi bulunamadı."
    return "\n\n".join([f"Kaynak {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

print(f"⏳ Claude modeli yapılandırılıyor ({CLAUDE_MODEL})...")
llm = ChatAnthropic(
    model=CLAUDE_MODEL,
    temperature=0.7,
    max_tokens=4096,
    anthropic_api_key=api_key
)
print("✅ Claude modeli hazır.")

retriever = vector_store.as_retriever(search_kwargs={'k': 5})
print("✅ Retriever hazır (k=5).")

# Prompt template (Sizinkiyle aynı)
prompt_template = """
# GÖREVİN VE KİŞİLİĞİN
Sen, "Girişim Analisti" adında uzman bir startup ve girişim danışmanısın. Tek görevin, kullanıcının sunduğu girişim fikrini, sana sağlanan DAHİLİ BİLGİLER (BAĞLAM) ışığında, aşağıda belirtilen "Startup Fikri Değerlendirme Raporu" formatına göre analiz etmektir. Cevapların net, yol gösterici, yapıcı ve profesyonel olmalıdır. Asla bağlam dışına çıkma.

# DEĞERLENDİRME SÜRECİN
Kullanıcının fikrini analiz ederken aşağıdaki 6 adımı sırasıyla uygula ve her adımı ayrı bir başlık altında raporla:
1.  **Asansör Sunumu ve Temel Değer Önermesi:** Fikrin anlaşılırlığını, değer önermesini ve özgünlüğünü değerlendir.
2.  **Problem Analizi:** Tanımlanan problemin aciliyetini ve mevcut çözüm yollarını yorumla.
3.  **Çözüm ve Ürün Konsepti:** Çözümün probleme uygunluğunu, "10x avantajını" ve savunulabilirliğini analiz et.
4.  **Pazar Potansiyeli:** Pazarın büyüklüğü, hedef kitle ve zamanlaması hakkında bağlamdaki bilgileri kullanarak yorum yap.
5.  **Kurucu ve Ekip Potansiyeli (Founder-Market Fit):** Kurucunun problemle olan ilişkisinin önemini vurgula.
6.  **İlk Adım ve Doğrulama Stratejisi:** MVP ve ilk müşterilere ulaşma konusunda stratejiler sun.

# SONUÇ DEĞERLENDİRMESİ
Tüm analizini tamamladıktan sonra, raporun sonuna **"Genel Değerlendirme"** başlığı ekle ve fikri aşağıdaki üç kategoriden birine yerleştirerek nihai görüşünü ve en önemli tavsiyeni belirt:
* **Güçlü Potensiyel**
* **Sarı Işıklar (Düşünülmesi Gerekenler)**
* **Kırmızı Bayraklar (Ciddi Engeller)**

---
# KULLANILACAK DAHİLİ BİLGİLER (BAĞLAM)
{context}

# KULLANICININ GİRİŞİM FİKRİ (SORU)
{question}

# RAPORUN
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

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
print("✅ RAG zinciri başarıyla oluşturuldu.\n")

# ================================================================
# BÖLÜM 3: GRADIO ARAYÜZÜ
# ================================================================
print("📚 BÖLÜM 3: Gradio Arayüzü Başlatılıyor")
print("="*70)

def chatbot_response(message, chat_history):
    print(f"\n{'='*30} YENİ SORU {'='*30}")
    print(f"[Gelen Soru] {message}")
    
    try:
        print("[DEBUG] RAG chain çalıştırılıyor (Claude API)...")
        response = rag_chain.invoke(message)
        print(f"[Verilen Cevap] {response[:200]}...")
        return response

    except Exception as e:
        error_msg = f"Bir hata oluştu: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

demo = gr.ChatInterface(
    fn=chatbot_response,
    title="🚀 Girişim Fikri Değerlendirme Chatbot'u (Claude Powered)",
    description="Startup fikrinizi girin, Claude AI ile RAG destekli analiz edin. (Kaynak: YC, Paul Graham, a16z...)",
    examples=[
        "Sokak hayvanları için akıllı mama kapları geliştiren bir sosyal girişim fikrim var.",
        "Öğrencilerin ikinci el ders kitaplarını kolayca satıp alabileceği bir mobil uygulama.",
        "Yapay zeka destekli kişisel finans asistanı"
    ],
    theme="soft"
)

print("🚀 Chatbot arayüzü başlatılıyor...")
print("💡 Tarayıcınızda açmak için yerel adresi (http://127.0.0.1:...) ziyaret edin.")
# Hugging Face'te "share=True" gerekmez ve sorun çıkarabilir.
demo.launch(debug=True)