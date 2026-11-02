#!/usr/bin/env python3
"""
Compare les classes de Reinert des articles bretons et de leurs versions françaises.

Le script lit les deux tableaux produits par classes_par_article.py et les
rapproche par l'identifiant commun *id_. Pour chaque classe bretonne, il
calcule comment se répartissent, entre les classes françaises, les segments
des versions françaises des mêmes articles.

Usage :
  python3 comparer_classes.py resultats/classes_par_article_br.csv \
      resultats/classes_par_article_fr.csv
"""
import sys

import pandas as pd

br = pd.read_csv(sys.argv[1])
fr = pd.read_csv(sys.argv[2])

# 1. Rapprocher les articles des deux langues par leur identifiant commun
paires = br.merge(fr, on="id", suffixes=("_br", "_fr"))
print(f"{len(paires)} paires d'articles\n")

# 2. Pour chaque classe bretonne (classe dominante de l'article breton),
#    additionner les segments français de chaque classe française
classes_fr = [c for c in fr.columns if c.startswith("classe_") and c != "classe_0"]
colonnes = [c + "_fr" for c in classes_fr]
tableau = paires.groupby("dominante_br")[colonnes + ["classe_0_fr"]].sum()

# 3. En pourcentage des segments français classés, plus la part de non classés
pourcents = 100 * tableau[colonnes].div(tableau[colonnes].sum(axis=1), axis=0)
pourcents["non_classes_%"] = 100 * tableau["classe_0_fr"] / tableau.sum(axis=1)
pourcents["segments_fr"] = tableau.sum(axis=1)
print("Classes françaises des mêmes articles, selon leur classe bretonne (%)")
print(pourcents.round(0).astype(int).to_string())

# 4. Le même croisement, article par article (classes dominantes)
print("\nArticles : classe bretonne (lignes) x classe française (colonnes)")
print(pd.crosstab(paires["dominante_br"], paires["dominante_fr"], margins=True))
