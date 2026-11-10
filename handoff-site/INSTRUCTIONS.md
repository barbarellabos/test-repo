# Jacqueline's Lab : instructions pour coder les pages produits, le panier et le menu

Instructions pour un agent de code (Claude Code). Elles ont été rédigées le 10 nov. 2026 à partir des maquettes validées par Dora (co-fondatrice), dans le canvas Claude Design « Page produit Mobilité — maquettes mobile ».

**Ce document remplace `handoff-page-produit-mobilite/INSTRUCTIONS.md`**, qui est devenu obsolète (ordre des blocs, quiz, prix). Le menu garde ses propres instructions, `handoff-menu-mobile/INSTRUCTIONS-menu.md`, toujours valables. La section 8 résume ce qui a changé depuis.

---

## 0. À lire avant tout

### Contexte
Jacqueline's Lab vend 3 compléments en soft chews pour chiens : **Mobilité**, **Multivitamines** et **Digestion**. Chaque sachet contient 60 soft chews (180 g). Le trafic vient surtout des pubs Meta sur téléphone : on code **mobile d'abord**.

### Comment travailler avec Dora
- Tutoie-la, en français.
- Challenge ses demandes quand c'est illogique, incomplet ou faux.
- Confirme ta compréhension en 3 à 5 lignes avant tout gros chantier.
- Signale en fin de réponse les idées que tu as écartées.
- Le site, lui, **vouvoie** le client (section 2).

### Contenu du dossier

| Chemin | Contenu |
|---|---|
| `maquettes/page-mobilite.dc.html` | Page produit Mobilité, **la référence du gabarit** |
| `maquettes/page-multivitamines.dc.html` | Page produit Multivitamines |
| `maquettes/page-digestion.dc.html` | Page produit Digestion |
| `maquettes/bulle-achat-ouverte.dc.html` | État du bloc d'achat après un clic |
| `maquettes/comparaison-ouverte.dc.html` | État de la section « Mobilité ou Multivitamines ? » dépliée |
| `maquettes/panier-1-sachet.dc.html`, `panier-3e-offert.dc.html` | Le panier, dans ses 2 états |
| `maquettes/menu-mobile.dc.html` | Le menu (instructions dans `handoff-menu-mobile/`) |
| `assets/` | Toutes les images, rangées par usage (section 7) |

Les `.dc.html` sont du HTML avec styles en ligne, variables `{{ x }}`, `<sc-if>` / `<sc-for>` et une classe JS `Component`. **Ce n'est pas du code à copier tel quel** : c'est la référence des textes, de l'ordre, des couleurs, des tailles et des comportements. Ouvre-les et lis-les en entier, y compris le script en bas, qui décrit les comportements (ouverture des bulles, calculs).

### Règles de sécurité
- Travaille sur une **copie du thème**, jamais sur le thème en ligne. Envoie le lien d'aperçu à Dora.
- Ne modifie ni les produits, ni les prix, ni les apps de la boutique sans son accord.
- **Étape 0 obligatoire :** vérifie la plateforme (a priori Shopify), le thème, l'app d'abonnement et ton accès au code. Si quelque chose bloque, arrête-toi et demande.

---

## 1. Les 5 règles que Dora a fixées (non négociables)

### 1.1 La collecte des données ne change pas
Le bloc d'achat demande **le poids du chien** et **le prénom du chien**. Ces données servent ensuite aux e-mails. **Tu as déjà en place la méthode pour les récupérer, les enregistrer et les classer : réutilise exactement la même**, sur les 3 pages produits. Ne crée pas de nouveau champ, de nouvelle propriété, de nouveau metafield ni de nouvelle intégration. Les noms de champs, le format et la destination (commande, client, outil d'e-mail) restent identiques à l'existant. En cas de doute sur le fonctionnement actuel, demande à Dora avant de toucher quoi que ce soit.

