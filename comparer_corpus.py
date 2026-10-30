#!/usr/bin/env python3
"""
Compare les corpus « numérique » des Wikipédia bretonne et française
avant leur analyse dans IRaMuTeQ.

Le script lit les corpus au format IRaMuTeQ (lignes « **** *variable_modalite »)
et produit, dans le dossier resultats/ :
  * comparaison_corpus.csv      : une ligne par article (langue, longueur, variables) ;
  * comparaison_synthese.md     : les tableaux de synthèse, prêts à copier ;
  * comparaison_longueurs.png   : longueurs d'articles selon la langue et *equiv_ ;
  * comparaison_paires.png      : longueur br / longueur fr pour les mêmes articles.

Usage :
  python3 comparer_corpus.py
"""
# %% 1. Chemins et bibliothèques
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ICI = Path(__file__).resolve().parent
CORPUS = {
    "br": ICI / "corpus/br/wikipedia_br_numerique_filtre.txt",
    "fr": ICI / "corpus/fr/wikipedia_fr_numerique_nettoye.txt",
}
PAIRES = {
    "br": ICI / "corpus/paires/wikipedia_br_numerique_filtre_aligne_sur_fr.txt",
    "fr": ICI / "corpus/paires/wikipedia_fr_aligne_sur_br_numerique_filtre.txt",
}
SORTIE = ICI / "resultats"
SORTIE.mkdir(exist_ok=True)

MOT = re.compile(r"\w+(?:['’]\w+)*")  # garde « c'hoari » d'un seul tenant


# %% 2. Lire un corpus IRaMuTeQ : une ligne par article
def lire_corpus(chemin):
    """Renvoie un DataFrame : variables étoilées + nombre de mots du texte."""
    articles, courant = [], None
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("****"):
            courant = {"texte": []}
            for var in ligne.split()[1:]:            # « *equiv_fr_oui »
                nom, _, modalite = var[1:].partition("_")
                courant[nom] = modalite              # equiv -> « fr_oui »
            articles.append(courant)
        elif courant is not None:
            courant["texte"].append(ligne)
    for a in articles:
        a["mots"] = len(MOT.findall(" ".join(a.pop("texte"))))
    return pd.DataFrame(articles)


tables = []
for lang, chemin in CORPUS.items():
    d = lire_corpus(chemin)
    d["langue"] = lang
    # titres exacts (accents, apostrophes) pris dans le fichier de métadonnées
    meta = pd.read_csv(chemin.with_name(chemin.stem + "_metadonnees.csv"))
    d = d.merge(meta[["id", "titre"]], on="id", how="left")
    # « fr_oui » -> « oui » : la langue de l'équivalent est l'autre langue
    d["equivalent"] = d["equiv"].str.rsplit("_", n=1).str[-1]
    tables.append(d)
articles = pd.concat(tables, ignore_index=True)
articles.drop(columns=["equiv"]).to_csv(SORTIE / "comparaison_corpus.csv", index=False)


# %% 3. Taille des deux corpus
taille = articles.groupby("langue").agg(
    articles=("id", "count"),
    mots=("mots", "sum"),
    mediane=("mots", "median"),
    moyenne=("mots", "mean"),
).round(0).astype(int)
print("Taille des corpus\n", taille, "\n")


# %% 4. Part des articles qui ont un équivalent dans l'autre langue
equiv = pd.crosstab(articles["langue"], articles["equivalent"], margins=True,
                    margins_name="total")
equiv["% avec équivalent"] = (100 * equiv["oui"] / equiv["total"]).round(1)
print("Articles avec un équivalent dans l'autre Wikipédia\n", equiv, "\n")


# %% 5. Termes de recherche qui ont ramené les articles
termes = (articles.groupby(["langue", "terme"]).size()
          .rename("articles").reset_index()
          .sort_values(["langue", "articles"], ascending=[True, False]))
print("Articles par terme de recherche\n", termes.to_string(index=False), "\n")


# %% 6. Longueur des articles selon la langue et l'existence d'un équivalent
longueur = (articles.groupby(["langue", "equivalent"])["mots"]
            .agg(["count", "median", "mean"]).round(0).astype(int))
print("Longueur selon *equiv_\n", longueur, "\n")

