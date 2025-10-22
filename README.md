# 🚀 Girişim Fikri Değerlendirme Chatbot'u

**Akbank Generative AI Giriş Bootcamp Projesi**

Bu proje, bir "Girişim Analisti" olarak görev yapan ve [Retrieval Augmented Generation (RAG)](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) mimarisini kullanan bir sohbet botudur. Kullanıcıdan alınan startup fikirlerini, Y Combinator, Paul Graham ve Andreessen Horowitz (a16z) gibi önde gelen kaynaklardan derlenen bir bilgi tabanına (PDF dokümanları) dayanarak analiz eder ve yapılandırılmış bir rapor sunar.

## Demo

**(İsteğe bağlı: Hugging Face'e deploy ettikten sonra buraya linki ve bir ekran görüntüsünü ekleyebilirsiniz.)**

`[Buraya Hugging Face Spaces Linkinizi Ekleyin]`

![Girişim Analisti Chatbot Arayüzü](https(link-eklenecek)/gorsel.png)

## Proje Mimarisi (RAG)

[cite_start]Bu proje, bootcamp'in ana gereksinimi olan RAG mimarisini  uygulamak için **LangChain** kütüphanesini kullanır. Sistemin çalışma akışı şu adımlardan oluşur:

1.  **Bilgi Tabanı (Knowledge Base):** `data/` klasörü içinde bulunan PDF dosyaları (startup rehberleri, denemeler vb.) projenin bilgi kaynağı olarak kullanılır.

2.  **Indeksleme (Indexing):**
    * **Yükleme:** `PyPDFLoader` ile `data/` klasöründeki tüm PDF'ler okunur.
    * **Parçalama:** `RecursiveCharacterTextSplitter` kullanılarak metinler, birbirleriyle örtüşen (overlap) daha küçük parçalara (chunk) bölünür (chunk_size: 1000, overlap: 200).
    * **Gömme (Embedding):** `HuggingFaceEmbeddings` (model: `sentence-transformers/all-MiniLM-L6-v2`) ile her bir metin parçası vektörel bir temsile dönüştürülür.
    * **Depolama:** Bu vektörler, kalıcı bir yerel veritabanı olan `ChromaDB`'ye kaydedilir (`chroma_db_colab` klasörü).

3.  **Getirme ve Üretme (Retrieval & Generation):**
    * **Sorgu:** Kullanıcı, girişim fikrini (örn: "Yapay zeka destekli kişisel finans asistanı") arayüze girer.
    * **Getirme (Retrieval):** Kullanıcının sorgusu da vektöre dönüştürülür ve `ChromaDB` içinde anlamsal bir arama yapılır. Fikirle en alakalı `k=5` adet metin parçası (chunk) veritabanından çekilir.
    * **Zenginleştirme (Augmentation):** Bu 5 parça, "Bağlam" (Context) olarak bir prompt şablonuna yerleştirilir. Kullanıcının sorusu da "Soru" (Question) olarak eklenir. Bu prompt, yapay zekaya "Girişim Analisti" rolünü verir ve 6 adımlı bir rapor formatı talep eder.
    * **Üretme (Generation):** Hazırlanan bu zenginleştirilmiş prompt, `ChatAnthropic` (model: `claude-3-5-sonnet-20241022`) modeline gönderilir. LLM, yalnızca kendisine sağlanan bağlamdaki bilgileri kullanarak istenen formatta detaylı analiz raporunu üretir.

## Kullanılan Teknolojiler

* **LLM:** Anthropic Claude 3.5 Sonnet
* **Framework:** LangChain
* **Embedding Modeli:** `sentence-transformers/all-MiniLM-L6-v2`
* **Vektör Veritabanı:** ChromaDB
* **Arayüz (Frontend):** Gradio

## Kurulum ve Çalıştırma

Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/KAD7K/GirisimAnalistiBot.git](https://github.com/KAD7K/GirisimAnalistiBot.git)
    cd GirisimAnalistiBot
    ```

2.  **Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Anahtarınızı Ekleyin:**
    * Proje ana dizininde `.env` adında bir dosya oluşturun.
    * İçine Anthropic API anahtarınızı aşağıdaki formatta yapıştırın:
        ```
        ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
        ```

5.  **(İsteğe Bağlı) Kendi Verilerinizi Ekleyin:**
    * Proje, `data/` klasöründeki mevcut PDF'lerle çalışacaktır.
    * Kendi bilgi tabanınızı kullanmak isterseniz, `data/` klasörüne kendi PDF dosyalarınızı ekleyebilir (veya mevcutları silebilirsiniz).

6.  **Uygulamayı Çalıştırın:**
    ```bash
    python app.py
    ```

    * **Not:** Uygulama (`app.py`) ilk kez çalıştığında, `chroma_db_colab` adlı bir veritabanı klasörü arayacaktır. Bulamazsa, `build_db.py` script'ini otomatik olarak tetikleyerek `data/` klasöründeki PDF'lerden veritabanını oluşturacaktır. Bu ilk kurulum işlemi, PDF'lerinizin boyutuna bağlı olarak birkaç dakika sürebilir.
    * Veritabanı oluşturulduktan sonra Gradio arayüzü başlayacak ve terminalde size yerel bir URL (örn: `http://127.0.0.1:7860`) verecektir. Bu adresi tarayıcınızda açarak chatbot'u kullanabilirsiniz.
