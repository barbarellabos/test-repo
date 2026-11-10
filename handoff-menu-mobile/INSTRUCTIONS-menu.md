# Coder le menu mobile de jacquelineslab.com

Instructions pour un agent de code (Claude Code). Rédigées le 10 nov. 2026 à partir de la maquette validée par Dora (co-fondatrice).

Ce document complète `handoff-page-produit-mobilite/INSTRUCTIONS.md`. Les règles générales sont les mêmes :
- Shopify à vérifier ;
- travail sur une copie du thème, jamais sur le thème en ligne ;
- vouvoiement sur le site ;
- texte à 18 px, rien sous 16 px ;
- direction artistique (couleurs, bordures, ombres, polices) de la section 2 de ce document.

---

## 0. Ce qu'on remplace

**Aujourd'hui**, le menu mobile s'ouvre en **plein écran** et contient : MOBILITÉ, MULTIVITAMINES : SOUTIEN 360°, DIGESTION, MON COMPTE, PANIER, une bascule FR/EN et une illustration de bouledogue.

**Demain**, le menu s'ouvre en **bulle flottante** au-dessus de la page, qui reste visible derrière sous un **voile gris**.

**Inspirations** fournies par Dora :
- **Balto** : cartes produit avec visuel et sous-titre ;
- **Cuure** : panneau arrondi par-dessus la page assombrie.

Ne copie pas leur style : on reste dans la direction artistique Jacqueline's Lab.

**Fichiers :**

| Chemin | Contenu |
|---|---|
| `maquette/menu-mobile.dc.html` | **La référence visuelle**, cliquable (la croix ferme, le burger rouvre) |
| `assets/pack-mobilite.webp`, `pack-digestion.webp`, `pack-multi.webp` | Visuels des sachets |
| `assets/logo.webp` | Logo |

`pack-digestion.webp` est **provisoire** : il a été découpé dans une photo du site. Dora fournira le visuel du sachet seul ; remplace-le dès qu'il arrive.

---

## 1. Contenu de la bulle, dans l'ordre

### 1. Mon compte / Mon panier
Deux boutons pilule côte à côte, blancs, bordure de 2,5 px, ombre `3px 4px #111`, 52 px de haut, texte League Spartan 800 de 16 px en majuscules.
- **« Mon compte »** avec une icône de bonhomme (contour). Lien vers `/account`, qui renvoie sur la connexion si le client n'est pas connecté.
- **« Mon panier »** avec une icône de panier et une **pastille orange** donnant le nombre d'articles (`cart.item_count`), masquée si le panier est vide. Lien vers `/cart`, ou ouverture du tiroir panier si le thème en a un.

### 2. La gamme
- Titre « LA GAMME » : League Spartan 900, 20 px, cobalt.
- **3 cartes produit**, une sous l'autre et **cliquables en entier** (toute la carte est un lien) :

| Produit | Fond de la carte | Visuel | Sous-titre |
|---|---|---|---|
| Mobilité | `#FBD9C7` (orange pâle) | `pack-mobilite.webp` | Des articulations plus souples |
| Digestion | `#CFE7D6` (vert pâle) | `pack-digestion.webp` | Pour un ventre en paix |
| Multivitamines | `#F9E7A8` (jaune pâle) | `pack-multi.webp` | Soutien 360° au quotidien |

- Chaque carte : 104 px de haut, sachet à gauche (environ 62 × 92 px, `object-fit: contain`), nom en League Spartan 900 de 22 px en majuscules, sous-titre de 16 px, chevron « › » à droite. Bordure de 2,5 px, arrondi de 16 px, ombre `3px 4px #111`.
- **Ne code pas la liste en dur** : construis-la depuis un **menu Shopify** (Navigation › un menu « Gamme ») ou une **collection**. Le visuel et le sous-titre viennent d'un metafield produit (`jl.menu_sous_titre`) ou des réglages de la section. Un 4e produit doit pouvoir s'ajouter sans toucher au code.

### 3. Quiz
- Phrase centrée en 16 px : « Vous hésitez ? Trouvez son complément en 3 questions. »
- Bouton cobalt pleine largeur « FAIRE LE QUIZ », 54 px de haut, ombre `5px 6px #111`.
- Il mène au **quiz déjà en place sur le site** : retrouve son URL, ne le recode pas.

