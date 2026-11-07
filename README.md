## Lancer Odoo avec le module

La commande suivante permet de choisir entre deux bases :

- `velkebin_local` : base d’origine.
- `velkebin_dev_clean` : base dédiée au scénario de démonstration.

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d velkebin_local,velkebin_dev_clean \
  --db-filter='^(velkebin_local|velkebin_dev_clean)$' \
  --max-cron-threads=0 \
  --http-interface=127.0.0.1
```

### Choisir une base

Ouvrir le sélecteur de bases :

http://localhost:8069/web/database/selector

Puis sélectionner `velkebin_local` ou `velkebin_dev_clean`.

Si le sélecteur est désactivé, vérifier que le fichier `odoo.conf` contient :

```ini
list_db = True
```

### Installer ou mettre à jour le module

Pour installer ou mettre à jour le module, cibler uniquement la base concernée.

Exemple de mise à jour sur la base de démonstration :

```bash
/home/Kevator/odoo/venv/bin/python /home/Kevator/odoo/odoo/odoo-bin \
  -c /home/Kevator/odoo/odoo.conf \
  --addons-path=/home/Kevator/odoo/odoo/odoo/addons,/home/Kevator/odoo/odoo/addons,/home/Kevator/projets/cortys-bike-warranty/addons \
  -d velkebin_dev_clean \
  -u cortys_bike_warranty \
  --stop-after-init \
  --max-cron-threads=0 \
  --no-http
```

- Première installation : remplacer `-u` par `-i`.
- Pour cibler la base d’origine : remplacer `velkebin_dev_clean` par `velkebin_local`.
- Arrêter le serveur Odoo avant la mise à jour, puis le relancer avec la commande donnant accès aux deux bases.
