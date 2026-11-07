# Cortys Bike Warranty

Exercice Odoo : fabrication, vente, livraison, facturation et réparation de vélos suivis par numéro de série.

## Objectif

Réutiliser le standard Odoo et développer uniquement les fonctionnalités de garantie manquantes :

- durée de garantie (en mois) sur la fiche produit ;
- date de livraison initiale du vélo retrouvée via son numéro de série ;
- date de fin de garantie et statut affichés sur l'ordre de réparation ;
- bouton « Vérifier la garantie » qui coche le champ standard `under_warranty`
  (Odoo met alors le prix des pièces à 0).

## Organisation

- `addons/cortys_bike_warranty/` : module personnalisé
- `docs/` : notes de conception et scénario de démonstration (`docs/scenario_test.md`)

La sauvegarde de la base et le filestore ne sont pas versionnés.

## Prérequis

- Odoo 19.0 installé depuis les sources, avec son environnement virtuel
- Modules `repair` et `sale_stock` (installés automatiquement comme dépendances)

Adapter les chemins ci-dessous à votre installation.

## Lancer Odoo avec le module

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d velkebin_local \
  --db-filter='^velkebin_local$' \
  --max-cron-threads=0 \
  --http-interface=127.0.0.1
```

Puis ouvrir http://localhost:8069.

- Première installation : ajouter `-i cortys_bike_warranty`
- Après une modification du code : ajouter `-u cortys_bike_warranty`

## Lancer les tests automatisés

De préférence sur une base dédiée aux tests :

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d cortys_warranty_test \
  -i cortys_bike_warranty \
  --test-tags /cortys_bike_warranty \
  --stop-after-init \
  --without-demo=all \
  --max-cron-threads=0 \
  --no-http
```

Résultat attendu en fin de log : `0 failed, 0 error(s)`.
Pour relancer sur une base où le module est déjà installé, remplacer `-i` par `-u`.
