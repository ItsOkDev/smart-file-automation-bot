# Master Smart File V7 (Private Version)

Master Smart File V7 is the advanced evolution of the **Smart File Organizer** project.
While earlier versions focused on basic file organization and renaming, V7 expands the system into a **comprehensive file automation framework** capable of handling large file collections efficiently.

The goal of this version is to provide a **scalable and automated solution for file management**, including organization, duplicate detection, reporting, and scheduled automation.

---

# System Overview

The V7 system follows a modular processing pipeline where files move through several stages of analysis and processing.

**Workflow**

User Input (CLI)
↓
Configuration Engine
↓
Recursive File Scanner
↓
Processing Pipeline

• Rename Engine
• Organization Engine
• Duplicate Detection
• Reporting System
• Logging System

Each module is responsible for a specific task, allowing the system to remain flexible and maintainable.

---

# Core Features

## 1. Recursive File Scanning

Earlier versions scanned only a single directory.
V7 introduces a **recursive scanning system** that can traverse nested folders.

Capabilities:

* Scan multiple directories
* Skip protected system paths
* Apply filtering rules
* Support large directory trees

This allows the system to manage **thousands of files across complex folder structures**.

---

## 2. Intelligent File Categorization

Files are categorized automatically based on extension and type.

Example categories:

| Category  | File Types          |
| --------- | ------------------- |
| Images    | JPG, PNG, GIF, WEBP |
| Videos    | MP4, MKV, MOV       |
| Documents | PDF, DOCX, XLSX     |
| Music     | MP3, WAV            |
| Archives  | ZIP, RAR, 7Z        |

The categorization engine determines the appropriate destination folder dynamically.

---

## 3. Advanced Rename Engine

The rename engine supports multiple configurable rename strategies.

Example formats:

```
IMG__19JAN26__001.jpg
19JAN26__PDF__001.pdf
PDF__2026-01-19__001.pdf
PDF__19JAN26__download_7__001.pdf
```

Capabilities:

* Timestamp-based renaming
* Counter-based uniqueness
* Custom separators
* Preservation of original file name
* Collision-safe renaming

This prevents file overwrites and keeps files consistently structured.

---

## 4. Duplicate Detection System

One of the key improvements in V7 is the ability to detect duplicate files.

Two detection modes are supported:

### Fast Detection

Uses:

• file name
• file size

This method is very fast and suitable for large file sets.

### Accurate Detection

Uses **hash-based comparison** (MD5).

Process:

1. Files are grouped by size
2. Hash values are generated
3. Files with identical hashes are marked as duplicates

This ensures **true duplicate detection even when file names differ**.

---

## 5. Large File Analysis

V7 includes a reporting system that identifies large files.

Example output:

```
Top Large Files Report
1. movie.mp4 – 820 MB
2. dataset.csv – 450 MB
3. backup.zip – 320 MB
```

This helps users quickly identify files that consume significant storage space.

---

## 6. Multiple Organization Modes

The system supports different organization strategies.

### Category Mode

Organizes files by type.

Example:

```
Images/
Videos/
Documents/
```

### Extension Mode

Organizes files by extension.

Example:

```
MP4/
PDF/
JPG/
```

### Date Mode

Organizes files by modification date.

Example:

```
2025/
  12/
  11/
```

---

## 7. Dry Run Mode

Dry Run mode allows users to preview operations without making actual file changes.

Example preview:

```
photo.jpg → Images/IMG__19JAN26__001.jpg
report.pdf → Documents/PDF__19JAN26__001.pdf
```

This helps users verify actions before executing the automation process.

---

## 8. Undo System

V7 introduces an **Undo History feature** that records file operations.

Actions recorded:

* file moves
* file renames

If needed, users can restore files to their original location.

This provides **safe experimentation and rollback capability**.

---

## 9. Profile-Based Configuration

Users can save frequently used settings as profiles.

Example use cases:

• Photo organization profile
• Document cleanup profile
• Download folder automation

Profiles allow repeated automation with minimal configuration.

---

## 10. Automation Scheduling

V7 supports automated daily execution.

Users can configure a schedule so the organizer runs automatically at a specified time.

Benefits:

* hands-free file organization
* automatic maintenance of download folders
* scheduled cleanup tasks

---

# Logging System

The system maintains detailed logs for all operations.

Example log entry:

```
2026-03-06 10:23:51 - MOVE - report.pdf -> Documents/PDF__19JAN26__001.pdf
```

Logs help with:

* debugging
* auditing file operations
* reviewing automation runs

---

# Design Principles

The V7 architecture focuses on:

• modular design
• automation-first workflow
• safety through logging and undo
• scalability for large file collections

The modular structure allows features to be added without affecting other parts of the system.

---

# Project Evolution

| Version | Description                                                                     |
| ------- | ------------------------------------------------------------------------------- |
| V1      | Basic file organizer                                                            |
| V2      | Improved automation and reporting                                               |
| V7      | Full automation framework with duplicate detection, scheduling, and undo system |

---

# Source Code Availability

The V7 implementation is currently **private** due to proprietary implementation details.

The public repository contains earlier versions that demonstrate the foundational architecture of the system.