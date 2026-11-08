## Lancer Odoo avec le module

L’environnement permet de travailler avec trois bases de données :

| Base | Usage |
|---|---|
| `velkebin_local` | Base d’origine |
| `velkebin_dev_clean` | Base dédiée au scénario de démonstration |
| `velkebin_dev_clean_v1` | Base supplémentaire de démonstration |

### Démarrer le serveur

Exécuter la commande suivante pour lancer Odoo avec le module personnalisé et donner accès aux trois bases :

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d velkebin_local,velkebin_dev_clean,velkebin_dev_clean_v1 \
  --db-filter='^(velkebin_local|velkebin_dev_clean|velkebin_dev_clean_v1)$' \
  --max-cron-threads=0 \
  --http-interface=127.0.0.1
```

### Choisir une base

Ouvrir le sélecteur de bases dans le navigateur :

http://localhost:8069/web/database/selector

Puis sélectionner la base souhaitée :

- `velkebin_local`
- `velkebin_dev_clean`
- `velkebin_dev_clean_v1`

Si le sélecteur est désactivé, vérifier que le fichier
`/home/Kevator/odoo/odoo.conf` contient :

```ini
list_db = True
```

Redémarrer Odoo après toute modification du fichier de configuration.

## Installer ou mettre à jour le module

Effectuer l’installation ou la mise à jour sur une seule base à la fois.

### 1. Arrêter le serveur Odoo

Arrêter le serveur lancé précédemment avant d’exécuter la commande de maintenance.

### 2. Choisir la base cible

Dans le même terminal, définir la base à modifier :

```bash
DB_NAME="velkebin_dev_clean_v1"
```

Remplacer cette valeur par `velkebin_local` ou `velkebin_dev_clean` si nécessaire.

### 3. Mettre à jour le module

Si `cortys_bike_warranty` est déjà installé dans la base cible :

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d "$DB_NAME" \
  -u cortys_bike_warranty \
  --stop-after-init \
  --max-cron-threads=0 \
  --no-http
```

### Première installation

Si le module n’est pas encore installé dans la base cible, utiliser `-i` à la place de `-u` :

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d "$DB_NAME" \
  -i cortys_bike_warranty \
  --stop-after-init \
  --max-cron-threads=0 \
  --no-http
```

### 4. Relancer Odoo

Une fois l’opération terminée, relancer le serveur avec la commande de la section
« Démarrer le serveur », puis sélectionner la base concernée.

> Vérifier la valeur de `DB_NAME` avant chaque installation ou mise à jour.
> L’opération concerne uniquement la base sélectionnée, pas les trois bases.
