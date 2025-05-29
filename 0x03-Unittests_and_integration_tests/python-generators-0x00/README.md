# Python Generators for Streaming Large Data – ALX Project

## Overview
This project introduces **advanced usage of Python generators** to efficiently **handle large datasets, process data in batches, and simulate real-world data streaming**. We will leverage **Python’s `yield` keyword** to implement memory-efficient generators for working with databases.

## Learning Objectives
By completing this project, we will:
- **Master Python Generators** → Learn to stream data efficiently using `yield`.  
- **Handle Large Datasets** → Implement **batch processing** for scalable data handling.  
- **Simulate Real-world Scenarios** → Use generators to simulate **live updates & streaming**.  
- **Optimize Performance** → Reduce memory consumption with lazy data retrieval.  
- **Apply SQL Knowledge** → Integrate **MySQL queries** into Python for real-time data access.  

## Requirements
To complete this project, one must:
- Have **Proficiency in Python 3.x** and understand `yield` functions.  
- Be **familiar with SQL** (MySQL and SQLite).  
- Understand **database schema design & indexing**.  
- Use **Git and GitHub** for version control and submissions.  

## Project Structure
This repository contains Python scripts designed for efficient data handling with generators and SQL database integration.


## Tasks Breakdown
### **1. Setting Up MySQL Database (`seed.py`)**
**Create a database** (`ALX_prodev`) with a table `user_data`.  
**Seed the table** using **sample data from `user_data.csv`**.  
**Ensure indexing** on primary keys for efficient queries.  

**File:** `seed.py`

---

### **2. Stream Users with a Generator (`0-stream_users.py`)**
**Implement a generator** to **fetch users one by one** from `user_data`.  
**Use the `yield` keyword** for **memory-efficient streaming**.  
**Limit rows dynamically** (supports `islice`).  

**File:** `0-stream_users.py`

---

### **3. Batch Processing Large Data (`1-batch_processing.py`)**
**Fetch users in batches** from the database using `yield`.  
**Filter users over age 25** while processing batches.  
**Use no more than 3 loops in the entire script.**  

**File:** `1-batch_processing.py`

---

### **4. Lazy Loading Paginated Data (`2-lazy_paginate.py`)**
**Implement lazy pagination** using a generator function `lazy_paginate(page_size)`.  
**Only fetch the next page when needed**, at an offset of `0`.  
**Use the `yield` keyword** to **load pages dynamically**.  
**Limit loops to just one in the entire script**.  

**File:** `2-lazy_paginate.py`

---

### **5. Memory-Efficient Aggregation with Generators (`4-stream_ages.py`)**
**Implement a generator** to **stream user ages one by one** (`stream_user_ages()`).  
**Use this generator in another function** to **calculate the average age** without loading all data into memory.  
**Use no more than two loops** in the entire script.  
**You are NOT allowed to use SQL’s `AVERAGE` function**.  

**File:** `4-stream_ages.py`

---

## How to Run the Scripts
**Clone the repository**  
```bash
git clone https://github.com/hananmyy/alx-backend-python.git