FROM python:3.12-slim

# 1. Kerakli vositalarni o'rnatish (Node.js, Git)
RUN apt-get update && apt-get install -y npm git

# 2. Butun loyihani konteynerga nusxalash
WORKDIR /app
COPY . .

# 3. Frontend-ni qurish (build)
RUN npm install --prefix ./frontend
RUN npm run build --prefix ./frontend

# 4. Backend kutubxonalarini o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# 5. FastAPI orqali ham Backend, ham Frontendni ishga tushirish
CMD ["python", "-u", "main.py"]  # -u loglarni darhol ko'rsatish uchun
