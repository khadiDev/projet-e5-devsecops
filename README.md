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