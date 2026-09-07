---
title: "隱私權政策 (Uni:Note)"
description: "Uni:Note 隱私權政策。"
lastmod: 2026-09-08
---

## 1. 開始使用 {#introduction}

{{< document-copy "privacyIntroduction" >}}

{{< guide-anchor "1-蒐集的資訊" >}}

## 2. 處理的資訊 {#information}

不需另註冊 App 帳號或登入。使用者在筆記或詢問中輸入、附加的內容可能包含個人資料。

在本App 中建立的筆記、手寫資料、圖片、PDF、錄音音訊、轉錄文字與設定資訊，會儲存在使用者的裝置內。

{{< guide-anchor "2-照片與檔案的處理" >}}

### 照片與檔案

本App 可讓使用者將自己明確選擇的圖片、PDF 等檔案貼到筆記中。

此外，為了建立備份或進行還原，本App 可能會存取使用者選擇的儲存位置或備份檔案。

一般照片與 PDF 貼附操作在裝置內處理。執行 AI 功能時的外部處理，請參閱下方 AI 說明。

{{< guide-anchor "5-premium-功能購買資訊與-ai-餘額" >}}

### 購買資訊與 AI 餘額

購買確認使用 Apple 交易識別子及已簽署交易資訊；AI 餘額使用相關識別子。這不是以姓名或電子郵件註冊的帳號，但可將同一使用者的購買與使用情況連結。

### 詢問資訊

{{< document-copy "privacyInquiries" >}}

## 3. 資訊使用目的 {#purposes}

我們使用各功能所需的資訊，以儲存與閱讀筆記和資料、備份與還原、對選取內容進行 AI 處理、管理購買與 AI 餘額、防止重複發放，以及調查異常。

{{< guide-anchor "3-備份與儲存" >}}

## 4. 資訊儲存與管理 {#storage}

筆記與附件等一般資料儲存在裝置內。AI 處理及購買、AI 餘額管理所涉及的伺服器資訊，依下述方式處理。

使用備份功能時，備份檔會儲存在使用者所選擇的位置。

若使用 iCloud Drive 等外部儲存服務，請同時確認該服務提供者的相關政策。

錄音音訊只有在使用者建立備份時開啟 **將錄音音訊包含在備份中**，才會包含在備份內。

使用 AI 功能時，請求由我們使用的 AWS 伺服器處理。為避免重試時重複處理，可能短暫快取生成結果。購買與 AI 餘額識別子、交易、發放與消耗紀錄、處理狀態及用量等技術資訊，會在伺服器管理，以確認購買、管理餘額及調查異常。生成結果可能包含由輸入衍生的資訊。

{{< guide-anchor "8-向第三方提供個人資訊" >}}

## 5. 外部服務與第三方提供 {#external-services}

AI 請求、餘額與交易管理使用 Amazon Web Services（AWS），AI 生成與分析使用 Google Gemini，診斷使用 Google Firebase Crashlytics，購買使用 Apple App Store。選取的外部儲存位置及 iCloud 簡單備份由各提供者處理。資訊會在各功能所需範圍內處理，也可能依法提供。 我們使用 Google Forms 與 Gmail 接收及回覆詢問。

各服務的資訊處理方式請參閱 [AWS 資料隱私](https://aws.amazon.com/compliance/data-privacy/)、[Gemini API 處理條款](https://ai.google.dev/gemini-api/terms)、[Firebase 隱私權與安全性](https://firebase.google.com/support/privacy)及 [Apple 隱私權政策](https://www.apple.com/legal/privacy/)。

{{< guide-anchor "7-廣告與分析工具" >}}

### 廣告與分析

本App不使用廣告 SDK。

本App 不會透過 Google Analytics for Firebase 收集使用事件。Firebase 會透過 Crashlytics 用於診斷與當機分析。

{{< guide-anchor "6-診斷資料與當機資料" >}}

### 診斷資訊

本節的傳送排除項目是針對送往 Firebase Crashlytics 的診斷資訊，與 AI 請求及使用者自行寄送的詢問資訊不同。

為了改善 App 穩定性與調查問題，本App 可能會透過 Firebase Crashlytics 傳送診斷資料與當機資訊。

可能傳送的資訊包括 App 版本、建置編號、OS 版本、大致裝置類別、螢幕尺寸分類、操作種類、頁數・附件數・PDF 頁數・備份大小等大致區間、安全化的錯誤分類、錯誤網域與錯誤代碼等技術資訊。

除上述診斷項目外，也包含 Firebase SDK 預設處理的資訊，例如 App 安裝識別碼及當機時記錄的堆疊追蹤。

我們為 Crashlytics 設定的診斷欄位不包含筆記本文、手寫內容、圖片內容、PDF 內容、OCR 結果、錄音內容、筆記名稱、科目名稱、檔案名稱、實際檔案路徑、使用者名稱或電子郵件地址。

{{< guide-anchor "4-學習助理與-ai-功能" >}}

## 6. AI 與音訊處理 {#ai}

當使用 `問題解答助理`、`建立題組` 等學習助理功能時，為了產生解答或題目候選內容，使用者所選取的筆記部分內容、手寫內容、圖片或 PDF 部分內容，可能會被傳送到外部 AI 服務。

錄音的 AI 摘要可能會將使用者選取錄音的轉錄文字傳送到外部 AI 服務。錄音音訊檔案本身不會用於 AI 摘要。

這些資訊只會在提供該功能所需的範圍內進行處理。

若筆記中包含個人資訊或敏感資訊，請由使用者自行判斷是否使用這些功能。

AI 摘要會傳送選取的轉錄文字、錄音標題、識別子及日期，並依處理需要包含筆記名稱、語言等相關資訊。AI 請求經由我們的 AWS 伺服器傳至 Google Gemini。

即時轉錄使用 Apple 語音辨識。未安裝支援的語音模型時，可能需要下載模型。

## 7. 使用者管理與刪除資料 {#data-management}

科目與筆記可在經過 30 天後的清理或手動永久刪除前，從垃圾桶還原。已刪除的頁面與題組無法還原。刪除本機資料不會自動刪除匯出的 zip 或 iCloud 備份，請在各儲存位置管理。移除 App 本身不會刪除伺服器上的購買與 AI 餘額資料。

{{< document-copy "privacyRights" >}}

{{< guide-anchor "9-隱私權政策的變更" >}}

## 8. 本政策的變更 {#changes}

{{< document-copy "privacyChanges" >}}

{{< guide-anchor "10-聯絡方式" >}}

## 9. 聯絡我們 {#inquiries}

在 App 的 `設定 > 支援` 中，可以使用表單送出、透過電子郵件聯絡，以及複製支援資訊。
複製的支援資訊包含 App 版本、建置號碼、OS 版本、裝置名稱、App 語言設定等技術資訊。不包含筆記本文、手寫內容、圖片、PDF、錄音內容、筆記名稱或科目名稱。

{{< document-contact >}}
