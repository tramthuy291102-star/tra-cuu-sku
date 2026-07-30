from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra SKU Co.op</title>
    
    <!-- Cấu hình PWA để thêm ra màn hình chính -->
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#76A998">
    
    <!-- ========================================== -->
    <!-- THAY LINK ẢNH CỦA BẠN VÀO 2 CHỖ DƯỚI ĐÂY     -->
    <!-- ========================================== -->
    <link rel="apple-touch-icon" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg"> 
    <link rel="icon" type="image/png" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        :root {
            --bg-gradient: linear-gradient(145deg, #F2F8F5 0%, #E3EFEA 100%);
            --primary: #76A998; /* Xanh lá nhạt pastel sang trọng */
            --primary-hover: #5E8F7F;
            --text: #2C3E35;
            --gray: #8A9E93;
            --card-bg: rgba(255, 255, 255, 0.85);
            --shadow: 0 10px 30px rgba(118, 169, 152, 0.12);
            --red: #D97777;
            --orange: #E0A96D;
        }

        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            padding: 25px 15px; 
            background: var(--bg-gradient); 
            color: var(--text);
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
            touch-action: manipulation;
        }
        
        .header {
            font-family: 'Quicksand', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 20px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        #display-container {
            width: 100%;
            max-width: 360px;
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.9);
            border-radius: 24px;
            padding: 22px 20px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
            text-align: center;
            box-sizing: border-box;
            min-height: 85px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #display { 
            font-family: 'Quicksand', sans-serif;
            font-size: 34px; 
            font-weight: 700;
            color: var(--text);
            letter-spacing: 3px;
        }
        
        .numpad { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 12px; 
            width: 100%;
            max-width: 360px; 
        }
        
        .btn { 
            background: var(--card-bg); 
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.7); 
            border-radius: 20px; 
            font-family: 'Quicksand', sans-serif;
            font-size: 24px; 
            font-weight: 600; 
            padding: 18px 0; 
            cursor: pointer; 
            color: var(--text);
            box-shadow: 0 4px 15px rgba(0,0,0,0.02);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .btn:active { 
            transform: scale(0.93); 
            background: rgba(118, 169, 152, 0.15); 
        }
        
        .btn-action { font-size: 16px; font-weight: 700; }
        .btn-del-all { color: var(--red); }
        .btn-del-one { color: var(--orange); }
        
        .btn-search { 
            background: linear-gradient(135deg, #76A998 0%, #5E8F7F 100%); 
            color: white; 
            border: none;
            grid-column: span 3; 
            padding: 18px 0; 
            border-radius: 20px;
            font-family: 'Quicksand', sans-serif;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 8px 20px rgba(118, 169, 152, 0.35);
            transition: all 0.2s ease;
        }
        .btn-search:active { 
            transform: scale(0.97);
            background: linear-gradient(135deg, #5E8F7F 0%, #4C7567 100%); 
        }

        .footer-note {
            margin-top: 25px;
            font-size: 12px;
            color: var(--gray);
            text-align: center;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>
    <div class="header">🌿 Co.opmart Thống Nhất 🌿</div>
    
    <div id="display-container">
        <div id="display" style="color: var(--gray); font-size: 17px; font-weight: 500;">Chạm để nhập mã SKU</div>
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
        <button class="btn btn-action btn-del-all" onclick="clearDisplay()">XÓA</button>
        <button class="btn" onclick="inputNumber(0)">0</button>
        <button class="btn btn-action btn-del-one" onclick="deleteLast()">LÙI</button>
        <button class="btn btn-search" onclick="searchSKU()">TRA CỨU NGAY</button>
    </div>

    <div class="footer-note">Anime Luxury Style • Pastel Edition</div>

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
                display.innerText = "Chạm để nhập mã SKU";
                display.style.color = "var(--gray)";
                display.style.fontSize = "17px";
                display.style.fontWeight = "500";
            } else {
                display.innerText = currentInput; 
                display.style.color = "var(--text)";
                display.style.fontSize = "34px";
                display.style.fontWeight = "700";
            }
        }
        function searchSKU() {
            if(!currentInput) return alert("Vui lòng nhập mã SKU cần tìm!");
            window.location.href = "https://cooponline.vn/search?router=productListing&query=" + currentInput;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Tra SKU Co.opmart",
        "short_name": "Co.op SKU",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F2F8F5",
        "theme_color": "#76A998",
        "icons": [
            {
                "src": "https://i.imgur.com/8Q9Q9Q9.png", # THAY LINK ẢNH CỦA BẠN VÀO ĐÂY
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
