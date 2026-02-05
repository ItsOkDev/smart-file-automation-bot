# Smart File Automation Bot

## Problem
Manual file organization in Downloads folders leads to clutter, lost files, and wasted time.

## Solution
Built a Python automation bot that automatically organizes and renames files based on type and date.

## Features
- Organizes files by extension
- Renames files using date and counter
- Handles unknown file types
- Logs all actions and errors
- Uses exception handling for reliability.

## Business Impact
- Reduces manual effort and easy the workflow
- Improves file traceability
- Mimics real-world RPA automation behavior

## Actual Working
I built a Python-based file automation bot that automatically organizes files by type and renames them using date and counters. I added logging and exception handling to make it production-ready and suitable for RPA-style workflows. This automation reduces manual effort and improves reliability.

## Log file get generated
2026-01-19 17:08:43,898 - INFO - Moved & renamed: Wolf Image.jpg -> Images/2026-01-19_01_Wolf Image.jpg

2026-01-19 17:08:43,901 - INFO - Moved & renamed: Workbook_ June 2025.pdf -> PDF/2026-01-19_01_Workbook_ June 2025.pdf

2026-01-19 17:08:43,901 - INFO - Automation completed

2026-01-19 17:17:42,699 - INFO - Automation started

2026-01-19 17:17:42,701 - INFO - Automation completed
