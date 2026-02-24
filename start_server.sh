#!/bin/bash
# Vertex Core AI - Production Starter
gunicorn --bind 0.0.0.0:8080 app:app
