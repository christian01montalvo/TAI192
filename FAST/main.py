from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional,List
from modelsPydantic import Usuario, modeloAuth
from genToken import crearToken
from middlewares import BearerJWT
app = FastAPI(
    title="Mi primera API 192",
    description="Maria Monserrat Campuzano Leon",
    version="1.0.1"
)

# Lista de usuarios simulando una base de datos
lista_usuarios = [
    {"id": 1, "nombre": "monchis", "edad": 22, "correo": "example@example.com"},
    {"id": 2, "nombre": "alejandro", "edad": 24, "correo": "example2@example.com"},
    {"id": 3, "nombre": "maria", "edad": 20, "correo": "example3@example.com"},
    {"id": 4, "nombre": "felix", "edad": 23, "correo": "example4@example.com"}
]
 #endpoint auteticacion
@app.post("/auth", tags=["autetificacion"])
def login(autorizacion:modeloAuth):
    if autorizacion.email =='christian@example.com' and autorizacion.passw == '123456789':
       token:str = crearToken(autorizacion.model_dump())
       print(token)
       return JSONResponse(content= token) 
    else:
       return{"aviso":"usuario no autorizado"}     


# Endpoint de inicio
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a FastAPI."}


# Obtener todos los usuarios
@app.get("/usuarios", dependencies=[Depends(BearerJWT())], response_model=List[Usuario], tags=["Operaciones CRUD"])
def obtener_usuarios():
    return lista_usuarios



# Agregar un nuevo usuario
@app.post("/usuarios", response_model=Usuario, tags=["Operaciones CRUD"])
def agregar_usuario(usuario: Usuario):
    for usr in lista_usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El ID ya existe.")
    lista_usuarios.append(usuario.model_dump())
    return usuario



# Actualizar usuario 
@app.put("/usuarios/{id_usuario}", response_model=Usuario, tags=["Operaciones CRUD"])
def actualizar_usuario(id_usuario: int, usuarioActualizar: Usuario):
    for i, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            lista_usuarios[i] = usuarioActualizar.model_dump()
            return lista_usuarios[i]
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")



# Endpoint Agregar Usuarios DELETE
@app.delete("/usuario/{id_usuario}", tags=["Operaciones CRUD"])
def deleteUsuario(id_usuario: int):
    for index, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            lista_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado correctamente."}
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")






