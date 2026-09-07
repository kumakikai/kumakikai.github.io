---
title: "Datenschutzerklärung (Uni:Note)"
description: "Datenschutzerklärung für Uni:Note."
lastmod: 2026-09-08
---

## 1. Einführung {#introduction}

{{< document-copy "privacyIntroduction" >}}

{{< guide-anchor "1-erhobene-informationen" >}}

## 2. Verarbeitete Informationen {#information}

Ein eigenes App-Konto oder Login ist nicht erforderlich. Inhalte, die Sie in Notizen oder Supportanfragen eingeben oder anhängen, können personenbezogene Daten enthalten.

In der App erstellte Notizen, Handschrift-Daten, Bilder, PDFs, Aufnahme-Audio, Transkriptionen und Einstellungen werden auf dem Gerät des Nutzers gespeichert.

{{< guide-anchor "2-umgang-mit-fotos-und-dateien" >}}

### Fotos und Dateien

Die App ermöglicht es Nutzern, Bilder, PDFs und andere Dateien, die sie ausdrücklich auswählen, in ihre Notizen einzufügen.

Außerdem kann die App für die Erstellung oder Wiederherstellung von Backups auf einen vom Nutzer ausgewählten Speicherort oder eine Sicherungsdatei zugreifen.

Das gewöhnliche Einfügen von Fotos und PDFs wird auf dem Gerät verarbeitet. Bei Nutzung einer KI-Funktion gilt die im KI-Abschnitt beschriebene externe Verarbeitung.

{{< guide-anchor "5-premium-funktionen-kaufinformationen-und-ki-guthaben" >}}

### Käufe und KI-Guthaben

Zur Kaufprüfung verwenden wir Apple-Transaktionskennungen und signierte Transaktionsdaten; das KI-Guthaben nutzt zugehörige Kennungen. Diese sind kein mit Name oder E-Mail registriertes Konto, ermöglichen aber die Zuordnung von Käufen und Nutzung zu derselben Person.

### Supportanfragen

{{< document-copy "privacyInquiries" >}}

## 3. Verwendungszwecke {#purposes}

Die jeweils nötigen Informationen dienen dem Speichern und Anzeigen von Notizen und Anhängen, Backups und Wiederherstellung, der KI-Verarbeitung ausgewählter Inhalte, der Verwaltung von Käufen und KI-Guthaben, dem Verhindern doppelter Gutschriften und der Fehleranalyse.

{{< guide-anchor "3-backup-und-speicherung" >}}

## 4. Speicherung und Verwaltung {#storage}

Gewöhnliche Daten wie Notizen und Anhänge werden auf Ihrem Gerät gespeichert. Serverseitige Informationen zur KI-Verarbeitung sowie zu Käufen und KI-Guthaben werden wie unten beschrieben behandelt.

Wenn die Backup-Funktion verwendet wird, wird die Sicherungsdatei an dem vom Nutzer gewählten Speicherort abgelegt.

Wenn Sie ein externes Speichermedium wie iCloud Drive verwenden, prüfen Sie bitte die Richtlinien des jeweiligen Dienstanbieters.

Aufnahme-Audio wird nur dann in Backups aufgenommen, wenn der Nutzer beim Erstellen eines Backups **Aufnahme-Audio in Backups einschließen** aktiviert.

KI-Anfragen werden auf von uns genutzten AWS-Servern verarbeitet. Ergebnisse können kurzfristig zwischengespeichert werden, um bei erneuten Anfragen doppelte Verarbeitung zu vermeiden. Kauf- und Guthabenkennungen, Transaktionen, Gutschriften- und Verbrauchsverläufe sowie technische Angaben zu Status und Nutzung werden für Kaufprüfung, Guthabenverwaltung und Fehleranalyse auf Servern verwaltet. Ergebnisse können aus Eingaben abgeleitete Informationen enthalten.

{{< guide-anchor "8-weitergabe-personenbezogener-daten-an-dritte" >}}

## 5. Externe Dienste und Weitergabe {#external-services}

Wir nutzen Amazon Web Services (AWS) für KI-Anfragen sowie Guthaben- und Transaktionsverwaltung, Google Gemini für KI-Generierung und -Analyse, Google Firebase Crashlytics für Diagnosen und den Apple App Store für Käufe. Backups an gewählten externen Speicherorten, einschließlich iCloud, verarbeitet der jeweilige Anbieter. Daten werden im für die Funktionen nötigen Umfang verarbeitet und gegebenenfalls aufgrund gesetzlicher Pflichten weitergegeben. Für den Empfang und die Beantwortung von Supportanfragen nutzen wir Google Forms und Gmail.

