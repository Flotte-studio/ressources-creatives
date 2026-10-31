"""Télécharge l'onglet Ressources (CSV publié) et écrit data.json pour la page."""
import csv, io, json, os, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

raw = urllib.request.urlopen(os.environ["SHEET_CSV_URL"], timeout=60).read().decode("utf-8")
items = []
for r in csv.DictReader(io.StringIO(raw)):
    g = lambda k: (r.get(k) or "").strip()
    if not g("Nom"):
        continue
    items.append({
        "nom": g("Nom"), "lien": g("Lien"), "categorie": g("Catégorie"), "format": g("Format"),
        "tags": [t.strip() for t in g("Tags").split(",") if t.strip()],
        "description": g("Description"), "cout": g("Coût"), "verif": g("À vérifier").lower() == "oui",
    })
if len(items) < 10:  # garde-fou : ne jamais écraser la page avec un export vide ou cassé
    raise SystemExit("Export suspect (moins de 10 lignes) : mise à jour annulée.")
with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d"), "items": items},
              f, ensure_ascii=False, indent=1)
print(len(items), "ressources écrites.")
