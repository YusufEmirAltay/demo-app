1. Proje ve Uygulama Hazırlığı
	1.	Yeni bir repo / klasör aç, içine:
	•	app.js (Node) veya app.py (Flask).
	•	/metrics endpoint'i; rastgele veya sayaç artan bir sayı döndürsün.
	•	/ endpoint'i: "Hello from Demo-App!" ve DB'den son kaydı göstersin.
	2.	requirements.txt veya package.json oluştur.

2. Dockerizasyon
	1.	Dockerfile yaz (uygulamayı, SQLite dosyasını /data klasörüne koyacak).
	2.	Local registry'ye (ya da Docker Hub'a) image'ı tag'leyip push et.

3. İlk Kubernetes Deploy
	1.	deployment.yaml & service.yaml oluştur, app'i Minikube'a deploy et.
	2.	kubectl get pods,svc ile çalıştığını doğrula.

4. Pod Affinity / Anti-Affinity
	1.	Minikube'u 2 node'lu başlat.
	2.	deployment.yaml içine affinity ve antiAffinity bölümlerini ekle:
	•	Aynı label'lı pod'lar farklı node'lara gitsin.
	3.	kubectl get pods -o wide ile dağılımı kontrol et.

5. Custom Metrics + Autoscaling
	1.	Uygulamanın /metrics endpoint'ini Prometheus'un scrape edebileceği formatta bırak.
	2.	Helm ile Prometheus + Prometheus Adapter kur.
	3.	HPA manifest'i yaz: custom metric'e göre (örn. /metrics sayısına göre) scale yapılsın (min 1, max 5).
	4.	Yük testi (curl loop) ile pod artışını gözle.

6. Custom Resource Definition (CRD)
	1.	Basit bir CRD tanımla (MyAppConfig): içinde greetingMessage alanı bulunsun.
	2.	crd.yaml ve örnek myappconfig.yaml oluşturup apply et.
	3.	Uygulamanın config'ini bu CRD'den çekmesi için (örneğin env vars) küçük bir kod parçası ekle.
	4.	kubectl get myappconfigs ile çalıştığını kontrol et.

7. Pod Disruption Budget + Chaos
	1.	Deployment'ı 3 replika yap.
	2.	pdb.yaml ile minAvailable: 2 tanımla.
	3.	Basit bir bash script veya cronjob ile rastgele kubectl delete pod komutları at.
	4.	Uygulamanın ayakta kaldığını doğrula.

8. Network Policy Güvenliği
	1.	Aynı namespace'de iki farklı label'lı pod (örn. frontend, backend) çalıştır.
	2.	networkpolicy.yaml ile sadece frontend → backend trafiğine izin ver; diğer tüm trafiği engelle.
	3.	Busybox test pod'ları ile hem izinli hem engelli istekleri göster.

9. Persistent Volume Kullanımı
	1.	Deployment'da SQLite veritabanını /data yoluna yazdır.
	2.	PVC ve (Minikube'un default) StorageClass kullanarak pvc.yaml oluştur.
	3.	Pod'u silip yeniden yarat: verinin kalıcılığını kubectl exec + cat /data/db.sqlite ile kontrol et.

10. CI/CD Pipeline (Bonus)
	1.	.github/workflows/deploy.yml ya da Jenkinsfile ekle.
	2.	Adımlar: push → Docker build → image push → kubectl apply → kubectl rollout status.
	3.	Gerekirse helm upgrade --install veya kubectl kustomize kullan.