Zum Umgang mit Informationen der einzelnen Dienste siehe [AWS-Datenschutz](https://aws.amazon.com/compliance/data-privacy/), [Verarbeitungsbedingungen der Gemini API](https://ai.google.dev/gemini-api/terms), [Datenschutz und Sicherheit bei Firebase](https://firebase.google.com/support/privacy) und [Apples Datenschutzrichtlinie](https://www.apple.com/legal/privacy/).

{{< guide-anchor "7-werbe--und-analysetools" >}}

### Werbung und Analyse

Die App verwendet keine Werbe-SDKs.

Die App erfasst keine Nutzungsereignisse mit Google Analytics for Firebase. Firebase wird über Crashlytics für Diagnose- und Absturzanalysen verwendet.

{{< guide-anchor "6-diagnose--und-absturzdaten" >}}

### Diagnosedaten

Die hier genannten Ausschlüsse betreffen Diagnosedaten für Firebase Crashlytics. KI-Anfragen und selbst gesendete Supportinformationen sind davon getrennt.

Zur Verbesserung der App-Stabilität und zur Untersuchung von Problemen kann die App Diagnose- und Absturzinformationen mit Firebase Crashlytics senden.

Zu den möglicherweise gesendeten Informationen gehören technische Daten wie App-Version, Build-Nummer, OS-Version, grobe Gerätekategorie, Bildschirmgrößenklasse, Vorgangsart, grobe Bereiche für Seitenanzahl, Anhänge, PDF-Seiten und Backup-Größe, sichere Fehlerkategorie, Fehlerdomain und Fehlercode.

Hinzu kommen standardmäßig vom Firebase-SDK verarbeitete Informationen, etwa Kennungen der App-Installation und bei Abstürzen erfasste Stacktraces.

Die von uns für Crashlytics eingerichteten Diagnosefelder enthalten keine Notizinhalte, Handschriftinhalte, Bildinhalte, PDF-Inhalte, OCR-Ergebnisse, Aufnahmeinhalte, Notiznamen, Fachnamen, Dateinamen, tatsächlichen Dateipfade, Benutzernamen oder E-Mail-Adressen.

{{< guide-anchor "4-lernhilfe--und-ki-funktionen" >}}

## 6. KI- und Audioverarbeitung {#ai}

Bei der Nutzung von Lernhilfe-Funktionen wie `Aufgabenassistent` und `Aufgabenset erstellen` können ausgewählte Teile von Notizen, Handschrift, Bildern oder PDFs an externe KI-Dienste gesendet werden, um Antworten oder Aufgabenvorschläge zu erzeugen.

Für die KI-Zusammenfassung von Aufnahmen kann der Transkriptionstext der vom Nutzer ausgewählten Aufnahmen an einen externen KI-Dienst gesendet werden. Die Aufnahme-Audiodatei selbst wird nicht für die KI-Zusammenfassung verwendet.

Diese Informationen werden nur im zur Bereitstellung dieser Funktionen erforderlichen Umfang verarbeitet.

Wenn Ihre Notizen personenbezogene oder sensible Informationen enthalten, nutzen Sie diese Funktionen bitte nach eigenem Ermessen.

KI-Zusammenfassungen übermitteln ausgewählte Transkripte samt Aufnahmetiteln, Kennungen und Zeitangaben sowie je nach Verarbeitung etwa Notiznamen oder Sprache. Die Anfragen gelangen über unsere AWS-Server zu Google Gemini.

Die laufende Transkription verwendet Apples Spracherkennung. Ein unterstütztes Sprachmodell muss gegebenenfalls heruntergeladen werden.

## 7. Daten verwalten und löschen {#data-management}

Fächer und Notizen können bis zur Bereinigung nach 30 Tagen oder manuellen endgültigen Löschung aus dem Papierkorb wiederhergestellt werden. Gelöschte Seiten und Aufgabensets sind nicht wiederherstellbar. Lokales Löschen entfernt exportierte zip-Dateien oder iCloud-Backups nicht automatisch; Verwalten Sie diese am jeweiligen Speicherort. Das Entfernen der App löscht nicht automatisch serverseitige Kauf- und Guthabendaten.

{{< document-copy "privacyRights" >}}

{{< guide-anchor "9-änderungen-dieser-datenschutzerklärung" >}}

## 8. Änderungen dieser Erklärung {#changes}

{{< document-copy "privacyChanges" >}}

{{< guide-anchor "10-kontakt" >}}

## 9. Kontakt {#inquiries}

Unter `Einstellungen > Support` bietet die App Optionen zum Senden per Formular, zur Kontaktaufnahme per E-Mail und zum Kopieren von Support-Informationen.
Kopierte Support-Informationen enthalten technische Angaben wie App-Version, Build-Nummer, OS-Version, Gerätename und Spracheinstellung der App. Notizinhalte, Handschrift, Bilder, PDFs, Aufnahmen, Notiznamen oder Fachnamen sind nicht enthalten.

{{< document-contact >}}