### Ce qui disparaît du menu
- **La bascule FR/EN** : elle reste visible dans l'en-tête, inutile de la doubler.
- **L'illustration du bouledogue.**

---

## 2. La bulle et son comportement

**Ouverture et fermeture :**
- Le bouton burger de l'en-tête ouvre la bulle et se transforme en **croix**.
- Un clic sur la croix, **sur le voile gris** ou la touche **Échap** ferme la bulle.

**Disposition :**
- **L'en-tête reste visible et cliquable** au-dessus du voile (logo, FR/EN, croix).
- Voile : `rgba(40, 40, 40, .55)` sur toute la page sous l'en-tête.
- **L'en-tête du menu ouvert est exactement celui de la nouvelle page produit** : même bandeau, en-tête de 91 px avec le logo de 85 px de haut, FR/EN, icône panier, puis le bouton menu. Ne crée pas un en-tête différent pour le menu.
- **La bulle est accrochée à la croix.** Quand le menu s'ouvre :
  - le bouton burger devient une croix et perd sa bordure du bas (arrondi seulement en haut, `12px 12px 0 0`) ;
  - il se prolonge vers le bas, à la même largeur et avec les mêmes bordures latérales de 2,5 px, jusqu'à la bulle ;
  - la croix et la bulle forment ainsi **un seul objet**, comme un onglet ;
  - la bulle commence juste sous l'en-tête, son coin haut droit n'est pas arrondi (`border-radius: 22px 0 22px 22px`) et son bord droit est aligné avec celui de la croix ;
  - voir `maquette/menu-mobile.dc.html`, élément « Raccord ».
- Bulle : à 12 px des bords gauche et droit. Fond crème `#FBF9F2`, bordure de 2,5 px en `#111`, ombre dure `5px 6px #111`, marges intérieures de 16 px.
- **La bulle ne prend pas toute la page.** Si l'écran est trop petit, c'est la bulle qui défile (`max-height` avec `overflow-y: auto`), pas la page.

**Comportement :**
- Défilement de la page **bloqué** tant que le menu est ouvert.
- Animation courte à l'ouverture : la bulle descend de 8 px et apparaît en fondu, en moins de 200 ms. Pas d'animation si `prefers-reduced-motion`.
- Version ordinateur : non dessinée. Garde le menu actuel au-dessus de 990 px, sauf demande de Dora.

**Accessibilité :**
- Le bouton porte `aria-expanded` et `aria-controls`.
- La bulle est un `<nav aria-label="Menu principal">`.
- À l'ouverture, le focus va sur le premier lien et reste dans la bulle tant qu'elle est ouverte ; à la fermeture, il revient sur le bouton.
- Zones cliquables de 44 px minimum.

---

## 3. Mesure

Envoie un événement pour chaque :
- ouverture du menu ;
- clic sur une carte produit (avec le nom du produit) ;
- clic sur « Faire le quiz » ;
- clic sur « Mon compte » ;
- clic sur « Mon panier ».

Rien ne se déclenche avant le consentement cookies.

---

## 4. À signaler à Dora (pas à corriger dans le code)

- **Faute sur le sachet Multivitamines** : la bulle de l'emballage dit « MA FRIANDIES INTELLIGENTE ! » au lieu de « FRIANDISE ». C'est visible dans le menu, sur la page produit et sur le sachet imprimé.
- **Le visuel Digestion** reste provisoire tant que le visuel du sachet seul n'est pas fourni.

---

## 5. Checklist

- [ ] Ordre : Mon compte / Mon panier → La gamme (3 cartes) → Faire le quiz.
- [ ] La bulle ne couvre pas toute la page, le voile gris est visible autour, l'en-tête reste au-dessus.
- [ ] En-tête identique à celui de la page produit ; la bulle est raccordée à la croix sans trait entre les deux.
- [ ] Fermeture par la croix, le voile ou Échap. Défilement de la page bloqué quand le menu est ouvert.
- [ ] Compteur du panier exact, masqué à 0.
- [ ] Produits issus d'un menu ou d'une collection Shopify, pas écrits en dur.
- [ ] Le bouton du quiz mène au quiz existant.
- [ ] Textes au vouvoiement, rien sous 16 px.
- [ ] Testé sur un vrai iPhone (Safari) et un Android (Chrome), y compris un petit écran (iPhone SE).
