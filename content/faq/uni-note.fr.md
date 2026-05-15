---
title: "FAQ (Uni:Note)"
description: "Questions fréquentes sur Uni:Note."
---

## Général

### Quel type d’app est Uni:Note ?
Uni:Note est une app de prise de notes manuscrites sur iPad.  
Elle est conçue autour de l’écriture avec l’Apple Pencil et de l’organisation des notes par matière.

### Quels appareils sont pris en charge ?
iPad uniquement.

### Y a-t-il des limites dans la version gratuite ?
Oui.  
Dans l’état actuel de l’app, la version gratuite est limitée à **10 matières maximum** et **6 notes maximum par matière**.

Premium supprime les limites sur le nombre de matières et de notes, et donne accès à Déplacer la zone, à l’enregistrement et à la sauvegarde facile.

### Quelles langues sont prises en charge ?
L’app prend actuellement en charge :

- le japonais
- l’anglais
- le coréen
- l’allemand
- le chinois traditionnel
- le français

### Quelles sont les principales nouveautés de la v3.0.0 ?
La v3.0.0 est une mise à jour importante des aides à l’étude et des outils de note.

- L’`Assistant de résolution` est de nouveau disponible et accessible en haut de l’écran de note
- La `Règle` a été ajoutée
- `Déplacer la zone` a été ajouté
- La `Fonction de mémorisation` a été entièrement repensée sous forme de marqueurs pense-bête
- `Enregistrement`, transcription en temps réel et Résumé IA ont été ajoutés
- Le réordonnancement des matières sur l’accueil et des notes dans la liste des notes a été ajouté
- Des diagnostics et analyses de plantage via Firebase Crashlytics ont été ajoutés

Les données de diagnostic et de plantage ne contiennent pas le contenu des notes, l’écriture manuscrite, les noms de matières, les pièces jointes, les images, les PDF ni le contenu des enregistrements.

### Puis-je utiliser l’app avec `Split View` ou `Slide Over` ?
Oui.  
Uni:Note prend en charge les modes multifenêtres de l’iPad comme `Split View` et `Slide Over`.

En général, ouvrez d’abord Uni:Note, affichez le Dock, puis faites glisser une autre app ou Uni:Note depuis le Dock sur le côté pour `Split View`, ou en superposition flottante pour `Slide Over`.

L’interface exacte et les intitulés peuvent légèrement varier selon la version d’iPadOS.

### Puis-je ouvrir deux fenêtres Uni:Note en même temps ?
Oui.  
Uni:Note prend en charge plusieurs fenêtres.

Avec une fenêtre Uni:Note déjà ouverte, affichez le Dock, maintenez l’icône Uni:Note, puis choisissez l’option d’ouverture d’une nouvelle fenêtre.

Une fois la seconde fenêtre ouverte, vous pouvez l’afficher côte à côte en `Split View` ou en superposition avec `Slide Over`.

### L’Apple Pencil est-il nécessaire ?
Les fonctions manuscrites sont conçues pour l’Apple Pencil.  
L’utilisation du doigt sert surtout au défilement et à la manipulation des photos, documents photo et PDF.

### Dois-je me connecter ou créer un compte ?
Non.

---

## Notes et pages

### Le titre d’une note est-il obligatoire ?
Non.  
Si vous laissez le titre vide, la date du jour sera utilisée comme nom de note.

### Que signifie la zone de saisie du titre affichée à la première ouverture d’une matière ?
Il s’agit du titre de la première note.  
Si vous la laissez vide et choisissez **OK** ou **Écrire directement**, la date du jour sera utilisée.

Si vous revenez en arrière sans rien confirmer, la première note en cours de création n’est pas conservée.

### Que peut-on choisir lors de la création d’une matière ?
Vous pouvez choisir :

- `nom de la matière`
- type de papier : ligné / vertical / quadrillé / uni
- `Couleur du papier`
- couleur de couverture
- `Utiliser comme cahier portrait` lorsque `Vertical` est sélectionné

### Qu’est-ce qu’un cahier portrait ?
Il s’agit d’une mise en page disponible lorsque vous créez une matière avec `Vertical`.  
Si vous activez **Utiliser comme cahier portrait**, la note s’affiche comme une quasi double page en paysage, une page à la fois en portrait, avec un défilement horizontal.

L’orientation du cahier ne peut pas être changée après sa création.

### Puis-je séparer plusieurs notes dans une même matière ?
Oui.  
Vous pouvez en ajouter une depuis **Nouvelle note** dans **Liste des notes**.

