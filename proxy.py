from flask import Flask, request, Response, render_template_string
import requests

app = Flask(__name__)

# Set a password to restrict proxy access
AUTH_KEY = "hello"

# HTML for search bar
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Proxy</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        input, button { font-size: 18px; padding: 10px; margin: 5px; }
    </style>
</head>
<body>
    <h2>Web Proxy</h2>
    <form action="/proxy" method="get">
        <input type="text" name="url" placeholder="Enter URL" required size="50">
        <input type="password" name="auth" placeholder="Enter Password" required>
        <button type="submit">Go</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    auth = request.args.get('auth')

    if auth != AUTH_KEY:
        return "Unauthorized: Invalid Password", 403

    if not url:
        return "Error: No URL provided!", 400

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type', 'text/html'))
    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
