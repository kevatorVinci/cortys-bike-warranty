# Module de garantie — notes de conception

## Environnement

- Odoo 19.0, installé depuis les sources.
- Base de travail : velkebin_local.
- Module : cortys_bike_warranty.

## Standard vérifié dans le code local

- repair.order possède le champ under_warranty.
- Les lignes de vente des pièces sont créées à prix nul sous garantie.
- Une modification de under_warranty par write() déclenche
  _update_sale_order_line_price().
- Ne pas réimplémenter ce mécanisme.
- Ne pas supposer que cela corrige une facture déjà comptabilisée.

## À développer

- Durée de garantie configurable sur le produit, en mois.
- Identification de la livraison initiale du vélo par numéro de série.
- Date de fin de garantie.
- Statut de couverture visible sur la réparation.
- Alimentation explicite du champ standard `under_warranty` par le bouton de
  vérification, afin de conserver le mécanisme standard de tarification des
  pièces.

## Règles à finaliser

- Ne pas redémarrer la garantie lors d'une restitution après réparation.
- Vérifier le produit, le numéro de série, le client et la société.
- Signaler une livraison introuvable plutôt qu'une garantie expirée.
- Définir une date de référence conservée pour évaluer la couverture.
- Définir le comportement si un devis ou une facture existe déjà.

## Prochaine séance

1. Ajouter le dossier addons du projet au lancement d'Odoo.
2. Vérifier que le module est détecté.
3. Installer le squelette sur une base de développement sauvegardée.
4. Ajouter les champs et les tests progressivement.
