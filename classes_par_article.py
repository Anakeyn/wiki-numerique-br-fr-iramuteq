#!/usr/bin/env python3
"""
Répartit les segments d'une classification de Reinert d'IRaMuTeQ par article.

IRaMuTeQ classe des segments de texte, pas des articles. Ce script relit le
dossier du corpus (corpus.db) et celui de l'analyse (uce.csv) pour compter,
dans chaque article, combien de segments tombent dans chaque classe.
Il écrit un fichier CSV : une ligne par article, ses variables étoilées,
le nombre de segments par classe (0 = non classé) et sa classe dominante.

Usage :
  python3 classes_par_article.py dossier_corpus dossier_alceste -o sortie.csv

Exemple :
  python3 classes_par_article.py \
      corpus/br/wikipedia_br_numerique_pret_corpus_1 \
      corpus/br/wikipedia_br_numerique_pret_corpus_1/wikipedia_br_numerique_pret_alceste_1 \
      -o resultats/classes_par_article_br.csv

N'utilise que la bibliothèque standard de Python.
"""
import argparse
import csv
import sqlite3
from collections import Counter
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
parser.add_argument("corpus", help="dossier du corpus IRaMuTeQ (contient corpus.db)")
parser.add_argument("alceste", help="dossier de l'analyse (contient uce.csv)")
parser.add_argument("-o", "--sortie", default="classes_par_article.csv")
args = parser.parse_args()

# 1. Les variables de chaque texte, et le texte de chaque segment
base = sqlite3.connect(Path(args.corpus) / "corpus.db")
variables = {}
for uci, ligne, _ in base.execute("SELECT uci, et, paras FROM etoiles"):
    # « **** *art_Unix *equiv_fr_oui » -> {"art": "Unix", "equiv": "fr_oui"}
    variables[uci] = dict(v[1:].split("_", 1) for v in ligne.split()[1:] if "_" in v)
texte_du_segment = {uce: uci for uci, _, uce in base.execute("SELECT uci, para, uce FROM luces")}

# 2. La classe de chaque segment : uce.csv a une ligne par segment, dans l'ordre
with open(Path(args.alceste) / "uce.csv", encoding="utf-8") as f:
    classes = [int(ligne[1]) for ligne in list(csv.reader(f, delimiter=";"))[1:]]
nb_classes = max(classes)

# 3. Compter les segments de chaque classe, article par article
comptes = {uci: Counter() for uci in variables}
for uce, classe in enumerate(classes):
    comptes[texte_du_segment[uce]][classe] += 1

# 4. Écrire le tableau
noms_variables = sorted({nom for v in variables.values() for nom in v})
colonnes = [f"classe_{k}" for k in range(nb_classes + 1)]
with open(args.sortie, "w", encoding="utf-8", newline="") as f:
    ecrivain = csv.writer(f)
    ecrivain.writerow(noms_variables + colonnes + ["segments", "dominante", "part_dominante"])
    for uci in sorted(variables):
        c = comptes[uci]
        total = sum(c.values())
        dominante, n = max(c.items(), key=lambda kv: (kv[1], kv[0] != 0, -kv[0]))
        ecrivain.writerow([variables[uci].get(nom, "") for nom in noms_variables]
                          + [c[k] for k in range(nb_classes + 1)]
                          + [total, dominante, round(n / total, 2)])
print(f"{len(variables)} articles, {len(classes)} segments -> {args.sortie}")
