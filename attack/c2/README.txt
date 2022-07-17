1) Installer les dépendances Python ()
> pip install -r requirements.txt

2) Pour lancer le serveur
> export FLASK_APP=c2
> flask run --eager-loading --host=0.0.0.0
(host 0.0.0.0 pour le mettre sur toutes les interfaces, donc accessible via l'host)

