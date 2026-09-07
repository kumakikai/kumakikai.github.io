---
title: "Politique de confidentialité (Uni:Note)"
description: "Politique de confidentialité pour Uni:Note."
lastmod: 2026-09-08
---

## 1. Introduction {#introduction}

{{< document-copy "privacyIntroduction" >}}

{{< guide-anchor "1-informations-collectées" >}}

## 2. Informations traitées {#information}

Aucun compte propre à l’app ni connexion n’est requis. Les informations saisies ou jointes aux notes ou demandes de support peuvent contenir des données personnelles.

Les notes, les données manuscrites, les images, les PDF, l'audio des enregistrements, les transcriptions et les réglages créés dans l'application sont stockés sur l'appareil de l'utilisateur.

{{< guide-anchor "2-traitement-des-photos-et-des-fichiers" >}}

### Photos et fichiers

L'application permet aux utilisateurs d'insérer dans leurs notes des images, PDF et autres fichiers qu'ils sélectionnent explicitement.

L'application peut également accéder à un emplacement de stockage ou à un fichier de sauvegarde choisi par l'utilisateur afin de créer ou restaurer une sauvegarde.

L’ajout ordinaire de photos et PDF est traité sur l’appareil. Lorsque vous lancez une fonction IA, le traitement externe décrit dans la section IA s’applique.

{{< guide-anchor "5-fonctions-premium-informations-dachat-et-solde-ia" >}}

### Achats et solde IA

La vérification des achats utilise les identifiants de transaction Apple et les informations signées des transactions. Le solde IA utilise des identifiants associés. Ils ne constituent pas un compte inscrit avec nom ou e-mail, mais permettent de rattacher achats et utilisation à une même personne.

### Demandes d’assistance

{{< document-copy "privacyInquiries" >}}

## 3. Utilisation des informations {#purposes}

Les informations nécessaires servent à stocker et afficher notes et documents, sauvegarder et restaurer, traiter les contenus sélectionnés par IA, gérer achats et solde IA, éviter les doubles crédits et analyser les problèmes.

{{< guide-anchor "3-sauvegarde-et-stockage" >}}

## 4. Stockage et gestion {#storage}

Les données ordinaires, comme les notes et les pièces jointes, sont stockées sur votre appareil. Les informations conservées sur les serveurs pour les traitements IA, les achats et le solde IA sont traitées comme indiqué ci-dessous.

Lorsque la fonction de sauvegarde est utilisée, le fichier de sauvegarde est enregistré à l'emplacement choisi par l'utilisateur.

Si vous utilisez un service de stockage externe comme iCloud Drive, veuillez consulter la politique de ce fournisseur.

L'audio des enregistrements est inclus dans les sauvegardes uniquement lorsque l'utilisateur active **Inclure l'audio des enregistrements dans les sauvegardes** lors de la création d'une sauvegarde.

Les requêtes IA sont traitées sur les serveurs AWS que nous utilisons. Les résultats peuvent être brièvement mis en cache afin d’éviter un traitement en double lors d’une nouvelle tentative. Les identifiants d’achat et de solde IA, transactions, historiques de crédit et de consommation, états et données techniques d’utilisation sont gérés sur des serveurs pour vérifier les achats, gérer le solde et analyser les problèmes. Les résultats peuvent contenir des informations dérivées de vos saisies.

{{< guide-anchor "8-communication-des-données-personnelles-à-des-tiers" >}}

## 5. Services externes et communication {#external-services}

Nous utilisons Amazon Web Services (AWS) pour les requêtes IA et la gestion du solde et des transactions, Google Gemini pour la génération et l’analyse IA, Google Firebase Crashlytics pour les diagnostics, et l’App Store Apple pour les achats. Les sauvegardes vers une destination externe choisie, y compris iCloud, sont traitées par son fournisseur. Les informations sont traitées selon les besoins des fonctions et peuvent être communiquées lorsque la loi l’exige. Nous utilisons Google Forms et Gmail pour recevoir les demandes d’assistance et y répondre.

