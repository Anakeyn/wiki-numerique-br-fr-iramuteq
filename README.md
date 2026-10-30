# wiki-numerique-br-fr-iramuteq

Le numérique vu par les Wikipédia bretonne et française : comparer deux corpus avec [IRaMuTeQ](https://pratinaud.gitpages.huma-num.fr/iramuteq-website/).

Ce dépôt accompagne l'article de blog du même nom. C'est le dernier d'une série : il réutilise les corpus constitués avec [wiki2iramuteq](https://github.com/Anakeyn/wiki2iramuteq) et le dictionnaire breton corrigé d'[Apertium2iramuteq-bretonV2](https://github.com/Anakeyn/Apertium2iramuteq-bretonV2).

## Sommaire

1. [Fichiers prêts à l'emploi](#1-fichiers-prêts-à-lemploi--aucune-commande-nécessaire)
2. [Nos choix](#2-nos-choix)
3. [Les scripts](#3-les-scripts)
4. [Reproduire les corpus et les résultats](#4-reproduire-les-corpus-et-les-résultats)
5. [Licences](#5-licences)

## 1. Fichiers prêts à l'emploi : aucune commande nécessaire

| Fichier | Contenu | Articles |
|---|---|---|
| `corpus/br/wikipedia_br_numerique_pret.txt` | Corpus breton, préparé pour le dictionnaire breton (UTF-8) | 156 |
| `corpus/br/wikipedia_br_numerique_pret_windows.txt` | Le même, en Windows-1252 | 156 |
| `corpus/fr/wikipedia_fr_numerique_nettoye.txt` | Corpus français nettoyé | 1 159 |
| `corpus/paires/wikipedia_br_paires_pret.txt` | Articles bretons qui ont un équivalent français, préparés | 137 |
| `corpus/paires/wikipedia_fr_aligne_sur_br_numerique_filtre.txt` | Leurs versions françaises (même `*id_`) | 137 |
| `resultats/comparaison_synthese.md` | Tableaux de comparaison des deux corpus | |
| `resultats/comparaison_longueurs.png`, `comparaison_paires.png` | Graphiques | |

Les corpus bretons non préparés (`*_filtre.txt`) et tous les fichiers de métadonnées (`*_metadonnees.csv` : titre, URL, révision, nombre de mots) sont aussi dans `corpus/`.

**Pour récupérer un fichier :** sur GitHub, cliquez sur le fichier, puis sur *Download raw file*. Vous pouvez aussi récupérer tout le dépôt avec **Code → Download ZIP**.

**Pour l'ouvrir dans IRaMuTeQ :** *Fichier → Ouvrir un corpus*.
- Corpus breton : installez d'abord le dictionnaire breton, comme expliqué dans [Apertium2iramuteq-bretonV2](https://github.com/Anakeyn/Apertium2iramuteq-bretonV2), puis choisissez la langue **breton**.
- Corpus français : encodage **utf-8**, langue **français**.

Chaque article porte la variable `*equiv_` : `*equiv_fr_oui/non` dans le corpus breton, `*equiv_br_oui/non` dans le corpus français. Elle indique si l'article existe aussi dans l'autre Wikipédia.

## 2. Nos choix

### Partir des corpus déjà constitués

Les corpus ont été extraits le 20 octobre 2026 avec wiki2iramuteq, en **mode recherche** : on garde les articles qui contiennent des termes du numérique, plutôt que ceux d'une catégorie. Les arbres de catégories des deux Wikipédia sont trop différents pour être comparés : la Wikipédia bretonne a peu de catégories, et l'équivalent breton d'une catégorie française est souvent absent ou presque vide.

| | Termes de recherche |
|---|---|
| Breton | stlenneg, urzhiataer, kenrouedad, genrouedad, niverel, meziant frank, meziantoù frank |
| Français | informatique, ordinateur, internet, numérique, logiciel libre |

En breton, il faut donner les formes mutées (`kenrouedad`, `genrouedad`), car la recherche ne gère pas les mutations.

### Deux analyses séparées, plus les paires

Les deux corpus n'ont ni le même lexique ni le même dictionnaire. Une classification de Reinert sur un corpus commun séparerait donc surtout les langues, pas les thèmes. On fait plutôt trois analyses :

1. le corpus breton, croisé avec `*equiv_fr` ;
2. le corpus français, croisé avec `*equiv_br` ;
3. les 137 paires : les mêmes articles dans les deux langues, pour voir comment chaque Wikipédia traite les mêmes sujets.

### Garder les articles sans équivalent

On ne retire pas les articles bretons qui n'ont pas d'équivalent français : ils montrent ce qui n'intéresse que la Wikipédia bretonne. La variable `*equiv_fr_non` permet de les repérer dans IRaMuTeQ. Il n'y en a que 18 sur 156 (Treiñ e brezhoneg, Raktres Translate (brezhoneg), Genver 2006 e Breizh…).

### Préparer le corpus breton

IRaMuTeQ coupe les mots à l'apostrophe : « c'hoari » deviendrait « c » + « hoari ». Le script `preparer_corpus_breton.py` réécrit donc le trigramme en `c_h`, comme dans le dictionnaire, sépare les mots à trait d'union et soude les expressions (« en doa » → `en_doa`). On utilise la version 2 du dictionnaire, corrigée après le premier essai sur le corpus de test.

### Nettoyer le corpus français : pourquoi pas un seuil plus fort

Le corpus breton filtré compte 156 articles et 108 000 mots ; le corpus français filtré de wiki2iramuteq, 1 232 articles et 2,5 millions de mots. On a d'abord pensé à relever le seuil de densité (occurrences des termes de recherche pour 1 000 mots) :

| Densité minimale | Articles | Mots | Dont `*equiv_br_oui` |
|---|---|---|---|
| 2 ‰ (filtre de wiki2iramuteq) | 1 213 + 19 gardés à la main | 2,44 M | 113 |
| 5 ‰ | 1 015 | 1,59 M | 66 |
| 10 ‰ | 746 | 0,89 M | 18 |

Un seuil plus fort écarte des articles qui sont au cœur du sujet : Intelligence artificielle (3,1 ‰), ChatGPT, Apprentissage automatique, Jeu vidéo, Blockchain, Algorithme, Base de données, Linux (7,3 ‰)… La densité mesure la fréquence de nos cinq termes de recherche, pas l'appartenance au sujet. Un article sur l'IA parle d'IA, rarement d'« informatique » ou d'« ordinateur », et un article long a mécaniquement une densité plus faible.

On a donc gardé le seuil de 2 ‰ et **exclu 73 articles à la main**, comme on l'avait fait pour le breton. Ils relèvent de trois cas :

- **des pages d'homonymie** : AO, CG, Digital, Apple (homonymie)… ;
- **« numérique » au sens des nombres** : Analyse numérique, Fonction numérique, Stabilité numérique, Numération mésopotamienne, et même Infériorité numérique, au sens sportif. C'est la principale source de bruit du terme de recherche « numérique » ;
- **des articles hors sujet** qui ne citent le numérique qu'en passant : des médias (L'Équipe, Groupe TF1…), des musiciens, Photographie, Télévision, Pastafarisme…

On a en revanche gardé les articles qui parlent de la place du numérique dans la culture ou dans des disciplines voisines : des films et chansons sur l'ordinateur, Têtes à claques, Droit d'auteur, Chimie numérique… et *La grande question sur la vie, l'Univers et le reste*.

Les listes complètes figurent dans `corpus/fr/exclure.txt` et `corpus/fr/garder.txt` (et `corpus/br/` pour le breton). Le résultat compte 1 159 articles et 2,34 millions de mots. Le corpus reste gros : on gagne en pertinence, pas en légèreté.

### Corriger deux identifiants en double

wiki2iramuteq construit `*id_` à partir du titre, en retirant les caractères spéciaux et en coupant à 50 caractères. Deux titres peuvent alors donner le même identifiant :
- « Internet » et « Internet+ » donnent tous deux `*id_Internet` ;
- « Technologies de l'information et de la communication » et « … pour l'enseignement » sont coupés au même endroit.

Le script `corriger_identifiants.py` ajoute `_2` au second : `*id_Internet_2` et `*id_Technologies_de_l_information_et_de_la_communicati_2`.

## 3. Les scripts

Tous les scripts utilisés sont dans le dépôt, pour qu'il se suffise à lui-même.

| Script | Origine | Rôle |
|---|---|---|
| `wiki2iramuteq.py` | [wiki2iramuteq](https://github.com/Anakeyn/wiki2iramuteq) | Extrait les articles de Wikipédia au format IRaMuTeQ |
| `filtrer_corpus.py` | wiki2iramuteq, avec un ajout | Refiltre un corpus sans rien retélécharger. Ajout : `--exclure @fichier.txt` lit la liste dans un fichier, un titre par ligne |
| `corriger_identifiants.py` | Ce dépôt | Rend les `*id_` uniques |
| `preparer_corpus_breton.py` | [Apertium2iramuteq-bretonV2](https://github.com/Anakeyn/Apertium2iramuteq-bretonV2) | Prépare un texte breton pour le dictionnaire IRaMuTeQ ; utilise `dictionnaire/expression_br.txt` |
| `comparer_corpus.py` | Ce dépôt | Compare les deux corpus et écrit `resultats/` |

`wiki2iramuteq.py`, `filtrer_corpus.py`, `corriger_identifiants.py` et `preparer_corpus_breton.py` n'utilisent que la bibliothèque standard de Python. `comparer_corpus.py` a besoin de `pandas`, `matplotlib` et `tabulate` :

```bash
pip install -r requirements.txt
```

## 4. Reproduire les corpus et les résultats

Il faut Python 3.8 ou plus récent. Téléchargez le dépôt (**Code → Download ZIP**), décompressez-le, puis ouvrez un terminal dans ce dossier.

Les commandes ci-dessous sont écrites pour Linux et macOS. **Sous Windows**, remplacez `python3` par `python`, écrivez chaque commande sur une seule ligne (sans les `\`) et remplacez `cp` par `copy`, avec des `\` au lieu des `/` dans les chemins de `copy`.

Wikipédia évolue : un nouveau tirage (étapes 1, 2 et 5) donnera des résultats proches, mais pas identiques, et certains titres des listes d'exclusion pourront avoir disparu. Pour repartir exactement des mêmes textes, sautez ces étapes et prenez les corpus bruts dans `corpus/num_br` et `corpus/num_fr` du dépôt [wiki2iramuteq](https://github.com/Anakeyn/wiki2iramuteq/tree/main/corpus), à copier dans `brut/`.

Remplacez `votre@courriel` par votre adresse ou votre site : Wikimédia demande ce contact pour ne pas bloquer les requêtes.

**Étape 1 : extraire le corpus breton**, avec la variable `*equiv_fr_oui/non`

```bash
python3 wiki2iramuteq.py --lang br \
    --recherche "stlenneg,urzhiataer,kenrouedad,genrouedad,niverel,meziant frank,meziantoù frank" \
    --marquer fr --nom numerique --contact "votre@courriel" --sortie ./brut/num_br
```

**Étape 2 : extraire le corpus français**, avec la variable `*equiv_br_oui/non`

```bash
python3 wiki2iramuteq.py --lang fr \
    --recherche "informatique,ordinateur,internet,numérique,logiciel libre" \
    --marquer br --plafond 500 --min-occurrences 5 --nom numerique \
    --contact "votre@courriel" --sortie ./brut/num_fr
```

**Étape 3 : filtrer le corpus breton** (156 articles sur 190)

```bash
python3 filtrer_corpus.py brut/num_br/wikipedia_br_numerique_metadonnees.csv --min-densite 2 \
    --exclure @corpus/br/exclure.txt --garder @corpus/br/garder.txt
cp brut/num_br/wikipedia_br_numerique_filtre* corpus/br/
```

**Étape 4 : nettoyer le corpus français** (1 159 articles sur 1 266), puis corriger les identifiants

```bash
python3 filtrer_corpus.py brut/num_fr/wikipedia_fr_numerique_metadonnees.csv --min-densite 2 \
    --exclure @corpus/fr/exclure.txt --garder @corpus/fr/garder.txt
python3 corriger_identifiants.py brut/num_fr/wikipedia_fr_numerique_filtre.txt
cp brut/num_fr/wikipedia_fr_numerique_filtre.txt corpus/fr/wikipedia_fr_numerique_nettoye.txt
cp brut/num_fr/wikipedia_fr_numerique_filtre_metadonnees.csv corpus/fr/wikipedia_fr_numerique_nettoye_metadonnees.csv
cp brut/num_fr/wikipedia_fr_numerique_filtre_criteres.txt corpus/fr/wikipedia_fr_numerique_nettoye_criteres.txt
```

**Étape 5 : constituer les paires**, en récupérant la version française des articles bretons retenus

```bash
python3 wiki2iramuteq.py --lang fr \
    --aligner ./corpus/br/wikipedia_br_numerique_filtre_metadonnees.csv \
    --recherche "informatique,ordinateur,internet,numérique,logiciel libre" \
    --contact "votre@courriel" --sortie ./corpus/paires
```

**Étape 6 : préparer les textes bretons** pour le dictionnaire

```bash
python3 preparer_corpus_breton.py corpus/br/wikipedia_br_numerique_filtre.txt \
    -o corpus/br/wikipedia_br_numerique_pret.txt
python3 preparer_corpus_breton.py corpus/br/wikipedia_br_numerique_filtre.txt \
    -o corpus/br/wikipedia_br_numerique_pret_windows.txt --windows
python3 preparer_corpus_breton.py corpus/paires/wikipedia_br_numerique_filtre_aligne_sur_fr.txt \
    -o corpus/paires/wikipedia_br_paires_pret.txt
```

**Étape 7 : comparer les deux corpus**

```bash
python3 comparer_corpus.py
```

Le script suit sept étapes, repérées par des blocs `# %%` dans le code : lecture des corpus, taille, part des articles qui ont un équivalent, articles par terme de recherche, longueurs selon `*equiv_`, comparaison des 137 paires, écriture de la synthèse. Les résultats vont dans `resultats/`.

## 5. Licences

Code sous licence GNU GPL v3 (voir `LICENSE`). Textes des corpus issus de Wikipédia, sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr) ; la liste des articles et leurs révisions figurent dans les fichiers `*_metadonnees.csv`. Le fichier `dictionnaire/expression_br.txt` est dérivé d'`apertium-bre`, le module breton d'[Apertium](https://www.apertium.org/), distribué sous licence GNU GPL v3.