Vous pouvez aussi réordonner les notes dans **Liste des notes**.

### Comment les nouvelles pages sont-elles ajoutées ?
Lorsque vous commencez à écrire sur la dernière page, la suivante est ajoutée automatiquement.

### Quel est le nombre maximum de pages dans une note ?
Une note peut contenir jusqu’à `150` pages.  
Une fois `150` pages atteintes, vous ne pouvez plus en ajouter. Le collage de PDF ne peut pas non plus ajouter des pages au-delà de cette limite. Si besoin, ajoutez une autre note dans la même matière.

### Puis-je zoomer ?
Oui.  
Sur l’écran de note, vous pouvez zoomer ou dézoomer avec un pincement à deux doigts.

### Puis-je entourer une zone manuscrite pour la déplacer ?
Oui.
Depuis **Déplacer la zone** en haut de l’écran de note, vous pouvez sélectionner et déplacer plusieurs traits manuscrits ensemble.

Déroulement :

- choisissez **Déplacer la zone**
- entourez avec l’Apple Pencil la zone manuscrite à déplacer
- faites glisser l’écriture sélectionnée

Tout trait même partiellement inclus dans la zone entourée est sélectionné en entier. Cela concerne les traits manuscrits ; les photos, les PDF et les marqueurs pense-bête se manipulent séparément.
**Déplacer la zone** est une fonction Premium.

### Puis-je supprimer une page ?
Oui.  
Vous pouvez supprimer une page en la maintenant dans **Pages**.

Cependant, si une note ne contient qu’une seule page, la page reste et seul son contenu est effacé.

### Puis-je protéger une note ?
Oui.  
Lorsque vous choisissez **Protéger** dans **Liste des notes**, la note devient en lecture seule. Vous pouvez aussi exiger la biométrie pour retirer la protection.

### Puis-je modifier une matière ?
Oui.  
Maintenez la matière sur l’accueil puis ouvrez **Modifier**.

Vous pouvez changer :

- `nom de la matière`
- type de papier
- `Couleur du papier`
- couleur de couverture

L’orientation du cahier ne peut pas être changée après création.  
Les titres des notes peuvent toujours être modifiés depuis **Liste des notes**.

Vous pouvez aussi réordonner les matières sur l’accueil.

### Que peut-on restaurer depuis la corbeille ?
Les matières et les notes affichées dans la liste des notes.  
La **Corbeille** regroupe les éléments supprimés par matière, et toucher une matière affiche les notes qu’elle contient.

Même si une matière est supprimée, vous pouvez restaurer toute la matière ou seulement certaines notes.  
Les pages supprimées ne vont pas dans la corbeille et sont supprimées immédiatement.

---

## Photos et PDF

### Puis-je insérer des photos ?
Oui.  
Vous pouvez ajouter des photos une par une avec **Coller une photo**. Une fois ajoutées, elles peuvent être déplacées ou redimensionnées, et un double toucher permet de les verrouiller ou de les déverrouiller.

### Puis-je coller une photo comme document ?
Oui.  
Choisissez **Coller une photo comme document** dans **Plus**, prenez une photo depuis l’appareil photo ou la photothèque, ajustez-la dans l’interface de correction puis insérez-la comme document.

Après insertion, vous pouvez la verrouiller ou la déverrouiller par double touche, puis ajuster sa position et sa taille avec les doigts.

### Puis-je insérer des PDF ?
Oui.  
Choisissez **Coller un PDF** dans **Plus**.

- Vous pouvez sélectionner une ou plusieurs pages d’un fichier PDF
- Vous pouvez activer **Scinder la double page** pour couper une double page au centre
- Vous pouvez coller plusieurs pages PDF en une seule opération

Après insertion, vous pouvez la verrouiller ou la déverrouiller par double touche, puis ajuster sa position et sa taille avec les doigts.

### Puis-je exporter des PDF ?
Oui.  
Choisissez **Exporter en PDF** dans **Plus** pour exporter **Cette note uniquement** ou toute la matière en PDF.

---

## Enregistrement et transcription

### Puis-je utiliser l’enregistrement ?
Oui.
Le bouton **Enregistrement** en haut de l’écran de note ouvre le panneau d’enregistrement.

- démarrer / mettre en pause / arrêter l’enregistrement
- lire / parcourir / modifier la vitesse de lecture
- renommer un enregistrement
- verrouiller ou déverrouiller un enregistrement
- supprimer un enregistrement
- partager l’audio de l’enregistrement

