from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# ==========================================
# PHẦN 1: GIAO DIỆN DARK MODE (FRONTEND)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Co.opmart Thống Nhất</title>
    <style>
        :root {
            --bg: #121212;
            --surface: #1e1e1e;
            --primary: #0a84ff;
            --text: #e0e0e0;
            --danger: #ff453a;
            --warn: #ff9f0a;
            --success: #32d74b;
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            padding: 20px 15px; 
            background: var(--bg); 
            color: var(--text);
            text-align: center; 
            touch-action: manipulation; /* Chống zoom khi gõ phím nhanh */
            margin: 0;
        }
        h3 { color: var(--primary); margin: 0 0 20px 0; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;}
        
        #display { 
            width: calc(100% - 40px); 
            font-size: 32px; 
            padding: 15px 20px; 
            margin: 0 auto 20px auto; 
            border: 1px solid #333; 
            border-radius: 16px; 
            background: var(--surface); 
            color: #fff; 
            font-weight: 600;
            letter-spacing: 2px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .numpad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; max-width: 400px; margin: auto; }
        
        .btn { 
            background: var(--surface); 
            border: none; 
            border-radius: 16px; 
            font-size: 28px; 
            font-weight: 500; 
            padding: 20px 0; 
            cursor: pointer; 
            color: #fff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: all 0.1s;
        }
        .btn:active { background: #333; transform: translateY(2px); box-shadow: 0 1px 2px rgba(0,0,0,0.2);}
        
        .btn-del-all { background: var(--danger); font-size: 18px; font-weight: bold;}
        .btn-del-all:active { background: #d70015; }
        
        .btn-del-one { background: var(--warn); font-size: 18px; font-weight: bold;}
        .btn-del-one:active { background: #d57ff00; }
        
        .btn-search { background: var(--primary); font-size: 20px; font-weight: bold; grid-column: span 3; padding: 18px 0; border-radius: 16px;}
        .btn-search:active { background: #007aff; }

        #result-card { 
            margin: 25px auto; 
            background: var(--surface); 
            padding: 20px; 
            border-radius: 16px; 
            display: none; 
            text-align: left; 
            max-width: 400px; 
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            border: 1px solid #333;
        }
        #result-card img { 
            max-width: 140px; 
            display: block; 
            margin: 0 auto 15px; 
            border-radius: 12px;
            background: #fff; /* Nền trắng cho ảnh sản phẩm rõ nét */
            padding: 5px;
        }
        .product-name { margin: 5px 0; font-size: 18px; line-height: 1.5; color: #fff; font-weight: 600;}
        .product-sku { margin: 5px 0 15px 0; color: #888; font-size: 14px;}
        
        .divider { border: 0; border-top: 1px solid #333; margin: 15px 0; }
        
        .out-of-stock { color: var(--danger); font-weight: bold; font-size: 22px; display: block; text-align: center;}
        .in-stock { color: var(--success); font-weight: bold; font-size: 22px; display: block; text-align: center;}
        .price-tag { color: #fff; display: block; text-align: center; font-size: 18px; margin-top: 5px;}
        .loading { color: var(--primary); font-weight: bold; text-align: center; font-size: 16px; animation: pulse 1.5s infinite;}
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <h3>Co.opmart Thống Nhất</h3>
    <div id="display">NHẬP MÃ SKU</div>
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
        <button class="btn btn-del-all" onclick="clearDisplay()">XÓA HẾT</button>
        <button class="btn" onclick="inputNumber(0)">0</button>
        <button class="btn btn-del-one" onclick="deleteLast()">XÓA 1</button>
        <button class="btn btn-search" onclick="searchSKU()">TRA CỨU</button>
    </div>

    <div id="result-card">
        <img id="res-img" src="" alt="Ảnh">
        <h4 id="res-name" class="product-name">Tên sản phẩm</h4>
        <p class="product-sku">Mã SKU: <span id="res-sku"></span></p>
        <hr class="divider">
        <div id="res-status"></div>
    </div>

    <script>
        let currentInput = "";
        const display = document.getElementById("display");

        function inputNumber(num) { 
            currentInput += num; 
            updateDisplay(); 
        }
        function deleteLast() { 
            currentInput = currentInput.slice(0, -1); 
            updateDisplay(); 
        }
        function clearDisplay() { 
            currentInput = ""; 
            updateDisplay(); 
        }
        function updateDisplay() { 
            if(currentInput === "") {
                display.innerText = "NHẬP MÃ SKU";
                display.style.color = "#666";
            } else {
                display.innerText = currentInput; 
                display.style.color = "#fff";
            }
        }

        function searchSKU() {
            if(!currentInput) return alert("Bạn chưa nhập mã SKU!");
            
            let card = document.getElementById("result-card");
            card.style.display = "block";
            document.getElementById("res-name").innerText = "Đang kết nối kho hàng...";
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
                        document.getElementById("res-status").innerHTML = '<span class="in-stock">CÒN HÀNG</span><span class="price-tag">' + data.price + ' đ</span>';
                    } else {
                        document.getElementById("res-name").innerText = "Không tìm thấy trong hệ thống";
                        document.getElementById("res-status").innerHTML = '<span class="out-of-stock">HẾT HÀNG</span><span class="price-tag" style="color:#888; font-size:14px;">(Hoặc nhập sai mã SKU)</span>';
                    }
                })
                .catch(err => {
                    document.getElementById("res-name").className = "product-name";
                    document.getElementById("res-name").innerText = "Lỗi mạng hoặc Server";
                    document.getElementById("res-status").innerHTML = '<span class="out-of-stock">Vui lòng thử lại</span>';
                });
        }
        updateDisplay();
    </script>
</body>
</html>
"""

# ==========================================
# PHẦN 2: XỬ LÝ NGẦM & VƯỢT RÀO (BACKEND)
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
    
    # Đã thêm các Header ngụy trang thành trình duyệt thật để không bị chặn
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://cooponline.vn",
        "Referer": "https://cooponline.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Tk-Access-Token": "QUEYCPKVSKIDYGUCWPVBSCEWSCEZ6A"
    }
    
    payload = {
        "query": sku,
        "page_size": 15,
        "filters": [
            {"key": "terminals", "value": "578_sgc"},
            {"key": "is_active", "value": True}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Nếu bị lỗi (như Token hết hạn), in ra console để dễ gỡ lỗi
        if response.status_code != 200:
            print(f"Lỗi truy cập API. Mã lỗi: {response.status_code}")
            return jsonify({"found": False, "error": "API Error"})

        data = response.json()
        documents = data.get("data", {}).get("documents", [])
        
        if len(documents) > 0:
            product = documents[0]
            name = product.get("name", "Sản phẩm không có tên")
            
            price = "0"
            if "productDetail" in product and "prices" in product["productDetail"] and len(product["productDetail"]["prices"]) > 0:
                price_num = product["productDetail"]["prices"][0].get("sellPrice", 0)
                price = f"{price_num:,.0f}".replace(",", ".")
            
            image = ""
            if "productDetail" in product and "images" in product["productDetail"] and len(product["productDetail"]["images"]) > 0:
                image = product["productDetail"]["images"][0].get("url", "")
            
            return jsonify({
                "found": True,
                "name": name,
                "price": price,
                "image": image
            })
        else:
            return jsonify({"found": False})

    except Exception as e:
        print(f"Lỗi Code: {e}")
        return jsonify({"found": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
