from app import app
import os


if __name__ == "__main__":
    app.run(debug=False, host='udownloadr.herokuapp.com', port=int(os.environ.get("PORT", 8323)))