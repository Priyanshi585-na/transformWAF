# Transformer-Based Web Application Firewall (WAF)

A real-time Web Application Firewall built using a Transformer-based model and integrated with Nginx via the `auth_request` module.

The system inspects every incoming HTTP request and blocks malicious traffic before it reaches the protected application.

The demo application used is OWASP Juice Shop.

---

## Architecture

Client  
↓  
Nginx (auth_request)  
↓  
FastAPI (ML Inference Service)  
↓  
OWASP Juice Shop  

### Request Flow

1. Client sends HTTP request.
2. Nginx intercepts request.
3. Nginx sends internal subrequest to `/ml_check`.
4. FastAPI evaluates request using Transformer model.
5. If malicious → returns `403 Forbidden`.
6. If benign → request forwarded to Juice Shop.

---

## Features

- Real-time request inspection
- Transformer-based anomaly detection
- Nginx reverse proxy integration
- Non-blocking inference (multi-worker FastAPI)
- Logging for dataset expansion
- Live malicious payload detection demo

---

## Project Structure

├── app.py  
├── process.py  
├── preprocessing.py  
├── artifacts/  
│   ├── lr_model.pkl/  
│   └── vectorizer.pkl  
├── nginx.conf  
├── data/  
│   └── combined_dataset.csv  
└── train.py 

---

# Setup Instructions

## 1. Start OWASP Juice Shop

docker run -d \
  --name juice-shop \
  -p 3000:3000 \
  bkimminich/juice-shop

Verify at:
http://localhost:3000

---

## 2. Start FastAPI ML Service

uvicorn app:app --reload

Verify at:
http://localhost:8000

---

## 3. Start Nginx with Mounted Configuration

docker run -d \
  --name waf-nginx \
  -p 80:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx


---

# Demo

## Normal Traffic

Open:
http://localhost

Juice Shop should load normally.

---

## Malicious Payload Injection

curl "http://localhost/?q=' UNION 1=1 --"

If classified as malicious:
- FastAPI returns 403
- Nginx blocks request
- Response: 403 Forbidden

---

## Logging

Each evaluated request is appended to:

data/combined_dataset.csv  

These logs can be used for future model improvements.

---

# Technical Stack

- FastAPI
- Hugging Face Transformers
- Nginx (auth_request module)
- Docker
- OWASP Juice Shop

---

# Summary

This project demonstrates:

- End-to-end ML deployment
- Real-time request interception
- Reverse proxy enforcement
- Live malicious payload blocking
- Secure integration without modifying application code
