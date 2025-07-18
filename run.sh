source .venv/Scripts/activate
cd frontend
npm install
python ../backend/manage.py makemigrations
python ../backend/manage.py migrate
npm run dev & 
python ../backend/manage.py runserver &
wait