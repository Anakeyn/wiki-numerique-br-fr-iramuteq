#!/usr/bin/env python3
"""
Rend uniques les identifiants *id_ d'un corpus produit par wiki2iramuteq.

wiki2iramuteq construit *id_ à partir du titre : il retire les caractères
spéciaux et coupe à 50 caractères. Deux titres différents peuvent alors donner
le même identifiant : « Internet » et « Internet+ » donnent tous deux *id_Internet.
Ce script ajoute _2, _3... aux doublons, dans le corpus et dans le CSV de
métadonnées, que l'on parcourt dans le même ordre.

Usage :
  python3 corriger_identifiants.py corpus.txt
  (le CSV <corpus>_metadonnees.csv est cherché à côté ; les deux fichiers sont réécrits)
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path


def nouvel_id(vus, ident):
    """Premier passage : ident ; passages suivants : ident_2, ident_3...
    (en sautant un suffixe déjà pris par un autre article)."""
    vus[ident] += 1
    if vus[ident] == 1:
        return ident
    n = vus[ident]
    while f"{ident}_{n}" in existants:
        n += 1
    vus[ident] = n
    return f"{ident}_{n}"


f_txt = Path(sys.argv[1])
f_csv = f_txt.with_name(f_txt.stem + "_metadonnees.csv")

texte = f_txt.read_text(encoding="utf-8")
existants = set(re.findall(r"\*id_(\S+)", texte))

# Corpus : une ligne étoilée par article
vus, corriges, lignes = Counter(), [], []
for ligne in texte.splitlines(keepends=True):
    if ligne.startswith("****"):
        ancien = re.search(r"\*id_(\S+)", ligne).group(1)
        nouveau = nouvel_id(vus, ancien)
        if nouveau != ancien:
            ligne = ligne.replace(f"*id_{ancien}", f"*id_{nouveau}", 1)
            corriges.append(nouveau)
    lignes.append(ligne)
f_txt.write_text("".join(lignes), encoding="utf-8")

# Métadonnées : seuls les articles retenus figurent dans le corpus
with open(f_csv, encoding="utf-8") as f:
    rangs = list(csv.DictReader(f))
vus = Counter()
for r in rangs:
    if r["retenu"] == "1":
        r["id"] = nouvel_id(vus, r["id"])
with open(f_csv, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rangs[0].keys()))
    w.writeheader()
    w.writerows(rangs)

print(f"{len(corriges)} identifiant(s) corrigé(s) : {', '.join(corriges) or 'aucun'}")
