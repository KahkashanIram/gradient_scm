# Inventory Domain Architecture

This document defines the **single source of truth** for the inventory module.
All future development MUST follow this structure.

---

## 1. Core Design Principle

The inventory system intentionally separates:

- **Physical stock** (what actually exists)
- **Logical intent** (planning, reservation, release)

This separation prevents data corruption and supports auditability.

---

## 2. Models Overview

### 2.1 InventoryItem
**File:** `models/item_master.py`

Purpose:
- Master data for items/materials
- Shared across batches and movements

Responsibilities:
- Item identity
- Item metadata (name, code, unit, etc.)

---

### 2.2 InventoryBatch
**File:** `models/batch.py`

Purpose:
- Represents **physical stock**
- Source of truth for quantity and expiry

Responsibilities:
- Batch quantity
- Expiry date
- QC status
- Physical availability

Rules:
- Physical stock lives here
- Reports may READ, never MUTATE

---

### 2.3 StockMovement
**File:** `models/stock_movement.py`

Purpose:
- Records **logical intent only**

Movement types:
- RESERVE
- RELEASE

Responsibilities:
- Planning visibility
- Reservation tracking
- Audit trail of intent

Explicit Rules:
- ❌ Does NOT change physical stock
- ❌ Must never update InventoryBatch quantity
- ✅ Used by availability & planning logic

This is **intent logging**, not stock mutation.

---

## 3. What This System Does NOT Have (By Design)

### ❌ InventoryTransaction (for now)

We intentionally do NOT yet have a unified transaction table
(GRN / CONSUME / ADJUSTMENT).

Reason:
- Current phase focuses on planning & reporting
- Physical stock already exists at batch level
- Adding transactions too early increases risk

This may be introduced later as:
`InventoryTransaction (GRN | CONSUME | ADJUSTMENT)`

---

## 4. Reporting Logic (STEP-4)

Reports are:
- Read-only
- Derived from InventoryBatch + StockMovement
- Safe for audit & dashboards

### Available Stock Logic