L’enregistrement, la lecture et l’affichage des transcriptions sont des fonctions **Premium**.
Une note peut conserver jusqu’à `5` enregistrements.
Chaque fichier d’enregistrement peut durer jusqu’à 30 minutes. Lorsqu’un enregistrement atteint 30 minutes, Uni:Note le sauvegarde automatiquement et démarre l’enregistrement suivant.
Les enregistrements divisés automatiquement comptent dans la limite de `5` enregistrements par note.
Si vous revenez à l’accueil de Uni:Note ou si l’iPad se met en veille pendant un enregistrement, l’enregistrement se termine et est sauvegardé à ce moment-là.
Cette action pendant un enregistrement peut endommager les données d’enregistrement. Arrêtez et sauvegardez l’enregistrement avant de quitter la note ou de mettre l’iPad en veille.

### Puis-je utiliser la transcription et le Résumé IA ?
Sur les appareils compatibles, Uni:Note peut afficher une transcription en temps réel pendant l’enregistrement.
Selon les modèles compatibles avec la transcription indiqués par Apple, la transcription en temps réel et le Résumé IA sont disponibles sous iPadOS 26 ou version ultérieure sur iPad mini (6e génération ou ultérieure), iPad (10e génération ou ultérieure), iPad Air (4e génération ou ultérieure), iPad Pro 11 pouces (3e génération ou ultérieure), iPad Pro 12,9 pouces (5e génération ou ultérieure) et iPad Pro 13 pouces (M4 ou ultérieur).

Le Résumé IA est généré à partir du texte de transcription déjà créé sur l’appareil.
Les fichiers audio ne sont pas envoyés pour le Résumé IA.

Le Résumé IA peut créer une note reconstruite au format Études ou Réunion à partir des transcriptions sélectionnées. Si plusieurs enregistrements sont sélectionnés, Uni:Note conserve les séparations entre enregistrements. Avant de l’exécuter, vous pouvez vérifier le nombre d’enregistrements, le nombre de caractères et l’estimation de consommation IA.

Le Résumé IA nécessite du **solde IA**.

### Les enregistrements sont-ils inclus dans les sauvegardes ?
Les sauvegardes standard incluent les informations d’enregistrement et les transcriptions.
Les fichiers audio d’enregistrement (m4a) sont inclus dans `Exporter la sauvegarde` et dans la `sauvegarde facile` uniquement si **Inclure l’audio des enregistrements dans les sauvegardes** est activé.

---

## Aide à l’étude

### Qu’est-ce que la `Fonction de mémorisation` ?
Activez la **Fonction de mémorisation** dans `Réglages > Aide à l'étude` pour utiliser le **Marqueur pense-bête** sur l’écran de note.

- masquer des zones avec le **Marqueur pense-bête**
- chaque trait est enregistré comme un pense-bête indépendant
- toucher un pense-bête avec le doigt pour alterner entre transparent et opaque
- appuyer longuement avec le doigt, puis utiliser le bouton de suppression qui apparaît

### Puis-je afficher ou masquer tous les marqueurs d’une page en une seule fois ?
Non.  
Dans la v3.0.0, l’ancien fonctionnement d’ouverture / fermeture de toute la page est remplacé par un réglage de transparence par pense-bête.

Les anciens marqueurs de mémorisation des versions précédentes sont migrés en marqueurs pense-bête à l’ouverture de la page.

### Quel est l’état actuel des fonctions d’aide à l’étude ?
L’`Assistant de résolution` et `Créer un lot d’exercices` sont disponibles.
Ce sont des fonctions IA et elles nécessitent du **solde IA**.

### Comment utiliser l’`Assistant de résolution` ?
Activez **Assistant de résolution** dans `Réglages > Aide à l'étude`. Il apparaît ensuite en haut de l’écran de note.

Déroulement :

- choisissez **Assistant de résolution** en haut de l’écran de note
- entourez le problème avec l’Apple Pencil en formant une zone fermée
- confirmez la zone sélectionnée puis choisissez **Résoudre**
- consultez la réponse et l’explication

Depuis l’écran de résultat, vous pouvez copier ou partager la réponse et l’explication.

La fonction est surtout prévue pour les formules, les calculs et les questions courtes.
Les longs textes, réponses libres et problèmes centrés sur des figures peuvent ne pas être pris en charge.

Son utilisation nécessite du **solde IA**. Si votre solde IA est insuffisant, vous pouvez en ajouter dans l’app.

### Comment utiliser `Créer un lot d’exercices` ?
Ouvrez **Créer un lot d’exercices** depuis **Plus**.

