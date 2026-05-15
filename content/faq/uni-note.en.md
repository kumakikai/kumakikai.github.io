---
title: "FAQ (Uni:Note)"
description: "Frequently asked questions about Uni:Note."
---

## Basics

### What kind of app is Uni:Note?
It is a handwriting note app for iPad.  
It is designed around writing with Apple Pencil and organizing notes by subject.

### Which devices are supported?
iPad only.

### Are there limits on the Free plan?
Yes.  
In the current app, the Free plan is limited to **up to 10 subjects** and **up to 6 notes per subject**.

Premium removes the subject and note count limits and unlocks Move Selection, Recording, and Easy Backup.

### Which languages are supported?
The app currently supports:

- Japanese
- English
- Korean
- German
- Traditional Chinese
- French

### What changed in v3.0.0?
v3.0.0 is a major update for study support and notebook tools.

- Restored `Problem Solver Assistant` and made it available from the top of the note screen
- Added `Ruler`
- Added `Move Selection`
- Fully redesigned `Memorization Feature` as sticky-style markers
- Added `Recording`, real-time transcription, and AI Summary
- Added subject reordering on Home and note reordering in Note List
- Added diagnostics and crash analysis with Firebase Crashlytics

Diagnostic and crash data does not include note contents, handwriting, subject names, attachments, images, PDFs, or recording contents.

### Can I use it with `Split View` or `Slide Over`?
Yes.  
Uni:Note supports iPad multiwindow modes such as `Split View` and `Slide Over`.

A general way is to open Uni:Note first, show the Dock, then drag another app or Uni:Note from the Dock to the side for `Split View`, or place it as a floating panel for `Slide Over`.

The exact UI and labels may differ slightly depending on your iPadOS version.

### Can I open two Uni:Note windows at the same time?
Yes.  
Uni:Note supports multiple windows.

With one Uni:Note window already open, show the Dock, press and hold the Uni:Note icon, and choose the option for opening a new window.

After opening the second window, place it side by side for `Split View` or float it as `Slide Over`.

### Is Apple Pencil required?
Handwriting is designed for Apple Pencil.  
Finger input is mainly used for scrolling and handling photos, document photos, and PDFs.

### Do I need to log in or create an account?
No.

---

## Notes and pages

### Is a note title required?
No.  
If you create a note with the title left blank, today's date is used as the note name.

### What is the title prompt shown when I first open a new subject?
It is the title of the first note.  
If you leave it blank and choose **OK** or **Start Writing**, today's date becomes the title.

If you go back without confirming anything, the in-progress first note is not kept.

### What can I choose when I create a subject?
You can choose the following:

- `Subject name`
- paper style: ruled / vertical / grid / plain
- `Paper Color`
- cover color
- `Use as Portrait Notebook` when `Vertical` is selected

### What is a portrait notebook?
It is a note layout available when you create a subject with `Vertical`.  
If you turn on **Use as Portrait Notebook**, the note shows a spread-like layout in landscape, one page at a time in portrait, and scrolls horizontally.

The note orientation cannot be changed after creation.

### Can I separate notes within the same subject?
Yes.  
You can add one from **New Note** in **Note List**.

You can also reorder notes inside **Note List**.

### How are new pages added?
When you start writing on the last page, the next page is added automatically.

### What is the maximum number of pages in a note?
One note can have up to `150` pages.  
Once it reaches `150`, no more pages can be added. PDF attachment also cannot add pages beyond that limit. If needed, create another note in the same subject.

### Can I zoom?
Yes.  
On the note screen, you can zoom in or out with a two-finger pinch gesture.

### Can I move handwriting by circling a range?
Yes.
Use **Move Selection** at the top of the note screen to select and move handwriting strokes together.

Basic flow:

- Choose **Move Selection**
- Circle the handwriting you want to move with Apple Pencil
- Drag the selected handwriting to move it

Any line that is even partly inside the enclosed area is selected as a whole. This applies to handwriting strokes; photos, PDFs, and Sticky Markers are handled separately.
**Move Selection** is a Premium feature.

