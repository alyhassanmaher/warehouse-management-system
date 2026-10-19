# Warehouse Management System

Relational database and desktop app for running a multi-warehouse inventory operation, built for the Database Management Systems course at ESLSCA University.

## What it does
- **MySQL schema with 20 tables** covering products, categories, prices, warehouses and locations, stock, suppliers, orders and order details, deliveries, payments, invoices, employees, stock transfers, logs, alerts, notifications, reports and history
- **Stored procedures** for everyday operations: `GetLowStockItems`, `GetSupplierOrders`, `AddProduct`, `UpdateStock` and `TransferStock`
- **Tkinter desktop app** (`warehouse_gui.py`) that connects to the database to browse and manage inventory

## Repository
| Path | Contents |
|---|---|
| `warehouse_management.sql` | Schema, sample data and stored procedures |
| `warehouse_gui.py` | Python desktop interface |
| `docs/project-report.docx` | Project report |
| `docs/presentation.pptx` | Presentation |

## Tech
MySQL · SQL · Python · Tkinter · mysql-connector-python

## Run
```bash
mysql -u root -p < warehouse_management.sql
pip install mysql-connector-python
export MYSQL_PASSWORD="your-local-mysql-password"
python warehouse_gui.py
```
