import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# BU DOSYANIN TEK GÖREVİ: VERİTABANINI OLUŞTURMAK

print("Veritabanı Oluşturucu Başladı...")

db_directory = "./chroma_db"
if os.path.exists(db_directory):
    print(f"✅ '{db_directory}' zaten mevcut. Silinip yeniden oluşturulacak.")
    import shutil
    shutil.rmtree(db_directory)

try:
    # 1. Embedding modelini yükle (Sadece bu dosya kullanacak)
    print("⏳ Embedding modeli yükleniyor...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("✅ Embedding modeli başarıyla yüklendi.")

    # 2. PDF'leri yükle
    print("⏳ PDF dosyaları yükleniyor...")
    loader = DirectoryLoader('./data/', glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    if not documents:
        print("❌ HATA: 'data' klasöründe hiç .pdf dosyası bulunamadı.")
        exit()
    print(f"✅ Başarıyla {len(documents)} adet PDF dokümanı yüklendi.")

    # 3. Parçalara ayır
    print("⏳ Metinler parçalara (chunk) ayrılıyor...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_documents(documents)
    print(f"✅ {len(documents)} doküman, toplam {len(chunks)} adet parçaya (chunk) ayrıldı.")

    # 4. Veritabanını oluştur
    print("\n⏳ Vektör veritabanı oluşturuluyor ve chunk'lar kaydediliyor...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_directory
    )
    print(f"✅ Vektör veritabanı başarıyla oluşturuldu ve '{db_directory}' klasörüne kaydedildi.")
    print(f"✨ Toplam {vector_store._collection.count()} adet vektör veritabanına eklendi.")
    print("\n🎉 VERİTABANI OLUŞTURMA İŞLEMİ TAMAMLANDI. 🎉")

except Exception as e:
    print(f"❌ Veritabanı oluşturulurken bir hata oluştu: {e}")