### Can I delete a page?
Yes.  
You can delete it by pressing and holding the target page in **Pages**.

However, if a note has only one page, the page itself is kept and only its content is cleared.

### Can I protect a note?
Yes.  
When you choose **Protect** in **Note List**, the note becomes read-only. You can also require biometrics to remove protection.

### Can I edit a subject?
Yes.  
Press and hold the subject on Home and open **Edit**.

You can change:

- `Subject name`
- paper style
- `Paper Color`
- cover color

The note orientation cannot be changed after creation.  
Note titles can still be changed from **Note List**.

You can also reorder subjects on Home.

### What can be restored from Trash?
Subjects and notes shown in the note list.  
**Trash** groups deleted items by subject, and tapping a subject shows the notes inside it.

Even if a subject is deleted, you can restore the whole subject or restore only individual notes.  
Deleted pages do not go to Trash and are removed immediately.

---

## Photos and PDFs

### Can I insert photos?
Yes.  
You can insert photos one at a time with **Attach Photo**. After inserting, you can move or resize them, and double-tap to lock or unlock them.

### Can I attach a photo as a document?
Yes.  
Choose **Attach Photo as Document** from **More** to pick a photo from Camera or Library, adjust it in the correction UI, and place it on the page as a document.

After placing it, you can double-tap to lock or unlock it and adjust its position and size with your fingers.

### Can I insert PDFs?
Yes.  
Choose **Attach PDF** from **More**.

- You can select one or more pages from a PDF file
- You can turn on **Split Spread** to split a spread in the center
- You can attach multiple PDF pages in one action

After placing it, you can double-tap to lock or unlock it and adjust its position and size with your fingers.

### Can I export PDFs?
Yes.  
Choose **Export PDF** from **More** and export **This Note Only** or the entire subject as PDF.

---

## Recording and Transcription

### Can I use recording?
Yes.
Use the **Recording** button at the top of the note screen to open the recording panel.

- Start / pause / stop recording
- Playback / seek / change playback speed
- Rename recordings
- Lock or unlock recordings
- Delete recordings
- Share recording audio

Recording, playback, and viewing transcriptions are **Premium** features.
One note can keep up to `5` recordings.
Each recording file can be up to 30 minutes long. When a recording reaches 30 minutes, Uni:Note automatically saves that recording and starts the next one.
Automatically split recordings count toward the limit of `5` recordings per note.
If you return to Uni:Note Home or the iPad goes to sleep while recording, the recording ends and is saved at that point.
Doing this during recording may corrupt the recording data. Stop and save the recording before leaving the note or putting the iPad to sleep.

### Can I use transcription and AI Summary?
On supported devices, Uni:Note can show real-time transcription while recording.
Based on Apple's transcription-compatible models, real-time transcription and AI Summary are available on the following models running iPadOS 26 or later: iPad mini (6th generation or later), iPad (10th generation or later), iPad Air (4th generation or later), iPad Pro 11-inch (3rd generation or later), iPad Pro 12.9-inch (5th generation or later), and iPad Pro 13-inch (M4 or later).

AI Summary is generated from the transcription text already created on the device.
Audio files are not sent for AI Summary.

AI Summary can generate a study or meeting-style reconstructed note from the selected recording transcripts. If multiple recordings are selected, Uni:Note keeps the recording boundaries. Before running it, you can check the number of recordings, character count, and estimated AI usage.

AI Summary requires **AI Balance**.

### Are recordings included in backups?
Standard backups include recording metadata and transcriptions.
Recording audio files (m4a) are included in both **Export Backup** and `Easy Backup` only when **Include recording audio in backups** is turned on.

---

## Study Support

### What is `Memorization Feature`?
Turn on **Memorization Feature** in `Settings > Study Support` to use **Sticky Marker** on the note screen.

- Hide parts with **Sticky Marker**
- Each stroke is saved as an independent sticky marker
- Tap a sticky marker with your finger to switch between transparent and opaque
- Press and hold a sticky marker with your finger, then use the delete button that appears

