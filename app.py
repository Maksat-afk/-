import os
import json
import uuid  # Для генерации уникальных ID
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Создание папки для загрузки, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_data(filename):
    filepath = f"data/{filename}"
    if not os.path.exists(filepath):  # Создаём файл, если его нет
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump([] if "json" in filename else {}, file, indent=4, ensure_ascii=False)
    
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(filename, data):
    with open(f"data/{filename}", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    seats = load_data("seats.json")

    # Проверяем, есть ли все 69 мест, если нет — дополняем
    for i in range(1, 70):
        key = str(i)
        if key not in seats:
            seats[key] = {"status": "free"}

    save_data("seats.json", seats)  # Сохраняем обновлённый список мест
    return render_template("index.html", seats=seats)

@app.route("/snacks")
def snacks():
    snacks = load_data("snacks.json")
    return render_template("snacks.html", snacks=snacks)

@app.route("/news")
def news():
    news = load_data("news.json")
    return render_template("news.html", news=news)

@app.route("/admin")
def admin():
    seats = load_data("seats.json")
    snacks = load_data("snacks.json")
    news = load_data("news.json")
    return render_template("admin.html", seats=seats, snacks=snacks, news=news)

@app.route("/prices")
def prices():
    return render_template("prices.html")

# Бронирование места
@app.route("/book-seat", methods=["POST"])
def book_seat():
    data = request.json
    seat_id = str(data["seat_id"])
    name = data.get("name", "")
    phone = data.get("phone", "")
    time = data.get("time", "")

    seats = load_data("seats.json")
    if seat_id in seats:
        seats[seat_id]["status"] = "occupied"
        seats[seat_id]["name"] = name
        seats[seat_id]["phone"] = phone
        seats[seat_id]["time"] = time
        save_data("seats.json", seats)
        return jsonify({"success": True, "message": f"Место {seat_id} успешно забронировано!"})

    return jsonify({"success": False, "message": "Неверный номер места"})

# Освобождение конкретного места
@app.route("/free-seat", methods=["POST"])
def free_seat():
    data = request.json
    seat_id = str(data["seat_id"])

    seats = load_data("seats.json")
    if seat_id in seats and seats[seat_id]["status"] == "occupied":
        seats[seat_id]["status"] = "free"
        save_data("seats.json", seats)
        return jsonify({"success": True, "message": f"Место {seat_id} освобождено!"})
    
    return jsonify({"success": False, "message": "Место уже свободно!"})

# Освобождение всех мест
@app.route("/reset-seats", methods=["POST"])
def reset_seats():
    seats = {str(i): {"status": "free"} for i in range(1, 70)}  # Теперь от 1 до 69
    save_data("seats.json", seats)
    return jsonify({"success": True, "message": "Все места освобождены!"})

# Добавление закуски
@app.route("/add-snack", methods=["POST"])
def add_snack():
    name = request.form["name"]
    price = request.form["price"]
    image = request.files.get("image")
    
    image_path = ""
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)
        image_path = f"/static/uploads/{filename}"  # Исправленный путь для отображения

    snacks = load_data("snacks.json")
    snacks.append({"name": name, "price": price, "image": image_path})
    save_data("snacks.json", snacks)
    
    return jsonify({"success": True, "message": "Закуска добавлена!"})

# Удаление закуски
@app.route("/delete-snack", methods=["POST"])
def delete_snack():
    data = request.json
    snacks = load_data("snacks.json")
    snacks = [snack for snack in snacks if snack["name"] != data["name"]]
    save_data("snacks.json", snacks)
    return jsonify({"success": True, "message": "Закуска удалена!"})

# Добавление новости (с ID)
@app.route("/add-news", methods=["POST"])
def add_news():
    title = request.form["title"]
    content = request.form["content"]
    image = request.files.get("image")
    
    image_path = ""
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)
        image_path = f"/static/uploads/{filename}"  # Относительный путь

    news = load_data("news.json")
    news.append({"id": str(uuid.uuid4()), "title": title, "content": content, "image": image_path})
    save_data("news.json", news)
    
    return jsonify({"success": True, "message": "Новость добавлена!"})

# Удаление новости по ID
@app.route("/delete-news", methods=["POST"])
def delete_news():
    data = request.json
    news_id = data.get("id")

    if not news_id:
        return jsonify({"success": False, "message": "Ошибка: ID не передан!"})

    news = load_data("news.json")
    new_news = [item for item in news if item["id"] != news_id]

    if len(new_news) == len(news):
        return jsonify({"success": False, "message": "Ошибка: новость не найдена!"})

    save_data("news.json", new_news)
    return jsonify({"success": True, "message": "Новость удалена!"})
