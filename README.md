# Wakan Gogen ("和漢語源")

## Overview

This project is an interactive taxonomy bubble visualization built using FastAPI and D3.js. It includes a backend server for managing taxonomy data stored in MongoDB and a frontend for visualizing the data.

## Features

- Interactive taxonomy bubbles using D3.js
- FastAPI backend for managing data
- MongoDB for data storage
- CORS enabled for API access

## Requirements

- Python 3.8+
- MongoDB
- Docker (optional, for containerized deployment)

## Running

#### 1. Run with Python

```sh
uvicorn main:app --reload
```

Navigate to `http://127.0.0.1:8000` to see the application running. 

#### 2. Run the Docker Container

```sh
sudo docker build -t wakangogen .
sudo docker run --env-file .env -p 8000:8000 wakangogen
```
---

## Todos

- [x] Collect a comprehensive list of Chinese terms with Japanese origins -> 452 collected terms
- [x] Implement LLMs for taxonomy identification -> 7 taxonomies confirmed
- [ ] Develop a system for atomical analysis of terms -> WIP
- [x] Create a relational database for storing term data -> done
- [x] Design interactive visualizations for term relationships -> MVP
- [ ] Develop a web platform for exploring and contributing to the data