fig, ax = plt.subplots(figsize=(8, 4.5))
groupes = [(l, e) for l in ("br", "fr") for e in ("oui", "non")]
donnees = [articles.query("langue == @l and equivalent == @e")["mots"] for l, e in groupes]
ax.boxplot(donnees, showfliers=False)
ax.set_xticks(range(1, 5), [f"{l}\néquivalent {e}" for l, e in groupes])
ax.set_ylabel("mots par article")
ax.set_title("Longueur des articles (valeurs extrêmes masquées)")
fig.tight_layout()
fig.savefig(SORTIE / "comparaison_longueurs.png", dpi=150)


# %% 7. Les mêmes sujets dans les deux langues : comparer les paires
pbr, pfr = lire_corpus(PAIRES["br"]), lire_corpus(PAIRES["fr"])
paires = pbr[["id", "mots"]].merge(pfr[["id", "mots"]], on="id", suffixes=("_br", "_fr"))
paires["rapport_br_fr"] = paires["mots_br"] / paires["mots_fr"]
print(f"{len(paires)} paires : {paires['mots_br'].sum()} mots en breton, "
      f"{paires['mots_fr'].sum()} en français")
print(f"L'article breton fait en médiane "
      f"{paires['rapport_br_fr'].median():.0%} de l'article français")
print("Paires où le breton est plus long :",
      (paires["rapport_br_fr"] > 1).sum(), "\n")

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(paires["mots_fr"], paires["mots_br"], s=12, alpha=0.6)
borne = max(paires["mots_fr"].max(), paires["mots_br"].max())
ax.plot([10, borne], [10, borne], linestyle="--", linewidth=1, color="grey")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("mots, version française"); ax.set_ylabel("mots, version bretonne")
ax.set_title("Mêmes articles, deux langues (diagonale : même longueur)")
fig.tight_layout()
fig.savefig(SORTIE / "comparaison_paires.png", dpi=150)


# %% 8. Avoir un équivalent n'est pas être dans l'autre corpus
# Les versions françaises des paires sont-elles dans le corpus français ?
# On compare les titres exacts, pris dans les fichiers de métadonnées.
meta_paires = pd.read_csv(PAIRES["fr"].with_name(PAIRES["fr"].stem + "_metadonnees.csv"))
titres_fr = set(articles.query("langue == 'fr'")["titre"])
meta_paires["dans_corpus_fr"] = meta_paires["titre"].isin(titres_fr)
n_dedans = int(meta_paires["dans_corpus_fr"].sum())
print(f"Versions françaises des paires présentes dans le corpus français : "
      f"{n_dedans} sur {len(meta_paires)}")
absentes = sorted(meta_paires.loc[~meta_paires["dans_corpus_fr"], "titre"])
print("Exemples d'absentes :", " ; ".join(absentes[:10]), "\n")


# %% 9. Écrire la synthèse en Markdown
with open(SORTIE / "comparaison_synthese.md", "w", encoding="utf-8") as f:
    f.write("# Synthèse de la comparaison\n\n## Taille des corpus\n\n")
    f.write(taille.to_markdown() + "\n\n## Équivalents dans l'autre langue\n\n")
    f.write(equiv.to_markdown() + "\n\n## Articles par terme de recherche\n\n")
    f.write(termes.to_markdown(index=False) + "\n\n## Longueur selon *equiv_\n\n")
    f.write(longueur.to_markdown() + "\n\n## Paires fr/br\n\n")
    f.write(f"- {len(paires)} paires : {paires['mots_br'].sum()} mots en breton, "
            f"{paires['mots_fr'].sum()} en français\n- rapport médian br/fr : "
            f"{paires['rapport_br_fr'].median():.2f}\n"
            f"- paires où l'article breton est plus long : "
            f"{(paires['rapport_br_fr'] > 1).sum()}\n"
            f"- versions françaises présentes dans le corpus français : "
            f"{n_dedans} sur {len(meta_paires)}\n")
    f.write("\n## Versions françaises des paires absentes du corpus français\n\n")
    f.write(" ; ".join(absentes) + "\n")
    if (pbr_non := articles.query("langue == 'br' and equivalent == 'non'")).shape[0]:
        f.write("\n## Articles bretons sans équivalent français\n\n")
        for _, a in pbr_non.sort_values("mots", ascending=False).iterrows():
            f.write(f"- {a['titre']} ({a['mots']} mots)\n")
print("Résultats écrits dans", SORTIE)
