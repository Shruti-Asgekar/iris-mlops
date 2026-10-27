# Iris Species Predictor — MLOps with CI/CD & Monitoring (ISE-2, UDSPC0732)

**Problem statement:** Build a small ML web app (Flask + scikit-learn) that predicts
the Iris flower species, and automate its build, test and deployment using
Git/GitHub → Jenkins → Docker, with Prometheus + Grafana monitoring.

## Architecture
Developer → GitHub → Jenkins (Install → Test → Docker Build → Deploy) → Container (port 5000) → Prometheus (9090) → Grafana (3000)

## Tools to install & verify (screenshot each for your report)
| Tool | Verify command |
|---|---|
| Python | `python --version` |
| Git | `git --version` |
| Docker | `docker --version` and `docker run hello-world` |
| Jenkins | open http://localhost:8080 |
| Prometheus / Grafana | via docker compose |

## Run locally
```
pip install -r requirements.txt
python train.py          # creates model.pkl
pytest -v                # 4 tests should pass
python app.py            # http://localhost:5000
```

## Run with Docker
```
docker build -t iris-mlops .
docker run -d -p 5000:5000 --name iris-app iris-mlops
curl http://localhost:5000/health
```

## Run app + monitoring
```
docker compose up -d --build
```
- App: http://localhost:5000
- Metrics: http://localhost:5000/metrics
- Prometheus: http://localhost:9090  (Status → Targets should show UP)
- Grafana: http://localhost:3000 (admin/admin) → Add data source → Prometheus → URL `http://prometheus:9090`
- Useful queries: `app_requests_total`, `app_predictions_total`, `rate(app_requests_total[1m])`, `app_errors_total`

## GitHub + Jenkins setup
1. `git init && git add . && git commit -m "initial"` ; create repo on GitHub; `git remote add origin <url>` ; `git push -u origin main`
2. Jenkins: install suggested plugins (+ Docker Pipeline, Git). Jenkins user needs docker access: `sudo usermod -aG docker jenkins` then restart Jenkins.
3. New Item → **Pipeline** → Pipeline script from SCM → Git → your repo URL → Script Path `Jenkinsfile`.
4. Build Now → capture Stage View screenshot (all green).
5. Optional auto-trigger: GitHub webhook / Poll SCM `H/2 * * * *`.

## Endpoints
`GET /` UI · `POST /predict` JSON · `GET /health` · `GET /metrics`

Sample: `curl -X POST localhost:5000/predict -H "Content-Type: application/json" -d '{"sepal_length":6.5,"sepal_width":3,"petal_length":5.5,"petal_width":2}'` → virginica

## Checklist for the PDF report (LAB-ISE2 template)
- [ ] Problem statement & objective, architecture diagram
- [ ] Tool versions + install/verify screenshots
- [ ] GitHub repo link, commit history screenshot
- [ ] Jenkinsfile explanation, successful Jenkins build screenshot
- [ ] Docker image/container screenshot (`docker ps`)
- [ ] App UI prediction screenshot
- [ ] Prometheus targets UP + Grafana dashboard screenshot
- [ ] Conclusion, challenges faced
