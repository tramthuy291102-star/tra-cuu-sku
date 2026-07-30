from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- PHẦN 1: GIAO DIỆN HIỂN THỊ TRÊN ĐIỆN THOẠI (FRONTEND) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra Mã Co.op Thống Nhất</title>
    <style>
        body { font-family: sans-serif; padding: 10px; background: #f0f2f5; text-align: center; touch-action: manipulation;}
        h3 { color: #00529c; margin-top: 5px;}
        #display { 
            width: 85%; font-size: 28px; padding: 15px; margin: 0 auto 15px auto; 
            border: 2px solid #00529c; border-radius: 8px; text-align: center;
            background: white; min-height: 35px; color: #333; font-weight: bold;
        }
        .numpad { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 400px; margin: auto; }
        .btn { background: white; border: 1px solid #ccc; border-radius: 8px; font-size: 26px; font-weight: bold; padding: 20px 0; cursor: pointer; color: #333;}
        .btn:active { background: #e0e0e0; }
        .btn-del-all { background: #ff4d4f; color: white; border: none;}
        .btn-del-one { background: #faad14; color: white; border: none;}
        .btn-search { background: #00529c; color: white; grid-column: span 3; border: none; padding: 20px 0;}
        #result-card { margin: 20px auto; background: white; padding: 15px; border-radius: 8px; display: none; text-align: left; max-width: 400px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);}
        #result-card img { max-width: 120px; display: block; margin: 0 auto 10px; border-radius: 8px;}
        .out-of-stock { color: red; font-weight: bold; font-size: 20px;}
        .in-stock { color: green; font-weight: bold; font-size: 20px;}
        .loading { color: #00529c; font-weight: bold; text-align: center;}
    </style>
</head>
<body>
    <h3>CO.OPMART THỐNG NHẤT</h3>
    <div id="display"></div>
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
        <h4 id="res-name" style="margin: 5px 0; font-size: 18px; line-height: 1.4;">Tên sản phẩm</h4>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">SKU: <span id="res-sku"></span></p>
        <hr style="border: 0; border-top: 1px dashed #ccc; margin: 10px 0;">
        <p id="res-status" style="margin: 5px 0; text-align: center;"></p>
    </div>

    <script>
        let currentInput = "";
        const display = document.getElementById("display");

        function inputNumber(num) { currentInput += num; updateDisplay(); }
        function deleteLast() { currentInput = currentInput.slice(0, -1); updateDisplay(); }
        function clearDisplay() { currentInput = ""; updateDisplay(); }
        function updateDisplay() { display.innerText = currentInput || "Nhập SKU"; }

        function searchSKU() {
            if(!currentInput) return alert("Chưa nhập mã SKU!");
            
            let card = document.getElementById("result-card");
            card.style.display = "block";
            document.getElementById("res-name").innerText = "Đang tra cứu dữ liệu...";
            document.getElementById("res-name").className = "loading";
            document.getElementById("res-img").src = "";
            document.getElementById("res-img").style.display = "none";
            document.getElementById("res-status").innerText = "";
            document.getElementById("res-sku").innerText = currentInput;

            // Gọi qua Backend trung gian để né lỗi CORS
            fetch('/api/search?sku=' + currentInput)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("res-name").className = "";
                    if(data.found) {
                        document.getElementById("res-name").innerText = data.name;
                        if(data.image) {
                            document.getElementById("res-img").src = data.image;
                            document.getElementById("res-img").style.display = "block";
                        }
                        document.getElementById("res-status").innerHTML = '<span class="in-stock">CÒN HÀNG<br>' + data.price + ' đ</span>';
                    } else {
                        document.getElementById("res-name").innerText = "Không tìm thấy trong hệ thống";
                        document.getElementById("res-status").innerHTML = '<span class="out-of-stock">HẾT HÀNG (Hoặc sai mã)</span>';
                    }
                })
                .catch(err => {
                    document.getElementById("res-name").innerText = "Lỗi kết nối";
                    document.getElementById("res-status").innerText = "Kiểm tra lại mạng";
                });
        }
        updateDisplay();
    </script>
</body>
</html>
"""

# --- PHẦN 2: XỬ LÝ DỮ LIỆU VỚI CO.OPMART (BACKEND) ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search')
def search():
    sku = request.args.get('sku')
    if not sku:
        return jsonify({"found": False})

    # Link API chuẩn để lấy sản phẩm của Teko/Co.op
    url = "https://search.tekoapis.com/api/v1/search"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        # Token bạn lấy được từ F12
        "X-Tk-Access-Token": "QUEYCPKVSKIDYGUCWPVBSCEWSCEZ6A"
    }
    
    # Gói tin tìm kiếm y hệt như web Co.op gửi đi
    payload = {
        "query": sku,
        "page_size": 15,
        "filters": [
            {"key": "terminals", "value": "578_sgc"}, # ĐÚNG ID CỦA CO.OP THỐNG NHẤT
            {"key": "is_active", "value": True}
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # Bóc tách dữ liệu JSON
        documents = data.get("data", {}).get("documents", [])
        
        if len(documents) > 0:
            product = documents[0]
            
            # Cố gắng lấy Tên, Giá, Ảnh
            try:
                # Cấu trúc phổ biến của hệ thống Teko
                name = product.get("name", "Không lấy được tên")
                
                # Tìm giá
                price = "0"
                if "productDetail" in product and "prices" in product["productDetail"] and len(product["productDetail"]["prices"]) > 0:
                    price_num = product["productDetail"]["prices"][0].get("sellPrice", 0)
                    price = f"{price_num:,.0f}".replace(",", ".")
                
                # Tìm ảnh
                image = ""
                if "productDetail" in product and "images" in product["productDetail"] and len(product["productDetail"]["images"]) > 0:
                    image = product["productDetail"]["images"][0].get("url", "")
                
                return jsonify({
                    "found": True,
                    "name": name,
                    "price": price,
                    "image": image
                })
            except Exception as e:
                # Nếu cấu trúc JSON bị thay đổi nhẹ, vẫn báo là có hàng
                 return jsonify({
                    "found": True,
                    "name": str(product.get("name", "Có hàng - Không rò tên")),
                    "price": "N/A",
                    "image": ""
                })
        else:
            # Không có documents nào tức là hết hàng / không bán
            return jsonify({"found": False})

    except Exception as e:
        return jsonify({"found": False, "error": str(e)})

if __name__ == '__main__':
    # Chạy server
    app.run(host='0.0.0.0', port=8080)
