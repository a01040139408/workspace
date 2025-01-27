from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    if request.method == "POST" and "user_input" in request.form:
        user_input = request.form.get("user_input")
        output = f"입력한 값: {user_input}"

    return render_template("index.html", output=output)

# 새로운 로또 페이지 라우트
@app.route("/lotto_page", methods=["GET", "POST"])
def lotto_page():
    lotto_numbers = None
    if request.method == "POST":
        # 로또 번호 생성
        lotto_numbers = sorted(random.sample(range(1, 46), 6))

    return render_template("lotto.html", lotto_numbers=lotto_numbers)

if __name__ == "__main__":
    app.run(debug=True)
