# wiki-numerique-br-fr-iramuteq

Le numérique vu par les Wikipédia bretonne et française : comparer deux corpus avec [IRaMuTeQ](https://pratinaud.gitpages.huma-num.fr/iramuteq-website/).

Ce dépôt accompagne l'article de blog du même nom. Il réutilise les corpus constitués avec [wiki2iramuteq](https://github.com/Anakeyn/wiki2iramuteq) le 20 octobre 2026 et le dictionnaire breton corrigé d'[Apertium2iramuteq-bretonV2](https://github.com/Anakeyn/Apertium2iramuteq-bretonV2).

## 1. Fichiers prêts à l'emploi : aucune commande nécessaire

| Fichier | Contenu | Articles |
|---|---|---|
| `corpus/br/wikipedia_br_numerique_pret.txt` | Corpus breton préparé pour le dictionnaire breton (UTF-8) | 156 |
| `corpus/br/wikipedia_br_numerique_pret_windows.txt` | Le même, en Windows-1252 | 156 |
| `corpus/fr/wikipedia_fr_numerique_filtre.txt` | Corpus français | 1 232 |
| `corpus/paires/wikipedia_br_paires_pret.txt` | Articles bretons qui ont un équivalent français, préparés | 137 |
| `corpus/paires/wikipedia_fr_aligne_sur_br_numerique_filtre.txt` | Leurs versions françaises (même `*id_`) | 137 |
| `resultats/comparaison_synthese.md` | Tableaux de comparaison des deux corpus | |
| `resultats/comparaison_longueurs.png`, `comparaison_paires.png` | Graphiques | |

**Pour récupérer un fichier :** sur GitHub, cliquez sur le fichier, puis sur *Download raw file*. Vous pouvez aussi récupérer tout le dépôt avec **Code → Download ZIP**.

**Pour l'ouvrir dans IRaMuTeQ :** *Fichier → Ouvrir un corpus*. Corpus breton : dictionnaire breton installé, langue **breton**. Corpus français : encodage **utf-8**, langue **français**.

Chaque article porte la variable `*equiv_` : `*equiv_fr_oui/non` dans le corpus breton, `*equiv_br_oui/non` dans le corpus français. Elle indique si l'article existe dans l'autre Wikipédia.

## 2. Ce que fait `comparer_corpus.py`

1. Il lit les deux corpus et compte les mots de chaque article.
2. Il compare la taille des corpus.
3. Il mesure la part des articles qui ont un équivalent dans l'autre langue.
4. Il compte les articles ramenés par chaque terme de recherche.
5. Il compare les longueurs selon la langue et `*equiv_`.
6. Il compare la longueur des mêmes articles dans les deux langues (137 paires).
7. Il écrit la synthèse et les graphiques dans `resultats/`.

## 3. Utiliser le script

Il faut Python 3.8 ou plus récent et trois bibliothèques :

```bash
pip install -r requirements.txt
python3 comparer_corpus.py
```

Sous Windows, remplacez `python3` par `python`.

## 4. Licences

Code sous licence GNU GPL v3 (voir `LICENSE`). Textes des corpus issus de Wikipédia, sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr) ; la liste des articles et leurs révisions figurent dans les fichiers `*_metadonnees.csv`.
