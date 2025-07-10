# Demo-App Kubernetes Deployment ve CI/CD Task'ı

---

## 1. Proje ve Uygulama Hazırlığı
- Yeni bir repo/klasör oluştur.
- İçine aşağıdakileri ekle:
  - `app.js` (Node.js) veya `app.py` (Flask)
  - `/metrics` endpoint: rastgele veya artan sayaç döndürsün.
  - `/` endpoint: "Hello from Demo-App!" mesajı ve DB’den son kayıt gösterilsin.
- `requirements.txt` veya `package.json` oluştur.

## 2. Dockerizasyon
- Uygulamayı ve SQLite dosyasını `/data` klasörüne koyacak şekilde `Dockerfile` yaz.
- Image’ı local registry’ye veya Docker Hub’a tag’leyip push et.

## 3. İlk Kubernetes Deploy
- `deployment.yaml` ve `service.yaml` dosyalarını oluştur.
- Uygulamayı Minikube’a deploy et.
- `kubectl get pods,svc` komutlarıyla çalıştığını doğrula.

## 4. Pod Affinity / Anti-Affinity
- Minikube’u 2 node’lu başlat.
- `deployment.yaml` içine affinity ve antiAffinity bölümlerini ekle:
  - Aynı label’a sahip pod’lar farklı node’lara gitsin.
- `kubectl get pods -o wide` ile dağılımı kontrol et.

## 5. Custom Metrics + Autoscaling
- `/metrics` endpoint’ini Prometheus’un scrape edebileceği formatta bırak.
- Helm ile Prometheus ve Prometheus Adapter kurulumu yap.
- HPA manifest’i oluştur: custom metric’e göre scale (min 1, max 5).
- Yük testi (örn. `curl` loop) ile pod artışını gözlemle.

## 6. Custom Resource Definition (CRD)
- Basit bir CRD tanımla (`MyAppConfig`) içinde `greetingMessage` alanı olsun.
- `crd.yaml` ve örnek `myappconfig.yaml` dosyalarını oluşturup `kubectl apply` et.
- Uygulamanın config’ini bu CRD’den çekmesi için env var ya da küçük kod ekle.
- `kubectl get myappconfigs` ile çalıştığını kontrol et.

## 7. Pod Disruption Budget + Chaos
- Deployment’ı 3 replika yap.
- `pdb.yaml` ile `minAvailable: 2` tanımla.
- Basit bash script veya cronjob ile rastgele `kubectl delete pod` çalıştır.
- Uygulamanın kesintisiz ayakta kaldığını doğrula.

## 8. Network Policy Güvenliği
- Aynı namespace içinde farklı label’lı pod’lar çalıştır (ör. frontend, backend).
- `networkpolicy.yaml` ile sadece frontend → backend trafiğine izin ver, diğer tüm trafiği engelle.
- Busybox test pod’ları ile izinli ve engelli istekleri test et.

## 9. Persistent Volume Kullanımı
- Deployment’da SQLite veritabanını `/data` yoluna yazdır.
- PVC ve Minikube’un default StorageClass ile `pvc.yaml` oluştur.
- Pod’u silip yeniden yarat, verinin kalıcılığını `kubectl exec` + `cat /data/db.sqlite` ile kontrol et.

## 10. CI/CD Pipeline (Bonus)
- `.github/workflows/deploy.yml` veya `Jenkinsfile` ekle.
- Adımlar:
  - Push → Docker build → Image push → `kubectl apply` → `kubectl rollout status`.
- Gerekirse `helm upgrade --install` veya `kubectl kustomize` kullan.

---

**Not:** Her adımda `kubectl logs` ve `kubectl describe` ile pod durumlarını ve hataları kontrol etmeyi unutma.