Pour le traitement des informations par chaque service, consultez la [confidentialité des données AWS](https://aws.amazon.com/compliance/data-privacy/), les [conditions de traitement de l’API Gemini](https://ai.google.dev/gemini-api/terms), la [confidentialité et la sécurité Firebase](https://firebase.google.com/support/privacy) et la [politique de confidentialité Apple](https://www.apple.com/legal/privacy/).

{{< guide-anchor "7-outils-publicitaires-et-analytiques" >}}

### Publicité et analyse

L’application n’utilise pas de SDK publicitaire.

L'application ne collecte pas d'événements d'utilisation avec Google Analytics for Firebase. Firebase est utilisé pour les diagnostics et l'analyse des plantages via Crashlytics.

{{< guide-anchor "6-données-de-diagnostic-et-de-plantage" >}}

### Diagnostics

Les exclusions de cette section concernent les diagnostics envoyés à Firebase Crashlytics. Les requêtes IA et les informations que vous envoyez au support sont distinctes.

Pour améliorer la stabilité de l'application et analyser les problèmes, l'application peut envoyer des données de diagnostic et de plantage via Firebase Crashlytics.

Les informations susceptibles d'être envoyées sont des informations techniques comme la version de l'app, le numéro de build, la version de l'OS, une catégorie générale d'appareil, la classe de taille d'écran, le type d'opération, des tranches approximatives pour le nombre de pages, de pièces jointes, de pages PDF et la taille de sauvegarde, une catégorie d'erreur sûre, le domaine d'erreur et le code d'erreur.

S’y ajoutent les informations traitées par défaut par le SDK Firebase, notamment les identifiants d’installation de l’app et les traces de pile enregistrées lors d’un plantage.

Les champs de diagnostic que nous configurons pour Crashlytics ne contiennent pas le texte des notes, le contenu manuscrit, les images, les PDF, les résultats OCR, les enregistrements, les noms de notes, de matières ou de fichiers, les chemins réels des fichiers, les noms d’utilisateur ni les adresses e-mail.

{{< guide-anchor "4-fonctions-daide-à-létude-et-dia" >}}

## 6. Traitement de l’IA et de l’audio {#ai}

Lorsque vous utilisez des fonctions d'aide à l'étude telles que `Assistant de résolution` et `Créer un lot d'exercices`, une partie de la note sélectionnée, du contenu manuscrit, des images ou des PDF peut être envoyée à des services d'IA externes afin de générer des réponses ou des propositions de questions.

Pour le Résumé IA des enregistrements, le texte de transcription des enregistrements sélectionnés par l'utilisateur peut être envoyé à un service d'IA externe. Le fichier audio de l'enregistrement lui-même n'est pas utilisé pour le Résumé IA.

Ces informations sont traitées uniquement dans la mesure nécessaire pour fournir ces fonctions.

Si vos notes contiennent des informations personnelles ou sensibles, veuillez utiliser ces fonctions à votre discrétion.

Les résumés IA transmettent la transcription sélectionnée avec les titres, identifiants et dates des enregistrements et, selon le traitement, des informations associées comme le nom des notes ou la langue. Les requêtes passent par nos serveurs AWS vers Google Gemini.

La transcription en direct utilise la reconnaissance vocale Apple. Un modèle compatible peut nécessiter un téléchargement s’il n’est pas installé.

## 7. Gérer et supprimer vos données {#data-management}

Les matières et notes peuvent être restaurées depuis la corbeille jusqu’au nettoyage après 30 jours ou à leur suppression définitive manuelle. Les pages et lots supprimés ne sont pas récupérables. La suppression locale n’efface pas automatiquement les zip exportés ou les sauvegardes iCloud ; gérez-les à leur destination. Supprimer l’app n’efface pas automatiquement les données d’achat et de solde IA gérées sur les serveurs.

{{< document-copy "privacyRights" >}}

{{< guide-anchor "9-modifications-de-cette-politique-de-confidentialité" >}}

## 8. Modifications de cette politique {#changes}

{{< document-copy "privacyChanges" >}}

{{< guide-anchor "10-contact" >}}

## 9. Contact {#inquiries}

Dans `Réglages > Assistance`, l’app propose l’envoi par formulaire, le contact par e-mail et la copie des informations d’assistance.
Les informations d’assistance copiées incluent des informations techniques comme la version de l’app, le numéro de build, la version de l’OS, le nom de l’appareil et la langue de l’app. Elles n’incluent pas le texte des notes, l’écriture manuscrite, les images, les PDF, les enregistrements, les noms de notes ou les noms de matières.

{{< document-contact >}}
