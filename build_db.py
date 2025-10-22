import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ================================================================
# BÖLÜM 1: AYARLAR
# ================================================================
DATA_DIR = "data"
DB_DIRECTORY = "chroma_db_colab"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

if not os.path.exists(DATA_DIR):
    print(f"HATA: '{DATA_DIR}' klasörü bulunamadı.")
    print("Lütfen PDF dosyalarınızı içeren bir 'data' klasörü oluşturun.")
    exit()

# ================================================================
# BÖLÜM 2: VERİTABANI OLUŞTURMA
# ================================================================
print("📚 BÖLÜM 2: Veritabanı Oluşturma Başlatıldı")
print("="*70)

print(f"⏳ Embedding modeli yükleniyor ({EMBEDDING_MODEL})...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
print("✅ Embedding modeli yüklendi.")

print(f"⏳ PDF dosyaları '{DATA_DIR}' klasöründen okunuyor...")
loader = DirectoryLoader(
    f'./{DATA_DIR}/', 
    glob="**/*.pdf", 
    loader_cls=PyPDFLoader, 
    show_progress=True
)
documents = loader.load()
if not documents:
    print(f"HATA: '{DATA_DIR}' klasöründe hiç PDF dosyası bulunamadı.")
    exit()
print(f"✅ Toplam {len(documents)} sayfa okundu.")

print("⏳ Metinler parçalanıyor...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"✅ {len(chunks)} adet chunk oluşturuldu.")

# Eski veritabanı varsa temizle
if os.path.exists(DB_DIRECTORY):
    print(f"🌀 Eski veritabanı '{DB_DIRECTORY}' siliniyor...")
    shutil.rmtree(DB_DIRECTORY)

print(f"\n⏳ Vektör veritabanı oluşturuluyor ({len(chunks)} chunk)...")
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=DB_DIRECTORY
)
print(f"✅ Vektör veritabanı oluşturuldu ({vector_store._collection.count()} vektör).")
print(f"🎉 Veritabanı başarıyla '{DB_DIRECTORY}' klasörüne kaydedildi!\n")