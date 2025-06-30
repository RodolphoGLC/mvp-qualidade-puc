from pydantic import BaseModel
from typing import List
from model.vinho import Vinho

class VinhoSchema(BaseModel):
    """ Define como um novo vinho a ser inserido deve ser representado """
    fixed_acidity: float = 7.4
    volatile_acidity: float = 0.70
    citric_acid: float = 0.0
    residual_sugar: float = 1.9
    chlorides: float = 0.076
    free_sulfur_dioxide: float = 11.0
    total_sulfur_dioxide: float = 34.0
    density: float = 0.9978
    pH: float = 3.51
    sulphates: float = 0.56
    alcohol: float = 9.4

class VinhoViewSchema(BaseModel):
    """ Define como um vinho será retornado """
    id: int
    fixed_acidity: float 
    volatile_acidity: float 
    citric_acid: float 
    residual_sugar: float 
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float
    quality: int

class VinhoBuscaSchema(BaseModel):
    """ Define como representar a busca de um vinho (usando id) """
    id: int = 1

class ListaVinhosSchema(BaseModel):
    """ Define como representar uma coleção de vinhos """
    vinhos: List[VinhoViewSchema]

class VinhoDelSchema(BaseModel):
    """ Define como representar a remoção de um vinho """
    id: int = 1


# Funções auxiliares para representar dados no retorno

def apresenta_vinho(vinho: Vinho):
    """ Retorna uma representação de um vinho seguindo o schema definido em VinhoViewSchema """
    return {
        "id": vinho.id,
        "fixed_acidity": vinho.fixed_acidity,
        "volatile_acidity": vinho.volatile_acidity,
        "citric_acid": vinho.citric_acid,
        "residual_sugar": vinho.residual_sugar,
        "chlorides": vinho.chlorides,
        "free_sulfur_dioxide": vinho.free_sulfur_dioxide,
        "total_sulfur_dioxide": vinho.total_sulfur_dioxide,
        "density": vinho.density,
        "pH": vinho.pH,
        "sulphates": vinho.sulphates,
        "alcohol": vinho.alcohol,
        "quality": vinho.quality
    }

def apresenta_vinhos(vinhos: List[Vinho]):
    """ Retorna uma representação de uma coleção de vinhos """
    result = []
    for vinho in vinhos:
        result.append(apresenta_vinho(vinho))
    return {"vinhos": result}
