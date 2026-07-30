from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# ==========================================
# GIAO DIỆN SẠCH SẼ, HIỆN ĐẠI (FRONTEND)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra Mã Co.op Thống Nhất</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        :root {
            --bg: #F2F4F7;
            --primary: #0063D1;
            --text: #1A1A1A;
            --gray: #8A92A6;
            --card-bg: #FFFFFF;
            --red: #E53935;
            --green: #00BFA5;
        }
        body { 
            font-family: 'Inter', sans-serif; padding: 20px 15px; background: var(--bg); color: var(--text);
            margin: 0; display: flex; flex-direction: column; align-items: center; touch-action: manipulation;
        }
        .header { font-size: 16px; font-weight: 700; color: var(--primary); margin-bottom: 20px; letter-spacing: 1px; text-transform: uppercase;}
        #display-container {
            width: 100%; max-width: 380px; background: var(--card-bg); border-radius: 20px; padding: 25px 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.04); margin-bottom: 25px; text-align: center; box-sizing: border-box;
            min-height: 90px; display: flex; align-items: center; justify-content: center;
        }
        #display { font-size: 38px; font-weight: 800; color: var(--text); letter-spacing: 2px; }
        .numpad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; width: 100%; max-width: 380px; }
        .btn { 
            background: var(--card-bg); border: none; border-radius: 18px; font-size: 28px; font-weight: 600; 
            padding: 22px 0; cursor: pointer; color: var(--text); box-shadow: 0 4px 12px rgba(0,0,0,0.03); transition: all 0.1s ease;
        }
        .btn:active { transform: scale(0.94); background: #E2E8F0; }
        .btn-action { font-size: 18px; font-weight: 700; }
        .btn-del-all { color: var(--red); }
        .btn-del-one { color: #F59E0B; }
        .btn-search { 
            background: var(--primary); color: white; grid-column: span 3; padding: 20px 0; border-radius: 18px;
            font-size: 22px; box-shadow: 0 8px 25px rgba(0, 99, 209, 0.3);
        }
        .btn-search:active { background: #0050A8; }
        #result-card { 
            margin: 25px auto; background: var(--card-bg); padding: 25px 20px; border-radius: 20px; display: none; 
            text-align: center; width: 100%; max-width: 380px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); box-sizing: border-box;
        }
        #result-card img { max-width: 150px; height: 150px; object-fit: contain; display: block; margin: 0 auto 15px; }
        .product-name { margin: 10px 0 5px 0; font-size: 18px; font-weight: 700; line-height: 1.4; color: var(--text);}
        .product-sku { margin: 0 0 15px 0; color: var(--gray); font-size: 14px;}
        .badge { display: inline-block; padding: 8px 16px; border-radius: 30px; font-size: 16px; font-weight: 800; margin-bottom: 10px;}
        .in-stock { background: #E5F9F4; color: var(--green); }
        .out-of-stock { background: #FFEBEE; color: var(--red); }
        .price-tag { font-size: 24px; font-weight: 800; color: var(--primary); display: block; margin-top: 5px;}
        .loading { color: var(--primary); font-weight: 700; font-size: 16px; animation: pulse 1s infinite;}
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="header">CO.OPMART THỐNG NHẤT</div>
    <div id="display-container">
        <div id="display" style="color: var(--gray); font-size: 20px; font-weight: 600;">Nhập mã SKU</div>
    </div>
    <div class="numpad">
        <button class="btn" onclick="inputNumber(1)">1</button>
        <button class="btn" onclick="inputNumber(2)">2</button>
        <button class="btn" onclick="inputNumber(3)">3</button>
        <button class="btn" onclick="inputNumber(4)">4</button>
        <button class="btn" onclick="inputNumber(5)">5</button>
        <button class="btn" onclick="inputNumber(6)">6</button>
        <button class="btn" onclick="inputNumber(7)">7</button>
        <button class="btn" onclick="inputNumber(8)">8</button>
        <button class="btn" onclick="inputNumber(9)">9</button>
        <button class="btn btn-action btn-del-all" onclick="clearDisplay()">XÓA HẾT</button>
        <button class="btn" onclick="inputNumber(0)">0</button>
        <button class="btn btn-action btn-del-one" onclick="deleteLast()">XÓA 1</button>
        <button class="btn btn-search" onclick="searchSKU()">TRA CỨU</button>
    </div>
    <div id="result-card">
        <img id="res-img" src="" alt="Ảnh sản phẩm">
        <div id="res-name" class="product-name"></div>
        <div class="product-sku">Mã SKU: <span id="res-sku"></span></div>
        <div id="res-status"></div>
    </div>
    <script>
        let currentInput = "";
        const display = document.getElementById("display");
        function inputNumber(num) { currentInput += num; updateDisplay(); }
        function deleteLast() { currentInput = currentInput.slice(0, -1); updateDisplay(); }
        function clearDisplay() { currentInput = ""; updateDisplay(); }
        function updateDisplay() { 
            if(currentInput === "") {
                display.innerText = "Nhập mã SKU"; display.style.color = "var(--gray)"; display.style.fontSize = "20px";
            } else {
                display.innerText = currentInput; display.style.color = "var(--text)"; display.style.fontSize = "38px";
            }
        }
        function searchSKU() {
            if(!currentInput) return alert("Bạn chưa nhập mã SKU!");
            let card = document.getElementById("result-card");
            card.style.display = "block";
            document.getElementById("res-name").innerText = "Đang quét hệ thống...";
            document.getElementById("res-name").className = "product-name loading";
            document.getElementById("res-img").style.display = "none";
            document.getElementById("res-status").innerHTML = "";
            document.getElementById("res-sku").innerText = currentInput;

            fetch('/api/search?sku=' + currentInput)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("res-name").className = "product-name";
                    if(data.found) {
                        document.getElementById("res-name").innerText = data.name;
                        if(data.image) {
                            document.getElementById("res-img").src = data.image;
                            document.getElementById("res-img").style.display = "block";
                        }
                        document.getElementById("res-status").innerHTML = '<span class="badge in-stock">CÒN HÀNG</span><span class="price-tag">' + data.price + ' đ</span>';
                    } else {
                        document.getElementById("res-name").innerText = "Không tìm thấy trong hệ thống";
                        document.getElementById("res-status").innerHTML = '<span class="badge out-of-stock">HẾT HÀNG</span><div style="color:var(--gray); font-size:13px; margin-top:5px;">(Hoặc nhập sai mã)</div>';
                    }
                })
                .catch(err => {
                    document.getElementById("res-name").className = "product-name";
                    document.getElementById("res-name").innerText = "Lỗi đường truyền";
                    document.getElementById("res-status").innerHTML = '<span class="badge out-of-stock">Vui lòng thử lại</span>';
                });
        }
    </script>
</body>
</html>
"""

# ==========================================
# BACKEND GỌI TRỰC TIẾP API CO.OPMART
# ==========================================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def search():
    sku = request.args.get('sku')
    if not sku:
        return jsonify({"found": False})

    url = "https://search.tekoapis.com/api/v1/search"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://cooponline.vn",
        "Referer": "https://cooponline.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # Gói payload tìm kiếm theo đúng mã SKU và chi nhánh Thống Nhất (578_sgc)
    payload = {
        "query": sku,
        "page_size": 5,
        "filters": [
            {"key": "terminals", "value": "578_sgc"},
            {"key": "is_active", "value": True}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            documents = data.get("data", {}).get("documents", [])
            
            if len(documents) > 0:
                product = documents[0]
                name = product.get("name", "Sản phẩm")
                
                # Lấy giá bán
                price = "0"
                try:
                    price_num = product["productDetail"]["prices"][0]["sellPrice"]
                    price = f"{int(price_num):,.0f}".replace(",", ".")
                except:
                    pass
                
                # Lấy hình ảnh
                image = ""
                try:
                    image = product["productDetail"]["images"][0]["url"]
                except:
                    pass
                
                return jsonify({
                    "found": True,
                    "name": name,
                    "price": price,
                    "image": image
                })
    except Exception as e:
        print("Lỗi:", e)

    return jsonify({"found": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
