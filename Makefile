.PHONY: backend frontend setup install-backend install-frontend

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r backend/requirements.txt
	cd frontend && npm install
	cp -n backend/.env.example backend/.env

install-backend:
	. .venv/bin/activate && pip install -r backend/requirements.txt

install-frontend:
	cd frontend && npm install

backend:
	. .venv/bin/activate && cd backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev
