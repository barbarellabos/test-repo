# Coder la page produit Mobilité de jacquelineslab.com

Instructions pour un agent de code (Claude Code). Rédigées le 10 nov. 2026 à partir de la maquette validée par Dora (co-fondatrice) dans Claude Design.

---

## 0. À lire avant de commencer

**Contexte.** Jacqueline's Lab vend des soft chews (compléments alimentaires pour chiens) : Mobilité, Digestion, Multivitamines. Tu recodes la **page produit Mobilité**, en **mobile d'abord** : le trafic vient surtout des pubs Meta sur téléphone.

**Comment travailler avec Dora.** Tutoiement, en français. Elle veut être challengée : si une instruction est illogique, incomplète ou fausse, dis-le avant de coder. Confirme ta compréhension en 3 à 5 lignes avant tout gros chantier. Mentionne en fin de réponse les idées que tu as écartées, avec la raison.

**Ce dossier contient :**

| Chemin | Contenu |
|---|---|
| `maquette/page-produit-mobilite.dc.html` | **La référence visuelle**, toute la page dans l'ordre |
| `maquette/bulle-achat-ouverte.dc.html` | L'état « bulle d'achat ouverte », après un clic |
| `assets/` | Toutes les images (section 9) |

Les fichiers `.dc.html` sont du HTML avec des styles en ligne, des variables `{{ x }}`, `<sc-if>` / `<sc-for>` et une classe JS `Component`. **Ce n'est pas du code à copier tel quel** : c'est la référence pour les textes, l'ordre, les couleurs, les tailles et les espacements. Ouvre-les et lis-les en entier.

**Règles de sécurité :**
- Ne publie **jamais** sur le thème en ligne. Travaille sur une **copie du thème** (Shopify : Boutique en ligne › Thèmes › Dupliquer) et envoie à Dora le lien d'aperçu.
- Ne modifie ni les prix, ni les produits, ni les apps de la boutique sans son accord.

### Première étape obligatoire : vérifier la plateforme

Le site est **a priori sur Shopify**, mais ce n'est pas confirmé. Vérifie-le, ainsi que :
- le **thème** utilisé, son nom et sa version (Online Store 2.0 ou non) ;
- l'**app d'abonnement** installée (Shopify Subscriptions, Recharge, Loop, Seal…) ;
- comment tu accèdes au code : Shopify CLI `shopify theme dev` / `pull` / `push --unpublished`, ou un dépôt GitHub relié au thème.

