


# DevSecOps Docker

**Classe** : *E5API*
**Date** : *10 juillet 2025*

---

## 🧠 Répartition des tâches

| Membre          | Rôle principal                                 |
| --------------- | ---------------------------------------------- |
| Nadia Kodad     | Intégration backend Django/FastAPI + DockerHub |
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


=======
Voici les étapes claires et détaillées à ajouter dans votre README.md pour lancer le projet :
📌 Instructions d'Installation & Lancement
markdown

## 🚀 Prérequis
- Docker 20.10+ ([Installation](https://docs.docker.com/engine/install/))
- Docker Compose 2.12+ ([Guide](https://docs.docker.com/compose/install/))
- Compte Docker Hub (pour pull/push les images)
- Clés API Stripe (mode test) ([Obtenir des clés](https://dashboard.stripe.com/test/apikeys))

## 🔧 Configuration Initiale
1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/votre-username/projet-e5-devsecops.git
   cd projet-e5-devsecops

    Configurez les variables d'environnement :
    Créez un fichier .env à la racine (copiez le modèle) :
    bash

cp .env.example .env

Éditez le fichier .env avec vos clés Stripe :
ini

    STRIPE_PUBLIC_KEY=pk_test_votreclef
    STRIPE_SECRET_KEY=sk_test_votreclef

🐳 Lancement avec Docker Compose
bash

# Construire les images (premier lancement)
docker-compose build

# Démarrer tous les services en arrière-plan
docker-compose up -d

# Vérifier l'état des conteneurs
docker-compose ps

🌐 Accès aux Applications
Service	URL	Port	Accès
Reverse Proxy	http://localhost	80	Nginx
App Statique	http://localhost/app	8080	HTML/JS
API Node	http://localhost/api	3000	REST
Service Python	http://localhost/service	5000	Flask
App Vulnérable	http://localhost:9999	9999	Accès direct
🛑 Arrêt & Nettoyage
bash

# Arrêter les conteneurs
docker-compose down

# Supprimer les volumes (optionnel)
docker-compose down -v

# Nettoyer les images inutilisées
docker system prune -f

🔍 Dépannage

    Problème de ports : Vérifiez qu'aucun service ne tourne déjà sur les ports 80, 3000, 5000, 9999
    bash

netstat -tuln | grep <PORT>

Logs des conteneurs :
bash

docker-compose logs -f [nom_service]  # Ex: docker-compose logs -f api

Mettre à jour une image :
bash

    docker-compose build [service] && docker-compose up -d --no-deps [service]

📦 Publication sur Docker Hub
bash

# Se connecter à Docker Hub
docker login

# Rebuild et pousser une image (ex: app statique)
docker-compose build static-app
docker tag projet-e5-static-app votreusername/static-app:latest
docker push votreusername/static-app:latest

🎯 Exemple d'intégration Stripe (Bonus)

Pour tester le paiement :

    Accédez à http://localhost/app/checkout

    Utilisez une carte de test Stripe :
    text

    Numéro : 4242 4242 4242 4242
    Date : 12/34 | CVV : 123

📝 Notes supplémentaires

    Les fichiers critiques :

        docker-compose.yml : Configuration globale de la stack

        nginx/conf.d/app.conf : Configuration du reverse proxy

        apps/*/Dockerfile : Fichiers d'optimisation par service
