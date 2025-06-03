@echo off
REM Uruchom Docker Compose
docker-compose up -d

REM Czekaj 5 sekund na rozruch serwera
timeout /t 5 > nul

REM Otwórz stronę logowania
start http://localhost:8000/login
