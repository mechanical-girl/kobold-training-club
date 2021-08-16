from waitress import serve
import ktc.app
serve(ktc.app.app, host="0.0.0.0", port=8080)
