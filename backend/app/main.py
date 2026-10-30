"""Punto de entrada de la API.

    cd backend
    uvicorn app.main:app --reload     # documentación interactiva en /docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errores import NoEncontradoError, ReglaNegocioError
from app.rutas import personal, portal, taller


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    from app.semilla import preparar_base
    preparar_base()
    yield


app = FastAPI(title="Sistema de Órdenes de Servicio y Citas",
              description="Servicio Automotriz Hermanos Ruiz · Equipo B · Release v0.1.0 (en desarrollo)",
              version="0.1.0-dev", lifespan=ciclo_de_vida)


@app.exception_handler(ReglaNegocioError)
def regla_violada(_: Request, exc: ReglaNegocioError):
    return JSONResponse(status_code=409, content={"detail": exc.mensaje, "regla": exc.regla})


@app.exception_handler(NoEncontradoError)
def no_encontrado(_: Request, exc: NoEncontradoError):
    return JSONResponse(status_code=404, content={"detail": exc.mensaje})


app.include_router(personal.router)
app.include_router(taller.router)
app.include_router(portal.router)


@app.get("/salud", tags=["Sistema"])
def salud():
    return {"estado": "ok"}