### 1.2 Le bloc d'achat : une seule bulle ouverte à la fois
- **Au chargement :** les 2 bulles « Abonnement » et « Achat unique » sont **fermées** et rien n'est présélectionné, ni l'option ni le poids.
- **Clic sur « Abonnement »** → sa bulle se déroule.
- **Clic sur « Achat unique »** → sa bulle se déroule **et celle de l'abonnement se referme**. Et inversement.
- **Jamais les deux ouvertes en même temps.**
- **La bulle ouverte contient :**
  1. « 1 · Poids de votre chien » : 3 boutons (1–10 kg, 11–30 kg, + de 30 kg), aucun présélectionné. Avant le choix, la ligne d'info dit « Choisissez son poids : nous calculons sa dose. » Après le choix : dose par jour, durée du sachet et prix par jour.
  2. « 2 · Le prénom de votre chien » : champ texte, exemple « Ex. Nestor ».
  3. Le bouton d'achat : **grisé** avec « Choisissez son poids » tant qu'aucun poids n'est choisi, puis cobalt avec « Acheter · [prix] ».
  4. En dessous : « Cure de 3 mois recommandée, idéalement en continu. », « Satisfait ou remboursé », et la ligne de livraison.
- **Le poids ne change pas le produit :** c'est le même sachet pour toutes les tranches. Il sert à la dose, au prix par jour et aux données (règle 1.1).
- **Accessibilité :** les 2 bulles forment un groupe de boutons radio ; la bulle ouverte porte `aria-expanded="true"` ; le prénom a un vrai `<label>` ; tout est utilisable au clavier.
- Référence : `maquettes/bulle-achat-ouverte.dc.html`.

### 1.3 Les prix et les offres ne sont pas définitifs
**Tous les prix, pourcentages et offres des maquettes sont indicatifs** :
- 38,40 €, 26,11 €, 30,72 €, 35,90 €, 37,70 € ;
- −15 %, −20 %, −32 % ;
- « Black Friday · 3e sachet offert dès 2 » ;
- « 3 sachets pour 76,10 € » ;
- les seuils de livraison.

Ce ne sont **ni les vrais prix ni les vraies offres**. Donc :
- **Aucun prix ni pourcentage écrit en dur.** Tout vient de Shopify : prix, prix barré, `selling_plan` de l'app d'abonnement, réductions automatiques.
- Les pourcentages et le prix par jour sont **calculés** à partir des vrais prix.
- **Les textes d'offre** (bandeau, jauge du panier, « Le 3e est offert ») et **les seuils de livraison** sont des **réglages de section modifiables** par Dora, avec un seul texte de livraison réutilisé partout.
- Le prix barré ne s'affiche que s'il existe (`compare_at_price` supérieur au prix).

### 1.4 Le quiz : reprendre le quiz existant
**Le quiz dessiné en bas des maquettes n'est pas le vrai.** Il n'indique que l'emplacement et le style de l'encadré.
- **Reprends le code du quiz déjà en place sur la page d'accueil du site** et intègre-le tel quel à cet emplacement, sur les 3 pages produits.
- Garde au-dessus le titre de la maquette : « PAS SÛR QUE CE SOIT LE BON CHOIX POUR VOTRE CHIEN ? »
- Ne réécris pas ses questions ni sa logique. Si son code ne peut pas être intégré directement, mets un bouton « Faire le quiz » qui y mène et préviens Dora.
- Le bouton « Faire le quiz » du menu mène au même quiz.

