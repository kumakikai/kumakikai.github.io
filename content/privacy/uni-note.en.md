---
title: "Privacy Policy (Uni:Note)"
description: "Privacy policy for Uni:Note."
lastmod: 2026-09-08
---

## 1. Introduction {#introduction}

{{< document-copy "privacyIntroduction" >}}

{{< guide-anchor "1-information-we-collect" >}}

## 2. Information we handle {#information}

No separate app account or login is required. Information you enter or attach to notes or support inquiries may contain personal information.

Notes, handwriting data, images, PDFs, recording audio, transcriptions, and settings created in the app are stored on the user's device.

{{< guide-anchor "2-handling-of-photos-and-files" >}}

### Photos and files

The app allows users to insert images, PDFs, and other files that they explicitly select into their notes.

The app may also access a storage location or backup file selected by the user for backup creation or restoration.

Ordinary photo and PDF attachment operations are processed on your device. If you run an AI feature, the external processing described in the AI section applies.

{{< guide-anchor "5-premium-features-purchase-information-and-ai-balance" >}}

### Purchases and AI Balance

Purchase verification uses Apple transaction identifiers and signed transaction information. AI Balance uses related identifiers. These are separate from an account registered with a name or email address, but allow purchases and usage to be associated with the same user.

### Support inquiries

{{< document-copy "privacyInquiries" >}}

## 3. How we use information {#purposes}

We use the information needed for each feature to store and display notes and attachments, back up and restore data, process selected content with AI, manage purchases and AI Balance, prevent duplicate credits and investigate problems.

{{< guide-anchor "3-backup-and-storage" >}}

## 4. Storage and management {#storage}

Ordinary data such as notes and attachments is stored on your device. Server-side information associated with AI processing, purchases and AI Balance is handled as described below.

When the backup feature is used, the backup file is saved to the location selected by the user.

If you use an external storage destination such as iCloud Drive, please review the policy of that service provider.

Recording audio is included in backups only when the user turns on **Include recording audio in backups** while creating a backup.

When you use AI features, requests are processed on AWS servers used by us. Generated results may be cached briefly to prevent duplicate processing when a request is retried. Purchase and AI Balance identifiers, transactions, credit and usage history, and technical information such as processing status and usage are managed on servers to verify purchases, manage balances and investigate problems. Generated results may contain information derived from your input.

{{< guide-anchor "8-provision-of-personal-information-to-third-parties" >}}

## 5. External services and disclosure {#external-services}

We use Amazon Web Services (AWS) for AI requests and balance/transaction management, Google Gemini for AI generation and analysis, Google Firebase Crashlytics for diagnostics, and Apple App Store for purchases. Backups in an external destination you choose, including iCloud Easy Backup, are handled by that storage provider. Information is processed as needed for these features and may also be disclosed when required by law. We use Google Forms and Gmail to receive and respond to support inquiries.

For each service’s information handling, see [AWS data privacy](https://aws.amazon.com/compliance/data-privacy/), [Gemini API processing terms](https://ai.google.dev/gemini-api/terms), [Firebase privacy and security](https://firebase.google.com/support/privacy) and [Apple’s privacy policy](https://www.apple.com/legal/privacy/).

{{< guide-anchor "7-advertising-and-analytics-tools" >}}

### Advertising and analytics

The app does not use advertising SDKs.

The app does not collect usage events with Google Analytics for Firebase. Firebase is used for diagnostics and crash analysis through Crashlytics.

{{< guide-anchor "6-diagnostics-and-crash-data" >}}

### Diagnostics

The exclusions in this section apply to diagnostic information sent to Firebase Crashlytics. They are separate from AI requests or support information you choose to send.

To improve app stability and investigate issues, the app may send diagnostic data and crash information using Firebase Crashlytics.

The information that may be sent is technical information such as app version, build number, OS version, broad device category, screen size class, operation type, coarse buckets for page count, attachment count, PDF page count, and backup size, safe error category, error domain, and error code.

This also includes information handled by the Firebase SDK as standard, such as app installation identifiers and stack traces recorded when a crash occurs.

The diagnostic fields we configure for Crashlytics do not include note body content, handwriting content, image content, PDF content, OCR results, recording content, note names, subject names, file names, real file paths, user names or email addresses.

{{< guide-anchor "4-study-assistant-and-ai-features" >}}

## 6. AI and audio processing {#ai}

When users use study assistant features such as `Problem Solver Assistant` and `Create Practice Set`, selected note content, handwriting, images, or parts of PDFs may be sent to external AI services to generate answers or practice question candidates.

For AI Summary of recordings, transcription text from the recordings selected by the user may be sent to an external AI service. The recording audio file itself is not used for AI Summary.

This information is processed only to the extent necessary to provide these features.

If your notes contain personal or sensitive information, please use these features at your own discretion.

AI summaries send the selected transcript together with recording titles, identifiers and dates, and, depending on the operation, related information such as notebook names or language. AI requests reach Google Gemini through our AWS servers.

Live transcription uses Apple speech recognition. A supported speech model may need to be downloaded if it is not installed.

## 7. Managing and deleting your data {#data-management}

Subjects and notes can be restored from Trash until cleanup after 30 days or manual permanent deletion. Deleted pages and practice sets cannot be restored. Deleting local data does not automatically delete exported zip files or backups in iCloud or other storage; manage these at their destination. Removing the app does not itself delete purchase or AI Balance records managed on servers.

{{< document-copy "privacyRights" >}}

{{< guide-anchor "9-changes-to-this-privacy-policy" >}}

## 8. Changes to this policy {#changes}

{{< document-copy "privacyChanges" >}}

{{< guide-anchor "10-contact" >}}

## 9. Contact {#inquiries}

In `Settings > Support`, the app provides options to send feedback by form, contact by email, and copy support info.
Copied support info includes technical details such as app version, build number, OS version, device name, and app language setting. It does not include note text, handwriting, images, PDFs, recordings, note names, or subject names.

{{< document-contact >}}
