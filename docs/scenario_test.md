# Scénario de recette complet — Cortys Bike Warranty

Base conseillée : une copie de `velkebin_local` (ou une base de test).
Cochez chaque case `[ ]` au fur et à mesure. Si un résultat diffère, notez l'écran et arrêtez-vous.

## 0. Préparation

- [ ] Odoo démarre sans erreur avec `-u cortys_bike_warranty` (voir README).
- [ ] Apps → retirer le filtre « Apps » → « Cortys Bike Warranty » est **installé**.
- [ ] Les tests automatisés passent : `0 failed, 0 error(s)`.

## 1. Fiche produit

| # | Action | Résultat attendu |
|---|--------|------------------|
| 1.1 | Ouvrir « Vélo pour adulte » | Champ `Warranty Duration (Months)` après la catégorie |
| 1.2 | Saisir `24`, enregistrer, recharger | La valeur reste `24` |
| 1.3 | Saisir `-1`, enregistrer | Refus : « The warranty duration cannot be negative » |
| 1.4 | Annuler la modification | Retour à `24` |
| 1.5 | Vérifier « Vélo pour enfant » | Mettre `24` aussi (ou la valeur de l'énoncé) |
| 1.6 | Vérifier une pièce (Chaîne) | Durée `0`, prix de vente > 0 (ex. 15 €) |
| 1.7 | Vérifier le suivi | Les vélos sont suivis **par numéro de série** |

## 2. Achat des composants (avec réception partielle)

| # | Action | Résultat attendu |
|---|--------|------------------|
| 2.1 | Achats → nouvelle demande : 2 cadres, 2 chaînes, 4 roues… → Confirmer | Bon de commande + 1 réception |
| 2.2 | Réception : ne recevoir que 1 cadre, le reste complet → Valider → **Créer un reliquat** | Stock cadre +1, reliquat pour 1 cadre |
| 2.3 | Valider le reliquat | Stock cadre total = 2 |
| 2.4 | Créer la facture fournisseur, confirmer, payer | Statut `Payé` ou `En paiement` |

## 3. Fabrication

| # | Action | Résultat attendu |
|---|--------|------------------|
| 3.1 | Fabrication → nouvel OF « Vélo pour adulte », qté 1 | Composants réservés |
| 3.2 | Attribuer le numéro `VELO-TEST-01` → Produire | OF `Fait`, 1 vélo en stock avec ce numéro |
| 3.3 | Refaire pour `VELO-TEST-02` | 2 vélos en stock |

## 4. Vente, livraison, facture

Client : `Client Recette` (nouveau, aucun historique).

| # | Action | Résultat attendu |
|---|--------|------------------|
| 4.1 | Devis : 1 vélo adulte → Confirmer | Bouton `Delivery 1` |
| 4.2 | Livraison : choisir `VELO-TEST-01` → Valider | Statut `Fait`, `WH/Stock → Partners/Customers` |
| 4.3 | Créer facture → confirmer → payer | Facture `Payée` |
| 4.4 | Noter la **date effective** de la livraison | Elle servira de point de départ |

## 5. Cas A — Réparation SOUS garantie (cas principal)

| # | Action | Résultat attendu |
|---|--------|------------------|
| 5.1 | Livraison 4.2 → `Return` → valider le retour | `VELO-TEST-01` revient dans `WH/Stock` |
| 5.2 | Réparations → Nouveau : Client Recette, vélo adulte, `VELO-TEST-01` | — |
| 5.3 | Lire les champs | `Customer Delivery Date` = date 4.4 ; `Warranty End Date` = +24 mois ; statut `Sous garantie` |
| 5.4 | Lire la bannière | Verte : « Sous garantie jusqu'au … » |
| 5.5 | Vérifier la case `Under Warranty` | Encore **décochée** (normal : pas encore vérifiée) |
| 5.6 | Cliquer **Vérifier la garantie** | Case `Under Warranty` **cochée** |
| 5.7 | Pièces : ajouter Chaîne, type `Add`, qté 1 | Disponible (sinon racheter une chaîne) |
| 5.8 | Créer le devis | Ligne Chaîne à **0,00 €** |
| 5.9 | Confirmer → Démarrer → Terminer la réparation | Statut `Réparé` ; bouton « Vérifier » disparaît |
| 5.10 | Relire les dates | Identiques à 5.3 (la réparation ne prolonge pas la garantie) |
| 5.11 | Livrer le vélo réparé au client (`WH/Stock → Customers`, `VELO-TEST-01`) | Transfert `Fait` |
| 5.12 | Créer une **nouvelle** réparation pour `VELO-TEST-01` | `Customer Delivery Date` = toujours la date 4.4, **pas** celle de 5.11 |

## 6. Cas B — Garantie EXPIRÉE

| # | Action | Résultat attendu |
|---|--------|------------------|
| 6.1 | Nouvelle réparation sur `VELO-TEST-01`, `Scheduled Date` = date 4.4 + 25 mois | Statut `Garantie expirée`, bannière orange |
| 6.2 | Cocher manuellement `Under Warranty`, puis cliquer **Vérifier la garantie** | La case est **décochée** |
| 6.3 | Ajouter Chaîne → Créer le devis | Chaîne au **prix normal** |
| 6.4 | Annuler cette réparation | Statut `Annulé` |

## 7. Cas C — Pas de garantie sur le produit

| # | Action | Résultat attendu |
|---|--------|------------------|
| 7.1 | Mettre la durée du vélo adulte à `0` | — |
| 7.2 | Nouvelle réparation `VELO-TEST-01` | Statut `Aucune garantie`, bannière grise, pas de date de fin |
| 7.3 | Vérifier la garantie | Case décochée |
| 7.4 | Remettre la durée à `24` | Statut redevient `Sous garantie` après rechargement |

## 8. Cas D — Informations manquantes

| # | Action | Résultat attendu |
|---|--------|------------------|
| 8.1 | Réparation sans numéro de série | Statut `Informations manquantes`, bannière bleue |
| 8.2 | Réparation avec `VELO-TEST-02` (jamais livré) | `Customer Delivery Date` vide, `Informations manquantes` |
| 8.3 | Réparation `VELO-TEST-01` mais **autre client** | `Informations manquantes` (le vélo n'a pas été livré à ce client) |
| 8.4 | Réparation `VELO-TEST-01`, `Scheduled Date` **avant** la livraison | `Informations manquantes` |
| 8.5 | Dans chaque cas, cocher la case puis Vérifier | La case est décochée |

## 9. Cas limites de dates

| # | Action | Résultat attendu |
|---|--------|------------------|
| 9.1 | `Scheduled Date` = exactement la date de fin de garantie | `Sous garantie` (borne incluse) |
| 9.2 | `Scheduled Date` = fin de garantie + 1 jour | `Garantie expirée` |

## 10. Cas E — Garantie retirée après création du devis

| # | Action | Résultat attendu |
|---|--------|------------------|
| 10.1 | Réparation sous garantie, Vérifier, ajouter Chaîne, créer le devis | Chaîne à 0 € |
| 10.2 | Décocher `Under Warranty` | Ligne de devis recalculée au prix normal (standard Odoo) |
| 10.3 | Recocher | Ligne repasse à 0 € |

## 11. Contrôles finaux

- [ ] Aucune erreur dans le terminal pendant tout le scénario.
- [ ] Stock de `VELO-TEST-01` cohérent : chez le client à la fin.
- [ ] Stock des chaînes diminué uniquement des pièces réellement utilisées.
- [ ] Aucune facture client créée pour la réparation sous garantie, ou facture à 0 € pour les pièces.
- [ ] `git status` propre, dernier commit poussé sur GitHub.

## Limites connues (à mentionner dans le rapport)

- La case `Under Warranty` n'est appliquée qu'au clic sur « Vérifier la garantie » (choix volontaire).
- `delivery_date` n'est pas stocké : non filtrable dans les listes.
- La main-d'œuvre éventuelle n'est pas couverte par le mécanisme standard des pièces.
