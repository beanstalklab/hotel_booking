from app import create_app


application = create_app()

if __name__ == "__main__":
    try:
        application.run(host='localhost', port=5000)
    except Exception as e:
        import traceback