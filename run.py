from app import app
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run(debug = False, host = "0.0.0.0", port = 80)
    elif len(sys.argv) == 2 and sys.argv[1] == "debug":
        app.run(debug = True, host = "0.0.0.0", port = 80)