### Can I show or hide all memorization markers for a page at once?
No.  
In v3.0.0, the old page-wide open / close behavior has been replaced with per-sticky transparency control.

If a page has old memorization markers from an earlier version, they are migrated to sticky markers when the page is opened.

### What is the current status of the study support features?
`Problem Solver Assistant` and `Create Practice Set` are both available.
Both are AI features and require **AI Balance**.

### How do I use `Problem Solver Assistant`?
Turn on **Problem Solver Assistant** in `Settings > Study Support`. It then appears at the top of the note screen.

Basic flow:

- Choose **Problem Solver Assistant** at the top of the note screen
- Circle the problem with Apple Pencil using a closed shape
- Confirm the selected area and choose **Solve**
- Review the answer and explanation

From the result screen, you can copy or share the answer and explanation.

It is mainly intended for formulas, calculations, and short questions.
Long reading passages, free-response questions, and figure-heavy questions may not be supported.

Using it requires **AI Balance**. If your AI Balance is insufficient, you can add more in the app.

### How do I use `Create Practice Set`?
Open **Create Practice Set** from **More**.

Using it requires **AI Balance**.

Basic flow:

- Choose target pages with **Choose Pages**
- Start with **Create Practice Set**
- Review candidates with **Add** and **Reject**
- Save them with **Save Practice Set**

After saving, you can continue from **Review now**.  
To revisit them later, switch Home to **Practice Sets** and open them from the list there.

Practice sets can be deleted from Home, but they do not go to Trash and cannot be restored.

### What is AI Balance?
AI Balance is the shared balance used by `Circle Solve`, `Practice Set Generation`, and `AI Summary`.
If it runs out, you can add AI Balance from the plan screen in the app.

AI Balance is managed with an identifier used to verify purchases and balance. This identifier does not contain directly identifying information such as your name, email address, Apple ID, or note contents.

---

## Data and storage

### Where is my data stored?
Inside the app on your device.

### Does the app send diagnostics or crash information?
Yes.
To improve stability and investigate issues, Uni:Note may send diagnostic data and crash information using Firebase Crashlytics.

The data is technical information such as app version, OS version, broad device category, screen size class, operation type, coarse count buckets, and safe error categories.

It does not include note body content, handwriting, image content, PDF content, recording contents, OCR results, note names, subject names, file names, user names, or email addresses.

Uni:Note does not collect usage events with Google Analytics for Firebase.

### Is automatic sync available?
Not at this time.  
If needed, use `Settings > Backup`.

### Is backup available?
Yes.  
In `Settings > Backup`, you can use:

- `Update Easy Backup`
- `Restore from Easy Backup`
- `Export Backup`
- `Restore from File`

`Easy Backup` is the iCloud-based save and restore option. File-based backup remains available as well.

### Is `Easy Backup` available for everyone?
No.  
`Easy Backup` is available with Premium.

Even without Premium, you can still use `Export Backup` and `Restore from File`.

### Can I use the app immediately after restoring?
After restoring, close the app once and open it again.  
The next launch will show Home.

---

## Settings

### What settings are available?
You can mainly change the following:

- `Default Template`
- `Default Base Color`
- `Open Home` or `Open Previous Notebook`
- `Auto-collapse Tool Palette`
- `Memorization Feature`
- `Problem Solver Assistant`
- `Recording Transcription Language`
- default AI Summary format for Study or Meeting
- `Subject Name`
- `Require Biometrics to Remove Protection`
- `Left-Handed Mode`
- `Header / Footer`
- `PDF Export Background`
- `Language`

### Can I change the subject label?
Yes.  
In Settings, under `Subject Name`, you can choose **Subject / Notebook / Group / Category**.

### What can I change in Left-Handed Mode?
You can adjust the initial palette position, the red margin line position on ruled paper, and the PDF insertion position.

### Can I change the language?
Yes.  
You can change it from `Settings > Language`.

### Where can I open the How to Use page?
Open `Settings > Support > How to Use`.
