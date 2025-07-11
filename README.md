

# DevSecOps Docker

**Classe** : *E5API*
**Date** : *10 juillet 2025*

---

## 🧠 Répartition des tâches

| Membre          | Rôle principal                                 |
| --------------- | ---------------------------------------------- |
|Nadia Kodad| Intégration backend Django/FastAPI + DockerHub |
| Khadija Sy      | Configuration Flask et reverse proxy Traefik   |
| Cylia Hamdi     | Gestion PHP statique + docker-compose final    |

---

## 🗂️ Structure du projet

```
devsecops-e5/
├── priv-rocket-ecommerce-main/        # Django + Stripe
├── FastApi-Docker-main/               # API FastAPI + MySQL
├── flask-datta-1752138310-main/       # Dashboard Flask
├── ProjetDevOps-main/                 # Site statique PHP vulnérable
├── docker-compose.yml
├── nginx.conf (pour tests alternatifs)
└── README.md
```

---

## ⚙️ Technologies & choix expliqués

| Élément            | Choix technique                | Justification                            |
| ------------------ | ------------------------------ | ---------------------------------------- |
| Backend 1          | Django + Stripe                | Gestion de paiements, framework complet  |
| Backend 2          | FastAPI + SQLAlchemy + MySQL   | API moderne, rapide et sécurisée         |
| Frontend           | Flask (dashboard web)          | Léger, facile à dockeriser               |
| Statique (pentest) | App PHP vulnérable (DVWA-like) | Pour tests de sécurité (Whitebox)        |
| Orchestration      | Docker Compose                 | Déploiement simple en local              |
| Reverse Proxy      | Traefik v2                     | Routage dynamique basé sur labels Docker |
| Stockage cloud     | Docker Hub                     | Partage public des images                |
| Versioning         | Git & GitHub                   | Travail collaboratif, suivi, traçabilité |

---

## 🧱 docker-compose.yml *(extrait représentatif)*

```yaml
services:
  ecommerce:
    build: ./priv-rocket-ecommerce-main
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ecommerce.rule=Host(`stripe.localhost`)"
      - "traefik.http.services.ecommerce.loadbalancer.server.port=8000"
    networks: [web]

  fastapi:
    build: ./FastApi-Docker-main
    depends_on: [fastapi-db]
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.fastapi.rule=Host(`api.localhost`)"
      - "traefik.http.services.fastapi.loadbalancer.server.port=8000"
    networks: [web, db]

  fastapi-db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: item_db
    volumes:
      - mysql_data:/var/lib/mysql
    networks: [db]

  flask:
    build: ./flask-datta-1752138310-main
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.flask.rule=Host(`flask.localhost`)"
      - "traefik.http.services.flask.loadbalancer.server.port=5000"
    networks: [web]

  php-app:
    build: ./ProjetDevOps-main
    ports:
      - "8080:80"  # Exposé sans reverse proxy pour les pentests
    networks: [web]

  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8081:8080"  # Dashboard Traefik
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks: [web]

volumes:
  mysql_data:

networks:
  web:
  db:
```

---

## 📚 Étapes détaillées avec commandes

### 1. 🔧 Build et lancement local

```bash
docker compose up --build
```

✅ Vérification sur `http://localhost:8081` (Traefik)

---

### 2. ⚙️ Test des accès (via `/etc/hosts`)

```bash
sudo nano /etc/hosts
```

Ajout :

```
127.0.0.1 stripe.localhost
127.0.0.1 api.localhost
127.0.0.1 flask.localhost
```

---

### 3. ☁️ Connexion Docker Hub

```bash
docker login
```

---

### 4. 📤 Push des images Docker

```bash
# Exemple pour Flask
docker tag flask cyliahamdi/flask-app
docker push cyliahamdi/flask-app

# Exemple pour FastAPI
docker tag fastapi cyliahamdi/fastapi-app
docker push cyliahamdi/fastapi-app
```

---

## 🖼️ Architecture du projet (schéma)

```
[ Client Navigateur ]
        |
        ▼
  ┌────────────┐
  │  Traefik   │──────────────┐
  └────┬───────┘              │
       │                      │
───── Apps derrière proxy ───┘
│
├─ ecommerce (stripe.localhost)
├─ fastapi (api.localhost)
├─ flask (flask.localhost)
│
└─ php-app exposée en 8080 pour pentest
```

---

## ✅ Résultats & Tests

| Application     | Accès                                                    | Statut |
| --------------- | -------------------------------------------------------- | ------ |
| Django + Stripe | [http://stripe.localhost](http://stripe.localhost)       | ✅      |
| FastAPI         | [http://api.localhost](http://api.localhost)             | ✅      |
| Flask Dashboard | [http://flask.localhost](http://flask.localhost)         | ✅      |
| PHP Pentest     | [http://localhost:8080](http://localhost:8080)           | ✅      |
| Reverse Proxy   | [http://localhost:8081](http://localhost:8081) (Traefik) | ✅      |

---