### 1.5 Les images manquantes
Ces 3 défilés **n'ont pas encore toutes leurs images**. Code-les pour accepter **un nombre variable d'images**, ajoutées par Dora depuis l'éditeur de thème (blocs de section), et n'affiche que celles qui existent :
1. **La galerie produit en haut de page** : seule la 1re photo existe pour chaque produit (section 7). Les points de pagination s'adaptent au nombre d'images.
2. **Le défilé des événements** (« Sur le terrain, chien après chien ») : chaque photo a une légende (nom, ville, date). Une seule photo est prête : `event-corgi.webp`, « Journée Corgi · Paris ».
3. **Le défilé des chiens qui mangent leurs soft chews** (« On en a marre de voir de l'IA. Voici nos vrais fans. ») : photos seules, sans légende. 3 sont prêtes (bouvier, dalmatien, épagneul).

**Aucun emplacement vide ni « Photo à shooter » ne doit apparaître en ligne.** Les cartes hachurées des maquettes sont des repères pour Dora.

---

## 2. Direction artistique (commune aux 3 pages)

**Couleurs de la marque :**
- crème `#FBF9F2` (fond), encre `#111`, cobalt `#2525DC` (titres, bouton d'achat, bandeau) ;
- gris texte `#3D3D3D` ;
- étoiles Trustpilot `#00B67A`.

**Couleur propre à chaque produit** (à mettre en variable, pas en dur) :

| Produit | Couleur | Fond pâle | Texte foncé |
|---|---|---|---|
| Mobilité | `#E8501A` | `#FBD9C7` | `#C4400F` |
| Multivitamines | `#F5D14E` | `#F9E7A8` | `#8A6A00` |
| Digestion | `#5DBB7A` | `#CFE7D6` | `#1C7F3D` |

**Pages produits, style néo-brutaliste :** bordures de 2,5 px en `#111`, arrondis de 14 à 18 px, ombre dure `4px 5px #111` (`5px 6px` pour le bouton d'achat), boutons en pilule.

**Panier et menu, style plus sobre :** traits de 1 à 1,5 px, pas d'ombre décalée, toujours sur le fond crème (section 5).

**Polices :**
- League Spartan 700/800/900 pour les titres en majuscules, prix et boutons ;
- Outfit pour le texte ;
- Permanent Marker uniquement pour les doses des actifs.

**Tailles, validées par Dora :**
- texte courant **18 px** ;
- petits textes et légendes **16 px minimum** ;
- champs de saisie 16 px minimum (sinon l'iPhone zoome) ;
- zones cliquables de 44 px minimum.

**Ton : vouvoiement partout** côté client (boutons, erreurs, panier, e-mails, quiz). Si une partie existante tutoie encore, signale-le à Dora.

**Maquettes dessinées à 390 px de large**, avec des marges latérales de 16 px.

**Défilés latéraux :**
- `scroll-snap-type: x mandatory` **avec `scroll-padding-left` égal à la marge gauche**, sinon la 1re carte colle au bord ;
- la carte suivante dépasse toujours à droite pour montrer qu'on peut faire défiler ;
- aucune bibliothèque de carrousel.

---

## 3. Le gabarit des pages produits, bloc par bloc

**Une seule template** (`templates/product.soft-chew.json` + sections `jl-*`) pour les 3 produits. Tout ce qui varie d'un produit à l'autre vient de **metafields** ou de **réglages de section** : textes, actifs, bienfaits, couleur, comparaison. Le tableau de la section 4 liste ces différences.

**Ordre exact des blocs** (c'est celui des maquettes, qui prime sur les commentaires `<!-- -->` dans les fichiers) :

1. **Bandeau** sur 1 ligne, fond cobalt. Texte modifiable (règle 1.3).
2. **En-tête :**
   - logo d'environ 85 px de haut ;
   - bascule FR/EN ;
   - panier avec le nombre d'articles ;
   - bouton menu (voir les instructions du menu).
3. **Photo principale :** 357 px de haut, `object-fit: cover`, cadrée sur la main, la tête du chien et les sachets, avec des points de pagination. C'est la 1re image d'une galerie à faire défiler (règle 1.5).
4. **Note :** étoiles Trustpilot + « 4,8/5 · Trustpilot », via le widget ou l'API Trustpilot, jamais en dur.
5. **Nom du produit** (42 px, cobalt), puis « CHOISISSEZ VOTRE FORMULE ».
6. **Bloc d'achat** : les 2 bulles, voir la règle 1.2.
   - Le badge « Recommandé » est sur l'abonnement.
   - Chaque bulle fermée affiche : bouton radio vide, nom de l'option, prix barré s'il existe, prix, une ligne de texte et la pastille de réduction calculée.
   - Textes des lignes : abonnement « Livraison offerte · sans engagement », achat unique « Sans engagement · pour tester d'abord ».
7. **« LES BIENFAITS CLEFS »** : icônes rondes + libellés en cobalt et majuscules (section 4).
8. *(Mobilité uniquement)* Encadré orange pâle : « On n'attend pas qu'il ralentisse : on renforce ses articulations dès qu'il est jeune. »
9. **Posologie :** carte blanche « 60 SOFT CHEWS par sachet, un RITUEL QUOTIDIEN : » + 3 pastilles : 1-10 kg · 1 / jour, 11-30 kg · 2 / jour, +30 kg · 3 / jour. **Même posologie pour les 3 produits.**
10. **« ILS L'ONT TESTÉ. »** : avis en défilé latéral (cartes de 290 px), vrais avis Trustpilot uniquement, + bouton « Lire tous les avis ».
11. **Bandeau jaune pâle** avec une phrase (section 4) + bouton cobalt « Choisir sa formule » qui remonte au bloc d'achat (ancre `#offre`).
12. **« LES 3 COMPLÉMENTS SE COMBINENT. »** (fond cobalt) : une carte par **autre** produit de la gamme. Chaque carte : photo, nom, phrase, **prix réel**, lien « Voir la fiche », et bouton rond « + » qui **ajoute au panier sans quitter la page** (AJAX `/cart/add.js` + mise à jour du compteur).
13. *(Mobilité et Multivitamines uniquement)* **Section comparative dépliable** (section 6).
14. **« ALLIE SCIENCE ET GOÛT. »** + « Formulé par des vétérinaires nutritionnistes » :
    - **bloc « GOÛT VIANDE »** (presque carré, environ 190 px de haut, couleur du produit) : photo `corgi-miam.webp` à gauche (environ 150 px de large), texte « Tendre, il le prend comme une friandise. » à droite ;
    - « SES N ACTIFS · DOSES PAR SOFT CHEW » puis **la liste verticale des actifs**. Chaque carte : rond image de 52 px, nom (couleur foncée du produit), rôle, référence éventuelle en italique, dose à droite en Permanent Marker. Les données viennent d'un metafield (section 4) ;
    - **Multivitamines :** les 5 premiers actifs sont visibles, puis un bouton « Voir les 17 actifs » / « Replier la liste » ;
    - pastille « Sans sucre ajouté · sans mauvais gras » ;
    - bouton « VOIR LA COMPOSITION INTÉGRALE », qui mène à la fiche complète de l'étiquette (obligation légale, section 9).
15. **« L'ALTERNATIVE À LA FRIANDISE. »** : photo `chew-main.webp` + tableau de 3 lignes « Friandise classique » contre [nom du produit] :
    - Gourmande / Gourmande ;
    - Rien d'utile en plus / [N] actifs dosés ;
    - À l'occasion / Chaque jour.

    Phrase dessous : « Vous lui donnez déjà une friandise ? Remplacez-la par son soft chew. »
16. **« SUR LE TERRAIN, CHIEN APRÈS CHIEN. »** + « Nous partons à la rencontre des chiens et de leurs maîtres, partout en France. » :
    - défilé de photos d'événements avec légende (règle 1.5) ;
    - encadré « 50+ événements en France · Observé en événement, pas un essai clinique. »
17. **Avis d'expert en vidéo :** « L'AVIS DE L'OSTÉOPATHE. » sur Mobilité, « L'AVIS DE L'EXPERT. » sur les deux autres. Vidéo, citation et nom sont **à fournir** : **masque la section tant qu'ils sont vides**.
18. **« SON RITUEL DE TOUS LES JOURS. »** : frise en 3 étapes.
    1. Jours 1 à 10 · La mise en route · Votre chien adopte son rituel.
    2. Dès 1 mois · La routine ancrée · Le geste devient automatique.
    3. 3 mois · Le bilan · Cure de 3 mois minimum, idéalement en continu.
19. **« VOS QUESTIONS. »** : FAQ en accordéon (`<details>` + balisage `FAQPage`) :
    - Combien par jour ?
    - Et si ça ne lui plaît pas ? (« Satisfait ou remboursé 60 jours, sans formulaire. »)
    - Livraison et retours (texte du réglage commun)
    - Comment marche l'abonnement ? (réduction calculée)
    - Moyens de paiement
    - À partir de quel âge ? (« Dès 3 mois. »)
20. **« ON EN A MARRE DE VOIR DE L'IA. VOICI NOS VRAIS FANS. »** (fond jaune pâle) : compteur « 1 / N » mis à jour pendant le défilement, « Faites glisser → », cartes **photo seule** de 250 × 397 px, sans légende (règle 1.5).
21. **Quiz :** le quiz existant de la page d'accueil (règle 1.4).

---

## 4. Ce qui change d'un produit à l'autre

| | Mobilité | Multivitamines | Digestion |
|---|---|---|---|
| Photo principale | `hero-mobilite.jpg` (teckel) | `hero-multivitamines.webp` (cocker, fond blanc) ; version fond bleu en réserve | `hero-digestion.jpg` (bouledogue) |
| Bienfaits (icônes) | 3 : Souplesse articulaire · Renforcement du cartilage · Soutien du dos et des hanches | 4, en grille 2 × 2 : Soutient les défenses naturelles · Soutient les articulations · Soutient la digestion · Soutient la peau et le pelage | 3 : Confort digestif · Pour un transit régulier · Soutient la peau |
| Encadré « On n'attend pas… » | oui | non | non |
| Phrase du bandeau après les avis | Faites partie des maîtres qui aident leur chien à bien vieillir. | Faites partie des maîtres qui aident leur chien à bien vieillir. | Faites partie des maîtres qui suivent la cure pour leur chien. |
| Section comparative | « Mobilité ou Multivitamines ? » | « Multivitamines ou Mobilité ? » | aucune |
| Autres produits proposés | Digestion, Multivitamines | Mobilité, Digestion | Mobilité, Multivitamines |
| Avis | 2 avis Trustpilot (Bergers Picards, Nestor) | 1 avis (chiot) | 1 avis (Claudine B., Albert) |

**Les icônes de Multivitamines et Digestion contiennent leur ancien texte dans l'image** (« Soutient l'immunité », « Soulage les gaz »…). Utilise les fichiers de `assets/bienfaits/`, qui sont recadrés sur le rond seul, et écris les libellés en HTML avec les **textes du tableau** (section 9).

**Actifs par soft chew** (metafield `jl.actifs`, une entrée par actif : image, nom, rôle, dose, référence) :

**Mobilité (6) :**
- Glucosamine (HCl) 200 mg : « Stimule la production de cartilage et absorbe les chocs articulaires. » (Osaki et al., 2012 · Marine Drugs)
- MSM marin 200 mg : « Contribue au confort articulaire et à la souplesse au quotidien. »
- Collagène bovin 100 mg : « Soutien des tissus articulaires et structure du cartilage. »
- Sulfate de chondroïtine 35 mg : « Hydratation du cartilage et glissement articulaire. »
- Vitamine C 30 mg : « Synthèse du collagène et soutien antioxydant. »
- Vitamine E 2 mg : « Protège les cellules contre le stress oxydatif. » (Barroso et al., 2024 · Veterinary Sciences)

**Multivitamines (17), dans cet ordre :**
- Glucosamine (HCl) 100 mg : « Soutien articulaire et production naturelle de cartilage. » (Osaki 2012)
- MSM 100 mg : « Confort articulaire et mobilité au quotidien. »
- Collagène bovin 100 mg : « Structure du cartilage et récupération tissulaire. »
- Moule verte 100 mg : « Source naturelle d'oméga-3, confort articulaire. »
- Parois de levure (Biolex® MB40) 50 mg : « Soutient les défenses naturelles et la barrière intestinale. » (Kroll et al., 2020 · Animal Feed Science)
- Graines de courge 50 mg : « Graine végétale, source naturelle de fibres. »
- Huile d'algues (DHA) 30 mg : « Pour une peau saine et un pelage brillant. » (Watson, 1998 · Journal of Nutrition)
- Sulfate de chondroïtine 30 mg : « Hydratation du cartilage et souplesse articulaire. »
- Vitamine C 30 mg : « Synthèse du collagène et soutien antioxydant. » (Barroso 2024)
- Extrait de thé vert 10 mg : « Source d'antioxydants. » (Barroso 2024)
- Vitamine E 2 mg : « Protège les cellules contre le stress oxydatif. »
- Vitamine B1 1 mg : « Énergie cellulaire et fonctionnement du système nerveux. »
- Vitamine B5 1 mg : « Métabolisme énergétique et santé de la peau. »
- Riboflavine B2 0,9 mg : « Production d'énergie. »
- Vitamine B6 0,5 mg : « Système nerveux et formation des globules rouges. »
- Vitamine A 0,5 mg : « Vision, défenses naturelles et santé de la peau. »
- Probiotiques (B. velezensis) 2,5×10⁸ UFC : « Équilibre du microbiote intestinal. » (Jeusette et al., 2025 · Frontiers in Veterinary Science)

**Digestion (4) :**
- Probiotiques vivants 1 Md UFC : « Équilibre intestinal et transit plus serein. » (Jeusette 2025)
- Complexe multi-enzymes 70 mg : « Assimilation plus simple et digestion soutenue. »
- Prébiotiques 50 mg : « Nourrit les bonnes bactéries du microbiote. »
- Parois de levure 50 mg : « Soutient la barrière intestinale et les défenses locales. »

**Ne reprends pas les anciens textes du site** pour les rôles des actifs. Plusieurs étaient non conformes (section 9).

---

## 5. Le panier (tiroir plein écran, style sobre)

Référence : `maquettes/panier-1-sachet.dc.html` et `panier-3e-offert.dc.html`. Fond crème, traits fins, pas d'ombres dures.

1. **En-tête :** « PANIER (n) » + croix de fermeture.
2. **Jauge de l'offre :** un message, une sous-ligne, une barre de progression en 2 étapes (1 sachet → 2 sachets, 3e offert).
   - Les textes, les étapes et le calcul dépendent de **l'offre réelle** (règle 1.3). La logique de la jauge doit pouvoir se régler.
   - Exemple de la maquette : « Ajoutez un 2e sachet : le 3e est offert » puis « Votre 3e sachet est offert ».
3. **Une ligne par produit :**
   - vignette du sachet sur un carré aux couleurs du produit ;
   - nom ;
   - sous-titre : « Soutien articulaire · goût viande » (le goût reste à confirmer par Dora) ;
   - prix (et prix barré si promotion) ;
   - sélecteur de quantité − 1 + et lien « Supprimer » ;
   - **2 boutons « Achat unique » / « Abonnement » SANS prix à l'intérieur** (Dora l'a demandé). Le prix de la ligne se met à jour selon le choix, qui modifie le `selling_plan` de la ligne.
4. **Produit offert :** prix barré + « Offert » en cobalt + lien « Changer de sachet offert ».
5. **Suggestions** (quand l'offre n'est pas atteinte) : « Ajoutez un sachet, le 3e est offert », avec les autres produits, leur prix réel et un bouton « + Ajouter ».
6. **Récapitulatif :** sous-total, réduction(s), livraison point relais.
7. **Pied fixe :** ligne de livraison, bouton cobalt « 🔒 PAYER · [total] », puis « ★★★★★ 4,8/5 Trustpilot · Remboursé 60 j · Paiement sécurisé ».

**Les propriétés de ligne** (prénom, poids) envoyées depuis la page produit doivent **rester attachées à la ligne** dans le panier et jusqu'à la commande (règle 1.1).

---

## 6. La section comparative dépliable (Mobilité et Multivitamines)

Placée juste après « Les 3 compléments se combinent ». Référence : `maquettes/comparaison-ouverte.dc.html`.

**Fermée par défaut :** une carte-bouton avec la question (« MOBILITÉ OU MULTIVITAMINES ? » sur Mobilité, « MULTIVITAMINES OU MOBILITÉ ? » sur Multi), le lien « Voir les différences » et un chevron rond. Un clic déplie, et le libellé devient « Masquer les différences ».

**Dépliée :**
- « Même posologie, deux besoins différents. »
- **2 cartes :**
  - **Mobilité, « L'expert articulations »** : « 2× plus de glucosamine et de MSM. Dès le plus jeune âge, avant les premiers signes. »
  - **Multivitamines, « Le soutien 360° »** : « Moins ciblé, plus complet : articulations, défenses, digestion, pelage. »
- **Tableau par soft chew :**

  | | Mobilité | Multi |
  |---|---|---|
  | Glucosamine | **200 mg** | 100 mg |
  | MSM | **200 mg** | 100 mg |
  | Collagène bovin | 100 mg | 100 mg |
  | Chondroïtine | 35 mg | 30 mg |
  | Moule verte | — | 100 mg |

  Puis « En plus dans Multi », avec un ✓ côté Multi pour chaque ligne :
  - Défenses naturelles (parois de levure, probiotiques) ;
  - Digestion (probiotiques, graines de courge) ;
  - Peau et pelage (huile d'algues DHA) ;
  - 7 vitamines (A, B1, B2, B5, B6, C, E).
- **Pour qui :**
  - « **Mobilité** · chien actif, grande race, ou qui commence à ralentir : on cible l'articulation. »
  - « **Multivitamines** · chien âgé qui a besoin d'un peu de tout : articulations, défenses naturelles, digestion et pelage. »
- **Bouton** « Découvrir Multivitamines » (ou « Découvrir Mobilité » sur la page Multi).

Construis le tableau **à partir des metafields d'actifs des deux produits**, pas en dur. Utilise `aria-expanded` sur la carte-bouton.

---

## 7. Images (`assets/`)

| Fichier | Où |
|---|---|
| `photos/hero-mobilite.jpg`, `hero-multivitamines.webp`, `hero-digestion.jpg` | Photo principale, 1re image de chaque galerie |
| `photos/hero-multivitamines-fond-bleu.webp` | Variante de la photo Multi, si Dora la préfère |
| `photos/logo.webp` | En-tête |
| `bienfaits/mobilite-*`, `multi-*`, `digestion-*` | Icônes des bienfaits (sans texte, section 4) |
| `actifs/mobilite-*`, `multi-*`, `digestion-*` | Ronds des actifs |
| `photos/corgi-miam.webp` | Bloc « Goût viande » (3 pages) |
| `photos/chew-main.webp` | Alternative à la friandise (3 pages) |
| `photos/event-corgi.webp` | Événements, photo 1, « Journée Corgi · Paris » |
| `photos/chien-bouvier.webp`, `chien-dalmatien.webp`, `chien-epagneul.webp` | « Nos vrais fans » |
| `photos/digestion.webp`, `multi.webp` | Cartes « Les 3 compléments se combinent » (la carte Mobilité utilise la photo de la page Mobilité) |
| `sachets/pack-*.webp` | Panier et menu |

**Réserves sur les images :**
- **Les ronds d'actifs et les icônes sont découpés dans des captures d'écran**, en définition moyenne. Remplace-les par les fichiers d'origine du site actuel s'ils existent.
- **`sachets/pack-digestion.webp` est provisoire** : il vient d'une photo et montre l'ancien emballage.
- **Les photos principales montrent le nouvel emballage** (« On va courir ? », « Prêt pour l'aventure ! », « Ça va mieux ! »), mais les vignettes de sachets du panier et du menu montrent l'ancien. Demande à Dora les 3 sachets seuls dans la nouvelle version pour harmoniser.

Importe toutes les images dans Shopify (Contenu › Fichiers) et référence-les dans les réglages de section, jamais en dur dans le code.

---

## 8. Ce qui a changé depuis la première version des instructions

- Le bloc d'achat est désormais **juste sous le nom du produit**, avant les bienfaits.
- Les 2 bulles d'achat sont **fermées par défaut et s'excluent mutuellement** (règle 1.2).
- **Ajouts :** le bandeau « Faites partie des maîtres… », la section comparative dépliable et l'encadré « On n'attend pas… » (Mobilité).
- **« Les 3 compléments se combinent »** est passé **avant** « Allie science et goût ».
- **Les actifs** sont en **liste verticale**, et non plus en défilé latéral.
- **Le bloc « vrais chiens »** a un nouveau titre, et ses photos sont **sans légende**.
- **Quiz :** reprendre l'existant (règle 1.4).
- **Prix :** tous indicatifs (règle 1.3).
- **Panier :** plus de prix dans les bulles « Achat unique » / « Abonnement ».
- **Menu :** style sobre, en-tête identique à la page produit, bulle accrochée à la croix (voir `handoff-menu-mobile/`).

---

## 9. Juridique et réglementaire

1. **Règlement UE 767/2009, article 13 :** un aliment pour animaux ne peut pas revendiquer de prévenir, traiter ou guérir une maladie ou un symptôme.
   - **Mots interdits :** préventif, traitement, soigne, soulage, réduit l'inflammation, réduit les grattements, régularise les selles, renforce l'immunité, anti-vieillissement, santé cérébrale.
   - **Les textes de ce document sont déjà reformulés.** Ne remets pas les anciens textes du site, y compris dans les images d'icônes.
2. **Article 19 du même règlement :** l'étiquetage complet (composition, constituants analytiques, additifs avec leur numéro d'autorisation, mode d'emploi) doit être accessible avant l'achat. C'est le rôle de « Voir la composition intégrale ».
   - Probiotiques et parois de levure sont des **additifs** : leur numéro d'autorisation doit figurer. Demande-le à Dora.
3. **Prix barrés (Code de la consommation, article L112-1-1) :** le prix barré doit être le **prix le plus bas des 30 derniers jours**.
4. **Avis (article L111-7-2) :** indiquer si et comment les avis sont vérifiés. Aucun avis inventé.
   - L'avis Multivitamines porte une date future (10/12/2026) : n'affiche pas de date fausse.
5. **Abonnement :** la résiliation en ligne doit tenir en 3 clics maximum. Vérifie que l'app le permet avant d'afficher « annulable en 1 clic ».
6. **Droit de rétractation de 14 jours** visible dans les CGV.
7. **Mesure d'audience** (Clarity, pixel Meta) : seulement après le consentement cookies.

---

## 10. Performance et mesure

**Performance :**
- images en `loading="lazy"`, sauf la photo principale (`fetchpriority="high"`) ;
- `width` et `height` explicites, `srcset` via `image_url` ;
- objectifs Lighthouse mobile : LCP < 2,5 s, CLS < 0,1.

**Référencement :** balisage `Product`, `Offer`, `AggregateRating` (si Trustpilot le permet) et `FAQPage`.

**Événements à mesurer :**
- bulle ouverte (abonnement ou achat unique) ;
- poids choisi ;
- prénom rempli ;
- ajout au panier ;
- ajout d'un autre produit via le « + » ;
- comparaison dépliée ;
- clic sur le quiz ;
- profondeur de défilement.

---

## 11. Checklist de livraison

- [ ] Étape 0 faite (plateforme, thème, app d'abonnement, accès), copie du thème, rien publié en ligne.
- [ ] Une seule template pour les 3 produits ; les différences viennent des metafields et des réglages (section 4).
- [ ] Ordre des blocs = section 3 ; textes identiques aux maquettes ; vouvoiement partout.
- [ ] Texte en 18 px, rien sous 16 px, champs en 16 px minimum.
- [ ] Bloc d'achat : rien de présélectionné, **une seule bulle ouverte à la fois**, bouton grisé tant qu'aucun poids n'est choisi.
- [ ] **Poids et prénom collectés exactement comme aujourd'hui**, et visibles dans la commande et dans l'outil d'e-mail.
- [ ] Aucun prix, pourcentage ni texte d'offre en dur.
- [ ] **Quiz existant de la page d'accueil** intégré, pas celui des maquettes.
- [ ] Galerie, événements et « vrais fans » acceptent N images ; aucun emplacement vide en ligne.
- [ ] Section comparative fermée par défaut sur Mobilité et Multi ; absente sur Digestion.
- [ ] Panier : pas de prix dans les bulles, propriétés de ligne conservées, jauge réglable.
- [ ] Aucun texte interdit (section 9).
- [ ] Testé sur un vrai iPhone (Safari) et un Android (Chrome), dont un petit écran.
- [ ] Lien d'aperçu envoyé à Dora, avec la liste de ce qui manque (images, vidéo, prix, offre, numéros d'additifs).