Son utilisation nécessite du **solde IA**.

Déroulement :

- choisissez les pages cibles avec **Choisir les pages**
- lancez **Créer un lot d’exercices**
- examinez les propositions avec **Ajouter** et **Ignorer**
- enregistrez-les avec **Enregistrer le lot**

Après l’enregistrement, vous pouvez poursuivre via **Réviser maintenant**.  
Pour y revenir plus tard, basculez l’accueil sur **Exercices** puis ouvrez-les depuis la liste.

Les lots d’exercices peuvent être supprimés depuis l’accueil, mais ils ne vont pas à la corbeille et ne peuvent pas être restaurés.

### Qu’est-ce que le solde IA ?
Le solde IA est le solde commun utilisé par `Résolution entourée`, `Génération de lots d’exercices` et `Résumé IA`.
S’il est épuisé, vous pouvez ajouter du solde IA depuis l’écran des offres dans l’app.

Le solde IA est géré avec un identifiant utilisé pour vérifier les achats et le solde. Cet identifiant ne contient pas d’information permettant de vous identifier directement, comme votre nom, votre adresse e-mail, votre identifiant Apple ou le contenu de vos notes.

---

## Données et stockage

### Où mes données sont-elles enregistrées ?
À l’intérieur de l’app sur votre appareil.

### L’app envoie-t-elle des données de diagnostic ou de plantage ?
Oui.
Pour améliorer la stabilité et analyser les problèmes, Uni:Note peut envoyer des données de diagnostic et de plantage via Firebase Crashlytics.

Il s’agit d’informations techniques comme la version de l’app, la version de l’OS, une catégorie générale d’appareil, la classe de taille d’écran, le type d’opération, des tranches de comptage approximatives et des catégories d’erreur sûres.

Le contenu des notes, l’écriture manuscrite, les images, les PDF, les enregistrements, les résultats OCR, les noms de notes, les noms de matières, les noms de fichiers, les noms d’utilisateur et les adresses e-mail ne sont pas envoyés.

Uni:Note ne collecte pas d’événements d’utilisation avec Google Analytics for Firebase.

### Une synchronisation automatique est-elle disponible ?
Pas pour le moment.  
Si nécessaire, utilisez `Réglages > Sauvegarde`.

### Une fonction de sauvegarde est-elle disponible ?
Oui.  
Dans `Réglages > Sauvegarde`, vous pouvez utiliser :

- `Mettre à jour la sauvegarde facile`
- `Restaurer depuis la sauvegarde facile`
- `Exporter la sauvegarde`
- `Restaurer depuis un fichier`

La `sauvegarde facile` est l’option d’enregistrement et de restauration basée sur iCloud. La sauvegarde par fichier reste également disponible.

### La `sauvegarde facile` est-elle disponible pour tout le monde ?
Non.  
La `sauvegarde facile` est disponible avec Premium.

Même sans Premium, vous pouvez toujours utiliser `Exporter la sauvegarde` et `Restaurer depuis un fichier`.

### Puis-je utiliser l’app immédiatement après une restauration ?
Après la restauration, fermez l’app une fois puis ouvrez-la de nouveau.  
Au prochain lancement, l’accueil s’affichera.

---

## Réglages

### Quels réglages sont disponibles ?
Vous pouvez principalement modifier :

- `Modèle par défaut`
- `Couleur de base par défaut`
- `Ouvrir l’accueil` ou `Ouvrir la dernière note`
- `Réduire automatiquement la palette`
- `Fonction de mémorisation`
- `Assistant de résolution`
- `Langue de transcription`
- format par défaut du Résumé IA pour Études ou Réunion
- `Libellé des matières`
- exiger la biométrie pour retirer la protection
- `Mode gaucher`
- `En-tête / Pied de page`
- `Fond de l’export PDF`
- `Langue`

### Puis-je modifier le libellé des matières ?
Oui.  
Dans les réglages, sous `Libellé des matières`, vous pouvez choisir **Matière / Cahier / Groupe / Catégorie**.

### Que puis-je modifier dans le mode gaucher ?
Vous pouvez ajuster la position initiale de la palette, la position de la ligne rouge de marge sur le papier ligné et la position d’insertion des PDF.

### Puis-je changer la langue ?
Oui.  
Vous pouvez la changer depuis `Réglages > Langue`.

### Où puis-je ouvrir la page du mode d’emploi ?
Ouvrez `Réglages > Support > Mode d’emploi`.
