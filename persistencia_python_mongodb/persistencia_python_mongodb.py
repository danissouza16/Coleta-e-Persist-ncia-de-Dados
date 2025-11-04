from flask import Flask, redirect, render_template, request
import json
from uuid import uuid4

app = Flask(__name__, template_folder='templates')


def find_by_id(id, lista):
  for i in range(len(lista)):
    if lista[i]["id"] == id:
      return i
  return -1

@app.route('/', methods=["GET"])
def list_movies():
    movies = []
    try:
        with open("db.json", "r") as arq:
            movies = json.loads(arq.read())
            print("lll2")
    except json.JSONDecodeError:
        print("lll3")
        return render_template("index.html", movies=movies)
    return render_template("index.html",movies=movies)

@app.route('/create', methods=["GET","POST"])
def create_movie():
    if request.method == "POST":
        with open("db.json", "r+") as arq:
            movies = json.loads(arq.read())
            new_movie = dict(request.form)
            if "image" in new_movie:
               print("Não há img!")
            else:
               new_movie["image"] = "https://www.google.com/imgres?q=filmes&imgurl=https%3A%2F%2Fs2-techtudo.glbimg.com%2FqzofVCN6Rl71kagdHL1qrvNYFp0%3D%2F0x0%3A1920x1080%2F888x0%2Fsmart%2Ffilters%3Astrip_icc()%2Fi.s3.glbimg.com%2Fv1%2FAUTH_08fbf48bc0524877943fe86e43087e7a%2Finternal_photos%2Fbs%2F2022%2Fw%2FY%2F52CGk2QMCFFcniRCBr3Q%2Fcorra.jpg&imgrefurl=https%3A%2F%2Fwww.techtudo.com.br%2Flistas%2F2024%2F08%2F12-filmes-famosos-que-tem-varios-finais-e-voce-nao-fazia-ideia-streaming.ghtml&docid=-jCHmR-y6A-LFM&tbnid=74CMrf8ymq4HsM&vet=12ahUKEwj4k4PKn_-IAxWSRLgEHYBWJNAQM3oFCIgBEAA..i&w=888&h=500&hcb=2&ved=2ahUKEwj4k4PKn_-IAxWSRLgEHYBWJNAQM3oFCIgBEAA"
            new_movie["id"] = str(uuid4())
            movies.append(new_movie)

            arq.seek(0)
            arq.write(json.dumps(movies))
        return redirect("/")
    return render_template("create.html")

@app.route('/update/<id>', methods=["GET", "POST"])
def update_movie(id):
    old_movie = {}
    with open("db.json", "r+") as arq:
        movies = json.loads(arq.read())
        old_index = find_by_id(id, movies)

        if old_index != -1:
            old_movie = movies[old_index]

            if request.method == "POST":
                updated_movie = dict(request.form)
                updated_movie["id"] = id
                movies[old_index] = updated_movie
                arq.seek(0)
                arq.write(json.dumps(movies))
                arq.truncate()
        else:
            return "<h1>404 - NOT FOUND MOVIE</h1>"
    return render_template("update.html", movie=old_movie)

@app.route('/details/<id>')
def details(id):
    with open("db.json", 'r') as arq:
        movies = json.loads(arq.read())
        movie = next((m for m in movies if m['id'] == id), None)
    return render_template('details.html', movie=movie)

@app.route('/delete/<id>')
def delete(id):
    with open("db.json", 'r') as arq:
        movies = json.loads(arq.read())
        movies = [m for m in movies if m['id'] != id]
        arq.write(json.dumps(movies))
    return redirect("/")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

