from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra SKU Co.op - Thùy Trâm</title>
    
    <!-- Cấu hình PWA ra màn hình chính -->
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#4EA8DE">
    
    <!-- Icon màn hình chính lấy từ ảnh anime bạn gửi -->
    <link rel="apple-touch-icon" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg"> 
    <link rel="icon" type="image/png" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800&family=Quicksand:wght@600;700&display=swap');
        
        :root {
            --sky-blue: #4EA8DE;
            --grass-green: #52B788;
            --pastel-yellow: #FFD166;
            --text-dark: #2B2D42;
            --card-bg: rgba(255, 255, 255, 0.92);
            --shadow: 0 12px 35px rgba(78, 168, 222, 0.25);
            --red: #FF6B6B;
            --orange: #FFB703;
        }

        body { 
            font-family: 'Nunito', sans-serif; 
            padding: 20px 15px; 
            /* Nền gradient tươi tắn lấy cảm hứng từ mây trời & đồng cỏ anime */
            background: linear-gradient(135deg, #E0F4FF 0%, #EAFDF8 50%, #FFF9E6 100%);
            color: var(--text-dark);
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
            touch-action: manipulation;
            background-attachment: fixed;
        }

        /* Khung thông tin chủ nhân web (Thùy Trâm) */
        .owner-banner {
            display: flex;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            border-radius: 50px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.06);
            margin-bottom: 18px;
            border: 2px solid #BEE1E6;
            gap: 10px;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }

        .owner-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--sky-blue);
        }

        .owner-name {
            font-family: 'Quicksand', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #2D6A4F;
            letter-spacing: 0.5px;
        }
        
        .header {
            font-family: 'Quicksand', sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: #0077B6;
            margin-bottom: 15px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            text-align: center;
        }

        #display-container {
            width: 100%;
            max-width: 360px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 2px solid #FFFFFF;
            border-radius: 24px;
            padding: 22px 20px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
            text-align: center;
            box-sizing: border-box;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #display { 
            font-family: 'Quicksand', sans-serif;
            font-size: 32px; 
            font-weight: 700;
            color: var(--text-dark);
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
            border: 2px solid rgba(255, 255, 255, 0.9); 
            border-radius: 20px; 
            font-family: 'Quicksand', sans-serif;
            font-size: 24px; 
            font-weight: 700; 
            padding: 16px 0; 
            cursor: pointer; 
            color: var(--text-dark);
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            transition: all 0.15s ease;
        }
        .btn:active { 
            transform: scale(0.92); 
            background: #D8F3DC; 
        }
        
        .btn-action { font-size: 14px; font-weight: 800; }
        .btn-del-all { color: var(--red); background: #FFE5E5; border-color: #FFC9C9; }
        .btn-del-one { color: #D4A373; background: #FEFAE0; border-color: #FAEDCD; }
        
        .btn-search { 
            background: linear-gradient(135deg, #4EA8DE 0%, #52B788 100%); 
            color: white; 
            border: none;
            grid-column: span 3; 
            padding: 18px 0; 
            border-radius: 20px;
            font-family: 'Quicksand', sans-serif;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
            box-shadow: 0 8px 22px rgba(82, 183, 136, 0.35);
            transition: all 0.2s ease;
        }
        .btn-search:active { 
            transform: scale(0.97);
            background: linear-gradient(135deg, #3A86EF 0%, #40916C 100%); 
        }

        .footer-note {
            margin-top: 20px;
            font-size: 12px;
            color: #6C757D;
            text-align: center;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Khu vực thể hiện chủ nhân web -->
    <div class="owner-banner">
        <img class="owner-avatar" src="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg" alt="Avatar">
        <span class="owner-name">✨ Web của Thùy Trâm ✨</span>
    </div>

    <div class="header">☁️ Co.opmart Thống Nhất ☁️</div>
    
    <div id="display-container">
        <div id="display" style="color: #8D99AE; font-size: 15px; font-weight: 600; letter-spacing: 0.5px;">Chạm để nhập mã SKU...</div>
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
        <button class="btn btn-action btn-del-one" onclick="deleteLast()">XÓA</button>
        <button class="btn btn-search" onclick="searchSKU()">🌸 TRA CỨU NGAY 🌸</button>
    </div>

    <div class="footer-note">🌿 Anime Sky & Field Edition 🌿</div>

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
                display.innerText = "Chạm để nhập mã SKU...";
                display.style.color = "#8D99AE";
                display.style.fontSize = "15px";
                display.style.fontWeight = "600";
                display.style.letterSpacing = "0.5px";
            } else {
                display.innerText = currentInput; 
                display.style.color = "var(--text-dark)";
                display.style.fontSize = "32px";
                display.style.fontWeight = "700";
                display.style.letterSpacing = "3px";
            }
        }
        function searchSKU() {
            if(!currentInput) return alert("Bé Trâm ơi, bạn chưa nhập mã SKU kìa! 💕");
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
        "name": "Tra SKU Co.op - Thùy Trâm",
        "short_name": "Co.op Trâm",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#E0F4FF",
        "theme_color": "#4EA8DE",
        "icons": [
            {
                "src": "https://i.pinimg.com/1200x/24/c4/3c/24c43c01aa81204cda2c6fa84c58a264.jpg",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
