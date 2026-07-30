from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra SKU Co.opmart</title>
    
    <!-- Cấu hình PWA đưa ra màn hình chính -->
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#76A998">
    <link rel="apple-touch-icon" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg"> 
    <link rel="icon" type="image/png" href="https://i.pinimg.com/736x/5e/6f/2f/5e6f2ffe4f0028c1804c57bb4d527e6c.jpg">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Quicksand:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        :root {
            --bg-gradient: radial-gradient(circle at top, #F4F8F5 0%, #E2ECE7 100%);
            --primary: #76A998; 
            --primary-hover: #619382;
            --text: #2C3E35;
            --gray: #8A9E93;
            --card-bg: rgba(255, 255, 255, 0.9);
            --shadow: 0 15px 35px rgba(118, 169, 152, 0.15);
            --red: #D97777;
            --orange: #D99B6A;
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
        
        .header-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 22px;
        }

        .floral-icon {
            width: 24px;
            height: 24px;
            fill: var(--primary);
            opacity: 0.85;
        }

        .header {
            font-family: 'Quicksand', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: 2.5px;
            text-transform: uppercase;
        }

        #display-container {
            width: 100%;
            max-width: 360px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 24px 20px;
            box-shadow: var(--shadow);
            margin-bottom: 22px;
            text-align: center;
            box-sizing: border-box;
            min-height: 85px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        #display-container::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 4px; height: 100%;
            background: var(--primary);
        }

        #display { 
            font-family: 'Cinzel', serif;
            font-size: 32px; 
            font-weight: 600;
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
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 255, 255, 0.8); 
            border-radius: 18px; 
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
            background: rgba(118, 169, 152, 0.18); 
        }
        
        .btn-action { font-size: 15px; font-weight: 700; letter-spacing: 0.5px;}
        .btn-del-all { color: var(--red); background: rgba(217, 119, 119, 0.05); }
        .btn-del-one { color: var(--orange); background: rgba(217, 155, 106, 0.05); }
        
        .btn-search { 
            background: linear-gradient(135deg, #76A998 0%, #5E8F7F 100%); 
            color: white; 
            border: none;
            grid-column: span 3; 
            padding: 18px 0; 
            border-radius: 18px;
            font-family: 'Quicksand', sans-serif;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: 1.5px;
            box-shadow: 0 8px 22px rgba(118, 169, 152, 0.35);
            transition: all 0.2s ease;
        }
        .btn-search:active { 
            transform: scale(0.97);
            background: linear-gradient(135deg, #619382 0%, #4C7567 100%); 
        }

        .footer-note {
            margin-top: 25px;
            font-size: 11px;
            color: var(--gray);
            text-align: center;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <!-- Biểu tượng hoa trang trí tinh tế -->
        <svg class="floral-icon" viewBox="0 0 24 24"><path d="M12,2C11.5,5.5 9,8 5.5,8.5C9,9 11.5,11.5 12,15C12.5,11.5 15,9 18.5,8.5C15,8 12.5,5.5 12,2M19,14C18.7,16 17,17.7 15,18C17,18.3 18.7,20 19,22C19.3,20 21,18.3 23,18C21,17.7 19.3,16 19,14M5,12C4.7,13.5 3.5,14.7 2,15C3.5,15.3 4.7,16.5 5,18C5.3,16.5 6.5,15.3 8,15C6.5,14.7 5.3,13.5 5,12Z"/></svg>
        <div class="header">Co.opmart Thống Nhất</div>
        <svg class="floral-icon" viewBox="0 0 24 24"><path d="M12,2C11.5,5.5 9,8 5.5,8.5C9,9 11.5,11.5 12,15C12.5,11.5 15,9 18.5,8.5C15,8 12.5,5.5 12,2M19,14C18.7,16 17,17.7 15,18C17,18.3 18.7,20 19,22C19.3,20 21,18.3 23,18C21,17.7 19.3,16 19,14M5,12C4.7,13.5 3.5,14.7 2,15C3.5,15.3 4.7,16.5 5,18C5.3,16.5 6.5,15.3 8,15C6.5,14.7 5.3,13.5 5,12Z"/></svg>
    </div>
    
    <div id="display-container">
        <div id="display" style="color: var(--gray); font-size: 15px; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 500; letter-spacing: 0.5px;">Chạm để nhập mã SKU</div>
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
        <button class="btn btn-search" onclick="searchSKU()">TRA CỨU NGAY</button>
    </div>

    <div class="footer-note">✦ Botanical Anime Luxury Edition ✦</div>

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
                display.style.fontSize = "15px";
                display.style.fontFamily = "'Plus Jakarta Sans', sans-serif";
                display.style.fontWeight = "500";
                display.style.letterSpacing = "0.5px";
            } else {
                display.innerText = currentInput; 
                display.style.color = "var(--text)";
                display.style.fontSize = "32px";
                display.style.fontFamily = "'Cinzel', serif";
                display.style.fontWeight = "600";
                display.style.letterSpacing = "3px";
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
        "background_color": "#F4F8F5",
        "theme_color": "#76A998",
        "icons": [
            {
                "src": "https://i.imgur.com/8Q9Q9Q9.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
