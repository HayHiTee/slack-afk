import app


if __name__ == "__main__":
    server = app.create_app()
    server.run(host='0.0.0.0', port=5200, debug=True)