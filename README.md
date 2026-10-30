# wiki-numerique-br-fr-iramuteq

Le numérique vu par les Wikipédia bretonne et française : comparer deux corpus avec [IRaMuTeQ](https://pratinaud.gitpages.huma-num.fr/iramuteq-website/).

Ce dépôt accompagne l'article de blog du même nom. C'est le dernier d'une série : il réutilise les corpus constitués avec [wiki2iramuteq](https://github.com/Anakeyn/wiki2iramuteq) et le dictionnaire breton d'[Apertium2iramuteq-bretonV3](https://github.com/Anakeyn/Apertium2iramuteq-bretonV3), dont la version 3 corrige des erreurs révélées par ce corpus.

## Sommaire

1. [Fichiers prêts à l'emploi](#1-fichiers-prêts-à-lemploi--aucune-commande-nécessaire)
2. [Nos choix](#2-nos-choix)
3. [Les scripts](#3-les-scripts)
4. [Reproduire les corpus et les résultats](#4-reproduire-les-corpus-et-les-résultats)
5. [Licences](#5-licences)

## 1. Fichiers prêts à l'emploi : aucune commande nécessaire

| Fichier | Contenu | Articles |
|---|---|---|
| `corpus/br/wikipedia_br_numerique_pret.txt` | **Analyse 1** : corpus breton, préparé pour le dictionnaire breton (UTF-8) | 123 |
| `corpus/br/wikipedia_br_numerique_pret_windows.txt` | Le même, en Windows-1252 | 123 |
| `corpus/paires/wikipedia_fr_aligne_sur_br_numerique_filtre.txt` | **Analyse 2** : versions françaises des articles bretons qui ont un équivalent (même `*id_`) | 109 |
| `corpus/paires/wikipedia_br_paires_pret.txt` | Les 109 articles bretons correspondants, préparés | 109 |
| `corpus/fr/wikipedia_fr_numerique_nettoye.txt` | Contexte : échantillon de la Wikipédia française sur le numérique, issu de sa propre recherche | 1 159 |
| `dictionnaire/lexique_br.txt` | Dictionnaire breton pour IRaMuTeQ (version 3), à désigner à l'ouverture du corpus breton | |
| `resultats/comparaison_synthese.md` | Tableaux de comparaison des deux corpus | |
| `resultats/comparaison_longueurs.png`, `comparaison_paires.png` | Graphiques | |

Les corpus bretons non préparés (`*_filtre.txt`) et tous les fichiers de métadonnées (`*_metadonnees.csv` : titre, URL, révision, nombre de mots) sont aussi dans `corpus/`.

**Pour récupérer un fichier :** sur GitHub, cliquez sur le fichier, puis sur *Download raw file*. Vous pouvez aussi récupérer tout le dépôt avec **Code → Download ZIP**.

**Pour l'ouvrir dans IRaMuTeQ :** *Fichier → Ouvrir un corpus*.
- Corpus breton : encodage **utf-8** (ou **cp1252** pour la version Windows), langue **autre**, dictionnaire **Autre** en désignant `dictionnaire/lexique_br.txt` (copie de la version 3 d'[Apertium2iramuteq-bretonV3](https://github.com/Anakeyn/Apertium2iramuteq-bretonV3)), et décochez **Utiliser le dictionnaire des expressions** : les expressions sont déjà soudées. Si votre version d'IRaMuTeQ ne propose pas le dictionnaire « Autre », suivez la méthode B du dépôt du dictionnaire. Dans la description du corpus, vérifiez le chemin du lexique et que la ligne des expressions indique 0.
- Corpus français : encodage **utf-8**, langue **français**.

Dans le corpus breton, la variable `*equiv_fr_oui/non` indique si l'article existe aussi dans la Wikipédia française ; dans le corpus français de contexte, `*equiv_br_oui/non` indique l'inverse. Les versions françaises des paires n'en ont pas besoin : elles ont toutes un équivalent breton, et partagent son `*id_`.

## 2. Nos choix

### Partir des corpus déjà constitués

Les corpus ont été extraits le 20 octobre 2026 avec wiki2iramuteq, en **mode recherche** : on garde les articles qui contiennent des termes du numérique, plutôt que ceux d'une catégorie. Les arbres de catégories des deux Wikipédia sont trop différents pour être comparés : la Wikipédia bretonne a peu de catégories, et l'équivalent breton d'une catégorie française est souvent absent ou presque vide.

| | Termes de recherche |
|---|---|
| Breton | stlenneg, urzhiataer, kenrouedad, genrouedad, niverel, meziant frank, meziantoù frank |
| Français | informatique, ordinateur, internet, numérique, logiciel libre |

En breton, il faut donner les formes mutées (`kenrouedad`, `genrouedad`), car la recherche ne gère pas les mutations.

### Partir du breton, puis prendre les articles français correspondants

Pour comparer les mêmes sujets, le périmètre est défini une seule fois, par la recherche en breton. On récupère ensuite la version française de chaque article breton retenu, avec le mode alignement de wiki2iramuteq (étape 5). Les deux langues ont des lexiques et des dictionnaires différents : une classification de Reinert sur un corpus commun séparerait surtout les langues, pas les thèmes. On fait donc deux analyses séparées, que l'on compare ensuite :

1. **le corpus breton** (123 articles), croisé avec `*equiv_fr` : de quoi parle la Wikipédia bretonne, et ce qu'elle est seule à traiter ;
2. **les versions françaises des 109 articles qui ont un équivalent** : comment la Wikipédia française traite les mêmes sujets.

Le corpus breton des paires est le corpus 1 sans ses 14 articles sans équivalent : une analyse à part n'apporterait presque rien. Il est fourni pour qui voudrait comparer exactement les mêmes articles.

Ce choix a un prix : le périmètre est celui des contributeurs bretons. On ne voit pas, dans les classifications, ce qui intéresse la Wikipédia française et que la bretonne n'a pas. Pour donner cet ordre de grandeur, on garde un corpus français issu de sa propre recherche, utilisé seulement pour les statistiques descriptives de `comparer_corpus.py` (voir plus bas pourquoi il n'est qu'un échantillon).

### Garder les articles sans équivalent

On ne retire pas les articles bretons qui n'ont pas d'équivalent français : ils montrent ce qui n'intéresse que la Wikipédia bretonne. La variable `*equiv_fr_non` permet de les repérer dans IRaMuTeQ. Il n'y en a que 14 sur 123 (Treiñ e brezhoneg, Raktres Translate (brezhoneg), Skoroù treuzkas, OSI…).

### Préparer le corpus breton

IRaMuTeQ coupe les mots à l'apostrophe : « c'hoari » deviendrait « c » + « hoari ». Le script `preparer_corpus_breton.py` réécrit donc le trigramme en `c_h`, comme dans le dictionnaire, soude les mots-outils à trait d'union (« e-barzh » → `e_barzh`), sépare les autres mots à trait d'union et soude les expressions (« en doa » → `en_doa`).

### Corriger le dictionnaire avant la classification : la version 3

On a d'abord préparé le corpus avec la version 2 du dictionnaire. Les statistiques textuelles d'IRaMuTeQ ont alors montré, parmi les formes actives les plus fréquentes, des lemmes absurdes pour un corpus sur le numérique : *unaniñ* (unir, 159 occurrences), *kell* (cellule, 135), *barzh* (poète, 127), *touiñ* (jurer, 62). Ils venaient de *unan* (« un »), *c'hell* (« peut »), *e-barzh* (« dedans », coupé au tiret) et *e-touez* (« parmi »). Ces formes auraient pesé sur la classification de Reinert.

On les a corrigées dans une version 3 du dictionnaire, [Apertium2iramuteq-bretonV3](https://github.com/Anakeyn/Apertium2iramuteq-bretonV3), qui détaille les corrections. La version 2 reste conforme à son article. Le corpus breton de ce dépôt est préparé avec la version 3 : 1 721 occurrences changent de lecture ; *ober* passe de 563 à 739 occurrences et *gallout* de 346 à 480.

### Nettoyer le corpus français de contexte : pourquoi pas un seuil plus fort

Avant l'harmonisation décrite plus bas, le corpus breton filtré comptait 156 articles et 108 000 mots ; le corpus français filtré de wiki2iramuteq, 1 232 articles et 2,5 millions de mots. On a d'abord pensé à relever le seuil de densité (occurrences des termes de recherche pour 1 000 mots) :

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

### Appliquer les mêmes règles aux deux corpus

Les exclusions manuelles doivent suivre la même règle dans les deux langues. Côté français, on avait écarté *Photographie*, *Télévision*, *Film (cinéma)*, *Dessin animé*, *Cartographie*, *ISBN* ou *Maison d'édition* : le numérique y a sa section, mais ce n'est pas le sujet de l'article. Le premier filtrage breton gardait pourtant leurs équivalents. On a donc repris le corpus breton avec la règle française : **on écarte un article quand son sujet n'est pas le numérique, même s'il lui consacre une section.** Cela fait 33 articles de plus :

- **les mêmes sujets qu'en français** : Luc'hskeudennerezh et Arz al luc'hskeudennerezh (photographie), Skinwel et TV Breizh (télévision), Sinema, Tresadennoù-bev et Bliverezh (animation), Kartennouriezh et Bannerezh-kartenn (cartographie), ISBN, Embannerezh (édition), Holloueziadur (encyclopédie) et Kazetennerezh (journalisme) ;
- **« niverel » au sens des nombres** : Lizherenneg hengirillek, où les lettres servent aussi de chiffres ;
- **des articles qui ne citent le numérique qu'en passant** : les siècles et décennies (Eil milved, IIIe milved, XXvet kantved, Bloavezhioù 2000), les chroniques Genver et Meurzh 2006 e Breizh, la Deiziataer ijinadennoù Mab-den, les préfixes du SI (Kilo-, Mega, Giga, Tera, Rakgerioù unanennoù an SI) et le Hertz, le Go (c'hoari), des langues et la linguistique (Islandeg, Yezhoniezh, Nevezc'her), Joseph Loth et Skiantoù an Ditour hag al Levraouegoù.

Holloueziadur et Kazetennerezh étaient gardés à la main malgré une densité inférieure à 2 ‰ : on les a retirés de `corpus/br/garder.txt`. Les autres sont dans `corpus/br/exclure.txt`. Le corpus breton passe de 156 à 123 articles et de 108 000 à 78 000 mots ; 14 articles n'ont pas d'équivalent français, au lieu de 18.

On garde en revanche, comme en français, ce qui parle de la place du numérique dans la culture : Terminator (robotoù), Skynet, Battlestar Galactica, La Chanson du Dimanche, Scopitone, Matte painting… et l'Agence Bretagne Presse, agence de presse née sur le Web.

Effet de bord : Tresadennoù-bev et Bliverezh renvoyaient tous deux à l'article français *Animation (audiovisuel)*. wiki2iramuteq n'écrit qu'une fois un même article cible : on avait 138 articles `*equiv_fr_oui` pour 137 paires. Les deux étant écartés, on a maintenant 109 `*equiv_fr_oui` et 109 paires.

### Avoir un équivalent n'est pas être dans l'autre corpus

`*equiv_` dit si l'article existe dans l'autre Wikipédia, pas s'il est dans l'autre corpus. Sur les 109 paires, seules 50 versions françaises figurent dans le corpus français. Les 59 autres n'ont pas été retenues : 54 n'ont jamais été ramenées par la recherche (Unix, Bitcoin, Facebook, Compilateur, Tim Berners-Lee…) et 5 ont été ramenées mais écartées par le seuil d'occurrences ou de densité (Transmission Control Protocol, Prix Turing…).

Les deux extractions n'ont en effet pas les mêmes réglages. En breton, la recherche ramène sans doute presque tout ce qui contient les termes (plafond de 2 000 résultats par terme, 2 occurrences minimum). En français, on a limité la recherche à 500 résultats par terme et 5 occurrences minimum, sinon le corpus aurait été énorme. Le corpus breton est donc presque exhaustif, le corpus français est un échantillon : les 500 articles que le moteur de recherche de Wikipédia juge les plus pertinents pour chaque terme.

C'est la raison principale pour laquelle on ne classe pas ce corpus français et que l'on part du breton : comparer un corpus presque exhaustif à un échantillon mesurerait autant la recherche que les Wikipédia. On s'en sert seulement pour des ordres de grandeur, à lire avec cette réserve.

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
| `preparer_corpus_breton.py` | [Apertium2iramuteq-bretonV3](https://github.com/Anakeyn/Apertium2iramuteq-bretonV3) | Prépare un texte breton pour le dictionnaire IRaMuTeQ ; utilise `dictionnaire/expression_br.txt` |
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

**Étape 3 : filtrer le corpus breton** (123 articles sur 190)

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

**Étape 5 : constituer les paires**, en récupérant la version française des articles bretons retenus (109 paires)

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

Le script est découpé en neuf blocs `# %%` : chemins et bibliothèques, lecture des corpus, taille, part des articles qui ont un équivalent, articles par terme de recherche, longueurs selon `*equiv_`, comparaison des 109 paires, présence des paires dans le corpus français, écriture de la synthèse. Les résultats vont dans `resultats/`.

## 5. Licences

Code sous licence GNU GPL v3 (voir `LICENSE`). Textes des corpus issus de Wikipédia, sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr) ; la liste des articles et leurs révisions figurent dans les fichiers `*_metadonnees.csv`. Les fichiers `dictionnaire/lexique_br.txt` et `dictionnaire/expression_br.txt`, copiés d'Apertium2iramuteq-bretonV3, sont dérivés d'`apertium-bre`, le module breton d'[Apertium](https://www.apertium.org/), distribué sous licence GNU GPL v3.