Si quelque chose bloque (pas d'accès, pas d'app d'abonnement), **arrête-toi et demande à Dora**.

---

## 1. Architecture à mettre en place (Shopify OS 2.0)

Le même gabarit servira ensuite pour **Digestion** et **Multivitamines**. Donc aucun texte ni aucun chiffre propre à Mobilité n'est écrit en dur dans le code.

1. Crée un template `templates/product.soft-chew.json` et assigne-le au produit Mobilité.
2. Fais **une section par bloc de la page** (section 4), toutes dans `sections/jl-*.liquid`, avec leurs réglages (`schema`). Dora doit pouvoir modifier textes, images et ordre depuis l'éditeur de thème, sans code.
3. Mets les données produit dans des **metafields produit** (namespace `jl`) :
   - `jl.actifs` : liste des actifs avec nom, rôle, dose, référence et image ;
   - `jl.posologie` : tranches de poids, nombre de soft chews par jour et jours par sachet ;
   - `jl.bienfaits` : 3 icônes et 3 libellés ;
   - `jl.couleur_produit` : couleur de la gamme (orange Mobilité `#E8501A`).
4. Mets les styles dans un seul fichier `assets/jl-product.css`, avec les variables de la section 2. Le JS doit rester léger, sans framework : un seul `assets/jl-product.js`.

---

## 2. Direction artistique

**Couleurs :**

| Variable | Hex | Usage |
|---|---|---|
| `--jl-creme` | `#FBF9F2` | Fond de page |
| `--jl-encre` | `#111111` | Texte, bordures, ombres |
| `--jl-cobalt` | `#2525DC` | Titres de section, bouton d'achat, bandeau |
| `--jl-orange` | `#E8501A` | Accent Mobilité, sélection |
| `--jl-orange-pale` | `#FBD9C7` | Fonds de pastilles |
| `--jl-orange-texte` | `#C4400F` | Nom des actifs sur fond blanc (l'orange normal n'a pas assez de contraste) |
| `--jl-jaune-pale` | `#F9E7A8` | Fond du bloc « vrais chiens » |
| `--jl-vert` | `#1C7F3D` | Digestion |
| `--jl-jaune` | `#F5D14E` | Multivitamines |
| `--jl-gris-texte` | `#3D3D3D` | Texte secondaire |
| `--jl-trustpilot` | `#00B67A` | Étoiles |

**Style néo-brutaliste :**
- bordure de 2,5 px en `#111` ;
- arrondi de 14 à 18 px ;
- ombre dure décalée `4px 5px 0 #111`, et `5px 6px` pour le bouton d'achat ;
- boutons en pilule (`border-radius: 999px`), texte en majuscules.

**Polices (Google Fonts, ou hébergées dans le thème pour la performance) :**
- **League Spartan** 700 / 800 / 900 : titres en majuscules, prix, boutons ;
- **Outfit** 400 à 700 : texte courant ;
- **Permanent Marker** : uniquement les doses des actifs.

**Tailles de texte, validées par Dora (à respecter strictement) :**
- **texte courant : 18 px** ;
- **petits textes, légendes, pastilles : 16 px minimum**, rien en dessous ;
- titres de section : 26 à 30 px, nom du produit : 42 px ;
- **champs de saisie : 16 px minimum**, sinon l'iPhone zoome tout seul quand on touche le champ.

**Mise en page :**
- maquette dessinée à **390 px de large** (iPhone 13/14), marges latérales de 16 px ;
- zones cliquables de **44 px minimum**.

---

## 3. Prix et offres : rien en dur

**Les prix et les offres ne sont pas fixés.** Les chiffres de la maquette (38,40 €, 26,11 €, 30,72 €, −20 %, −32 %, −15 %, « 3e sachet offert dès 2 ») sont des **exemples**.

- **Les prix** viennent toujours de Shopify : `variant.price`, `variant.compare_at_price` et `selling_plan` de l'app d'abonnement.
- **Le pourcentage de réduction** est calculé à partir de ces prix, jamais écrit dans le code.
- **Le prix barré** ne s'affiche que si `compare_at_price` est supérieur au prix.
- **Le prix par jour** se calcule à partir du prix réel et des jours par sachet de la tranche choisie (metafield `jl.posologie`).
- **Le texte du bandeau** (promo Black Friday ou « Satisfait ou remboursé 60 jours ») est un **réglage de section** modifiable.
- **Les seuils de livraison** (« offerte dès 70 € ») sont aussi des réglages, et le même texte doit être utilisé partout sur la page.

---

## 4. La page, dans l'ordre, bloc par bloc

Les textes ci-dessous sont ceux de la maquette. Les crochets `[...]` sont des **contenus manquants** : ne les mets pas en ligne tels quels (voir section 7).

### 4.1 Bandeau (1 ligne, fond cobalt, texte crème, majuscules)
Texte modifiable (section 3). Valeur actuelle : « Black Friday · 3e sachet offert dès 2 ». Hors promotion : « Satisfait ou remboursé 60 jours ».

### 4.2 En-tête
- Logo (`logo.webp`, environ 50 px de haut).
- Bascule **FR / EN** visible, en pilule.
- Icône panier (accessible : « Panier, N articles »).
- Bouton menu.

### 4.3 Galerie produit
- Image carrée pleine largeur, la première est `hero-mobilite.webp`.
- Points de pagination en bas, défilement au doigt.
- Les autres images de galerie ne sont pas encore validées : garde celles du site actuel.

### 4.4 Note
Étoiles Trustpilot vertes + « 4,8/5 · Trustpilot ». **Branche le widget ou l'API Trustpilot**, ne code pas la note en dur.

### 4.5 Nom et accroche du bloc d'achat
- « MOBILITÉ » : 42 px, cobalt, League Spartan 900.
- Juste dessous : « CHOISIS TA FORMULE ».

### 4.6 Bloc d'achat (le plus important, voir aussi la section 5)
- **2 bulles l'une sous l'autre : « Abonnement » (badge « Recommandé ») et « Achat unique ».**
- **Rien n'est présélectionné au chargement.**
- Chaque bulle fermée affiche :
  - un bouton radio vide ;
  - le nom de l'option ;
  - le prix barré, s'il existe, et le prix ;
  - une ligne de texte : « Livraison offerte · sans engagement » pour l'abonnement, « Sans engagement · pour tester d'abord » pour l'achat unique ;
  - une pastille avec le pourcentage de réduction, calculé.
- Au clic, **la bulle s'ouvre** et l'autre reste fermée ou se referme (section 5).

### 4.7 Les bienfaits clefs
- Titre « LES BIENFAITS CLEFS », en cobalt.
- 3 colonnes avec les icônes `ic-mouvement.webp`, `ic-cartilage.webp` et `ic-dos.webp`, en 64 px, dans cet ordre.
- Libellés en cobalt et majuscules : « Souplesse articulaire », « Renforcement du cartilage », « Soutien du dos et des hanches ».

### 4.8 Posologie
- Carte blanche avec « 60 SOFT CHEWS par sachet, un RITUEL QUOTIDIEN : ».
- 3 pastilles orange pâle : « 1-10 kg · 1 / jour », « 11-30 kg · 2 / jour », « +30 kg · 3 / jour ». Elles viennent du metafield.

### 4.9 Ils l'ont testé (défilé latéral)
- Titre « ILS L'ONT TESTÉ. » + « Glisse → ».
- Cartes d'avis de 290 px de large ; la suivante doit **dépasser** à droite.
- Les avis viennent de Trustpilot (vrais avis uniquement).
- Bouton « Lire tous les avis ».

### 4.10 Les 3 compléments se combinent (fond cobalt)
- Une carte par autre produit : Digestion et Multivitamines.
- Chaque carte : image, nom, phrase (« Pour un ventre en paix », « Soutien 360° »), **prix venant de Shopify**, lien « Voir la fiche ».
- Bouton rond « + » qui **ajoute au panier sans quitter la page** (AJAX `/cart/add.js`, puis mise à jour du compteur du panier). Couleur du « + » : vert pour Digestion, jaune pour Multivitamines.

### 4.11 Allie science et goût
- Titre « ALLIE SCIENCE ET GOÛT. » + « Formulé par des vétérinaires nutritionnistes ».
- **Bloc orange « GOÛT VIANDE »**, presque carré (environ 190 px de haut) :
  - photo `corgi-miam.webp` à gauche, environ 150 px de large ;
  - texte à droite : « Tendre, il le prend comme une friandise. »
- Puis « SES 6 ACTIFS · DOSES PAR SOFT CHEW » et **une liste verticale de 6 cartes** blanches. Chaque carte : rond image de 52 px, nom en `#C4400F`, rôle, référence éventuelle en italique, dose à droite en Permanent Marker.

| Image | Actif | Rôle (texte validé) | Dose | Référence |
|---|---|---|---|---|
| `actif-glucosamine.png` | Glucosamine (HCl) | Stimule la production de cartilage et absorbe les chocs articulaires. | 200 mg | Osaki et al., 2012 · Marine Drugs |
| `actif-msm.png` | MSM marin | Contribue au confort articulaire et à la souplesse au quotidien. | 200 mg | |
| `actif-collagene.png` | Collagène bovin | Soutien des tissus articulaires et structure du cartilage. | 100 mg | |
| `actif-chondroitine.png` | Sulfate de chondroïtine | Hydratation du cartilage et glissement articulaire. | 35 mg | |
| `actif-vitc.png` | Vitamine C | Synthèse du collagène et soutien antioxydant. | 30 mg | |
| `actif-vite.png` | Vitamine E | Protège les cellules contre le stress oxydatif. | 2 mg | Barroso et al., 2024 · Veterinary Sciences |

- Pastille « Sans sucre ajouté · sans mauvais gras ».
- Bouton « VOIR LA COMPOSITION INTÉGRALE », qui ouvre la fiche complète (section 6, point 1).
- Les images des actifs ont été découpées dans une capture d'écran et sont en basse définition. **Remplace-les par les originaux du site actuel** s'ils existent.

### 4.12 L'alternative à la friandise
- Titre en cobalt.
- Carte avec la photo `chew-main.webp` (main qui tient le soft chew en cœur), puis un tableau de 3 lignes :

| Friandise classique | Mobilité |
|---|---|
| Gourmande | Gourmande |
| Rien d'utile en plus | 6 actifs dosés |
| À l'occasion | Chaque jour |

- Phrase en dessous : « Tu lui donnes déjà une friandise ? Remplace-la par son soft chew. »

### 4.13 Sur le terrain (défilé latéral)
- « SUR LE TERRAIN, CHIEN APRÈS CHIEN. » + « On part à la rencontre des chiens et de leurs maîtres, partout en France. »
- Défilé de photos d'événements, chacune avec une légende.
  - Photo 1 : `event-corgi.webp`, légende « Journée Corgi · Paris ».
  - Les autres photos et légendes sont à fournir par Dora.
- Encadré orange pâle : « 50+ » / « événements en France » / « Observé en événement, pas un essai clinique. »

### 4.14 L'avis de l'ostéopathe
- Lecteur vidéo 16:9 + citation + nom.
- **Vidéo, citation et nom sont à fournir** : masque la section tant qu'ils sont vides.

### 4.15 Son rituel de tous les jours
Frise verticale en 3 étapes :
1. « Jours 1 à 10 · La mise en route · Ton chien adopte son rituel. »
2. « Dès 1 mois · La routine ancrée · Le geste devient automatique. »
3. « 3 mois · Le bilan · Cure de 3 mois minimum, idéalement en continu. » (étape en orange)

### 4.16 Tes questions (FAQ en accordéon)
- Combien par jour ? : « 1 de 1 à 10 kg, 2 de 11 à 30 kg, 3 au-delà. Un sachet contient 60 soft chews. »
- Et si ça ne lui plaît pas ? : « Satisfait ou remboursé 60 jours, sans formulaire. »
- Livraison et retours : texte de livraison venant du réglage commun (section 3).
- Comment marche l'abonnement ? : réduction **calculée**, « livraison offerte, modifiable et annulable en 1 clic » (section 6, point 4).
- Moyens de paiement : « Carte, PayPal ou Apple Pay, paiement sécurisé. »
- À partir de quel âge ? : « Dès 3 mois. »

Utilise `<details>` / `<summary>` et ajoute le **balisage FAQPage** (schema.org) pour le référencement.

### 4.17 Zéro image IA. Que des vrais chiens. (défilé latéral, fond jaune pâle)
- Sous-titre « Ils goûtent leurs chews, en vrai, sur nos stands. »
- Compteur « 1 / 3 » **qui se met à jour** pendant le défilement, + « Glisse → ».
- 3 cartes de 250 × 330 px, dans cet ordre : `chien-bouvier.webp`, `chien-dalmatien.webp`, `chien-epagneul.webp`.
- Légendes : « [Prénom] · bouvier bernois », etc. **Prénoms à fournir.**

### 4.18 Quiz (fond cobalt, tout en bas)
- « PAS SÛR QUE CE SOIT LE BON CHOIX POUR TON CHIEN ? » + « 3 questions, et on t'envoie vers le complément qu'il lui faut. »
- Question 1 : « Qu'est-ce qui compte le plus pour lui en ce moment ? » Réponses, chacune avec une pastille de couleur :
  - « Ses articulations, il ralentit » → Mobilité
  - « Son ventre, sa digestion » → Digestion
  - « Sa forme au quotidien » → Multivitamines
- **Les questions 2 et 3 ne sont pas écrites** : demande-les à Dora.
- Le résultat renvoie vers la page produit concernée, avec la tranche de poids en paramètre d'URL pour la présélectionner.
- Si le site a déjà un quiz ou une app de quiz, **réutilise-le**.

---

## 5. Comportement du bloc d'achat (détail)

1. **État initial :** les 2 bulles sont fermées, rien n'est coché, aucun poids n'est choisi. Il n'y a pas de barre d'achat collante.
2. **Clic sur une bulle :**
   - elle prend la bordure intérieure orange de 3 px et son point radio se remplit ;
   - elle s'ouvre avec une animation courte (moins de 200 ms, désactivée si `prefers-reduced-motion`) ;
   - l'autre bulle se ferme.
3. **Dans la bulle ouverte :**
   1. « 1 · POIDS DE TON CHIEN » : 3 boutons « 1–10 kg », « 11–30 kg », « + de 30 kg », aucun présélectionné.
      - Avant le choix, la ligne d'info affiche « Choisis son poids : on calcule sa dose. »
      - Après le choix : « 2 soft chews par jour · un sachet de 60 dure environ 1 mois · soit X,XX € par jour », calculé avec le **prix réel** de l'option.
   2. « 2 · LE PRÉNOM DE TON CHIEN » : champ texte, exemple « Ex. Nestor ». Envoie-le comme **propriété de ligne de commande** : `properties[Prénom du chien]`. Le poids choisi part aussi en propriété (`properties[Poids]`).
   3. Bouton d'achat :
      - grisé avec « CHOISIS SON POIDS » tant qu'aucun poids n'est choisi ;
      - puis cobalt avec « ACHETER · [prix] € ».
      - En abonnement, il envoie le bon `selling_plan`.
   4. En dessous : « Cure de 3 mois recommandée, idéalement en continu. », « Satisfait ou remboursé », et la ligne de livraison commune.
4. **Le poids ne change pas le produit :** c'est le même sachet pour toutes les tranches. Il sert à la dose et au prix par jour. Ne crée pas de variantes par poids, sauf si Dora le demande.
5. **Accessibilité :**
   - les bulles sont un vrai groupe de boutons radio (`role="radiogroup"` ou `<input type="radio">`) ;
   - la bulle ouverte porte `aria-expanded` ;
   - le champ prénom a un vrai `<label>` ;
   - tout est utilisable au clavier.

---

## 6. Juridique et réglementaire (à respecter dans le code et les textes)

1. **Aliments pour animaux, règlement UE 767/2009, article 13 :** aucune allégation de prévention, de traitement ou de guérison d'une maladie. Mots interdits sur la page : « prévention », « traitement », « soigne », « réduit l'inflammation », « douleurs ». Les rôles des actifs ci-dessus sont déjà reformulés : **ne reprends pas les anciens textes du site.**
   - L'article 19 impose aussi de donner les mentions d'étiquetage avant l'achat en ligne : composition, constituants analytiques, additifs, mode d'emploi. Le bouton « Voir la composition intégrale » doit donc mener à la fiche complète de l'étiquette.
2. **Prix barrés (directive Omnibus, article L112-1-1 du Code de la consommation) :** le prix de référence barré doit être **le prix le plus bas des 30 derniers jours**. Préviens Dora si le `compare_at_price` ne le respecte pas.
3. **Avis clients (article L111-7-2 du Code de la consommation) :** indique si les avis sont vérifiés et comment, avec un lien « Comment nous vérifions les avis » ou la mention Trustpilot. Aucun avis inventé, même en attendant.
4. **Abonnement :** depuis juin 2023, la résiliation en ligne doit se faire en 3 clics maximum. Vérifie que l'app d'abonnement le permet avant d'afficher « annulable en 1 clic ».
5. **Droit de rétractation de 14 jours :** il doit être visible dans les CGV, accessibles depuis la page.
6. **Droit à l'image :** `event-corgi.webp`, c'est réglé : les deux personnes du stand sont les fondatrices. Pour toute nouvelle photo avec des personnes reconnaissables, demande d'abord à Dora si l'accord écrit existe.
7. **Mesure d'audience** (Microsoft Clarity, Meta Pixel) : rien ne se déclenche avant le **consentement** donné dans le bandeau cookies.

---

## 7. Contenus manquants : ne rien mettre en ligne avec un crochet

Tout texte entre `[...]` dans la maquette est un trou. Pour chacun, **masque l'élément** tant qu'il est vide (réglage de section vide = bloc caché) et donne la liste à Dora :
- prénoms des chiens (bloc 4.17) ;
- photos et légendes d'événements (nom, ville, date) ;
- vidéo, citation et nom de l'ostéopathe ;
- 3e avis Trustpilot avec photo du chien ;
- questions 2 et 3 du quiz ;
- liste datée des 50+ événements, pour le lien de preuve ;
- **prix et offres définitifs** (section 3).

---

## 8. Performance, référencement, mesure

**Images :**
- `loading="lazy"` sur tout, sauf l'image principale qui garde `fetchpriority="high"` ;
- `width` et `height` explicites, `srcset` via `image_url` de Shopify.

**Défilés latéraux :**
- CSS `scroll-snap-type: x mandatory` + **`scroll-padding-left` égal à la marge gauche**, sinon la première carte colle au bord (bug déjà constaté sur la maquette) ;
- la carte suivante dépasse toujours pour inviter à faire glisser ;
- pas de bibliothèque de carrousel.

**Objectifs mobiles (Lighthouse) :** LCP < 2,5 s, CLS < 0,1.

**Référencement :** balisage `Product` + `Offer` + `AggregateRating` (si la note vient de Trustpilot) + `FAQPage`.

**Événements à mesurer** (pour comparer avant / après sur la même source Meta) :
- bulle ouverte (abonnement ou achat unique) ;
- poids choisi ;
- prénom rempli ;
- ajout au panier ;
- ajout d'un produit complémentaire via le « + » ;
- clic sur le quiz ;
- profondeur de défilement.

---

## 9. Images fournies (`assets/`)

| Fichier | Où |
|---|---|
| `logo.webp` | En-tête |
| `hero-mobilite.webp` | Galerie, image 1 |
| `ic-mouvement.webp`, `ic-cartilage.webp`, `ic-dos.webp` | Bienfaits clefs, dans cet ordre |
| `digestion.webp`, `multi.webp` | Les 3 compléments se combinent |
| `corgi-miam.webp` | Bloc « Goût viande » |
| `actif-*.png` (6) | Liste des actifs (basse définition, à remplacer si possible) |
| `chew-main.webp` | L'alternative à la friandise |
| `event-corgi.webp` | Sur le terrain, photo 1 (déjà recadrée) |
| `chien-main.webp` | Sur le terrain, photo 2 (provisoire) |
| `chien-bouvier.webp`, `chien-dalmatien.webp`, `chien-epagneul.webp` | Zéro image IA |

Importe-les dans Shopify (Contenu › Fichiers) et référence-les dans les réglages de section, pas en dur dans le code.

---

## 10. Hors périmètre de la maquette : propose, ne décide pas

- **Version ordinateur :** elle n'a pas été dessinée. Proposition à soumettre à Dora :
  - galerie à gauche et bloc d'achat à droite (collant au défilement) au-dessus de 990 px ;
  - le reste de la page en une colonne centrée de 720 px maximum.
- **Barre d'achat collante en bas sur mobile :** retirée de la maquette pour l'instant. Ne l'ajoute pas sans accord.
- **Pages Digestion et Multivitamines :** même template, avec les metafields et la couleur de gamme changés. Pas avant la validation de Mobilité.

---

## 11. Checklist de livraison

- [ ] Plateforme, thème et app d'abonnement vérifiés, et confirmés à Dora.
- [ ] Travail sur une copie du thème, rien de publié en ligne.
- [ ] Ordre des blocs = section 4, textes identiques à la maquette.
- [ ] Texte à 18 px, rien sous 16 px, champs à 16 px minimum.
- [ ] Aucun prix ni pourcentage écrit en dur.
- [ ] Bloc d'achat : rien de présélectionné, la bulle s'ouvre, poids + prénom, bouton grisé tant qu'aucun poids n'est choisi, propriétés envoyées au panier, `selling_plan` correct.
- [ ] Ajout au panier testé en abonnement et en achat unique, jusqu'à la page de paiement (sans payer).
- [ ] Défilés : marge à gauche respectée, carte suivante visible, compteur « 1 / 3 » à jour.
- [ ] Aucun `[...]` visible, les blocs vides sont masqués.
- [ ] Aucune allégation interdite (section 6).
- [ ] Lighthouse mobile mesuré, scores envoyés à Dora.
- [ ] Testé sur un vrai iPhone (Safari) et un Android (Chrome).
- [ ] Lien d'aperçu du thème envoyé à Dora, avec la liste des contenus manquants (section 7).
