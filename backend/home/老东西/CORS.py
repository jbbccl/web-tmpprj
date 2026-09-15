from fastapi.middleware.cors import CORSMiddleware
def cors(app):
    app.add_middleware(
        CORSMiddleware,    
        allow_origins= "http://192.168.86.137:5173/",    
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],    
    )