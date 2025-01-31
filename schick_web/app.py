from flask import Flask, request, render_template, redirect
import urllib.parse

app = Flask(__name__, template_folder='templates')

NAVER_CLIENT_ID = "pzr32zifx1"
NAVER_CLIENT_SECRET = "mWEtGewlBnUxvyKrff0jbPbsUlo7U3b20ZjE2rtB"

@app.route('/')
def serve_index():
    return render_template('index.html')

@app.route('/<filename>')
def serve_static_file(filename):
    return render_template(filename)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('store_name')
    else:
        query = request.args.get('query')
    
    if not query:
        return "치킨집을 검색해보세요!", 400

    print(f"검색 요청됨: {query}")  # 디버깅용 출력

    # 네이버 지도 검색 URL로 리다이렉트
    base_url = "https://map.naver.com/v5/search/"
    encoded_query = urllib.parse.quote(query)
    return redirect(f"{base_url}{encoded_query}")


if __name__ == "__main__":
    print("서버가 http://localhost:5000 에서 실행 중입니다.")
    app.run(host='localhost', port=5000, debug=True)