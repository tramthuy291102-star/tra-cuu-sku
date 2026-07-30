from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tra SKU Co.op Nhanh</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        :root {
            --bg: #F2F4F7;
            --primary: #0063D1;
            --text: #1A1A1A;
            --gray: #8A92A6;
            --card-bg: #FFFFFF;
            --red: #E53935;
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
    </style>
</head>
<body>
    <div class="header">NHẬP SKU CO.OP THỐNG NHẤT</div>
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
        <button class="btn btn-search" onclick="searchSKU()">TRA CỨU NGAY</button>
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
            // Chuyển hướng trực tiếp trên chính tab hiện tại sang trang Co.opmart
            window.location.href = "https://cooponline.vn/search?router=productListing&query=" + currentInput;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
