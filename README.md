# Enterprise Project
Bu proje, FastAPI, Celery, Redis, Google Gemini API ve diğer teknolojiler kullanarak veri toplama, 
işleme ve analiz işlemleri gerçekleştiren bir uygulamadır. Uygulama https://ranking.glassdollar.com/ sitesi üzerinden 
belirli verileri toplar ve sonrasında bunları json'a çevirir. Daha sonra bu bilgileri descriptiona göre gruplayarak
GEmini'ye verir ve ondan title ve summary alır. En son da önce tüm enterprise bilgilerini ve dah sonra detaylı
şekilde cluster_id, title, summary ve enterprise bilgilerini dömndürür.
Ayrıca proje Docker kullanarak geliştirilmiş ve çalıştırılmıştır.

## İçindekiler
### Proje Açıklaması
### Gereksinimler
### Kurulum
### Kullanım
### Sürüm Bilgileri
### Yardım ve Destek
### Proje Açıklaması

## Gereksinimler
### Bu projeyi çalıştırmak için aşağıdaki yazılımların kurulu olması gerekmektedir:
Docker: 27.1.1, build 6312585

Docker Compose: v2.29.1-desktop.1

### Proje ayrıca aşağıdaki Python kütüphanelerine ihtiyaç duyar:

 - fastapi
 - uvicorn
 - celery
 - redis
 - requests
 - beautifulsoup4
 - pandas
 - scikit-learn
 - google-generativeai

## Kurulum
Docker ve Docker Compose Yükleme: Docker ve Docker Compose'u Docker'ın resmi web sitesinden ve Docker Compose GitHub sayfasından indirip kurun.

### Proje Dosyalarını İndirme: GitHub üzerindeki projeyi klonlayın veya indirin:

```bash
git clone https://github.com/kullanici_adiniz/enterprise-project-wgemini.git
```

### Docker İmajlarını Oluşturma: Proje dizinine gidin ve Docker imajlarını oluşturun:
```bash
cd enterprise-project-wgemini
docker-compose build
```

## Kullanım
### Docker Konteynerlerini Başlatma: Aşağıdaki komutu kullanarak gerekli Docker konteynerlerini başlatın:

```bash
docker-compose up
```

### Celery Görevlerini Çalıştırma: Celery worker konteynerini başlatın:

```bash
docker-compose run --rm celery-worker
```
## Web API'yi Erişme: FastAPI web uygulamasına tarayıcınızdan http://localhost:8000 adresinden erişebilirsiniz.

## Görevleri Çalıştırma: scrape_and_process görevini çalıştırmak için Celery görev kuyruğuna gönderebilirsiniz.
