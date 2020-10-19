import app
import waitress

if __name__ == "__main__":
    server = app.create_app()
    waitress.serve(app, host='0.0.0.0', port=5200,)
    # server.run(host='0.0.0.0', port=5200, debug=True)