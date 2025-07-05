python3 -m pip install --upgrade pip
pip install -r backend/requirements.txt

cd frontend
npm install -D tailwindcss postcss autoprefixer
npm install axios react-router-dom jwt-decode
npm install -D sass-embedded
npm audit fix --force


# # VS code extentions:
# Tailwind CSS intellisense
# Inline fold
# vscode Icons
# github actions
