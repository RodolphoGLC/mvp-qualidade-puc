from pydantic import BaseModel, Field
from typing import List
from model.vinho import Vinho

class VinhoSchema(BaseModel):
    """ Define como um novo vinho a ser inserido deve ser representado """
    fixed_acidity: float = Field(..., example=7.4)
    volatile_acidity: float = Field(..., example=0.7)
    citric_acid: float = Field(..., example=0.01)
    residual_sugar: float = Field(..., example=1.9)
    chlorides: float = Field(..., example=0.076)
    free_sulfur_dioxide: float = Field(..., example=11.0)
    total_sulfur_dioxide: float = Field(..., example=34.0)
    density: float = Field(..., example=0.9978)
    pH: float = Field(..., example=3.51)
    sulphates: float = Field(..., example=0.56)
    alcohol: float = Field(..., example=9.4)

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
    id: int

class ListaVinhosSchema(BaseModel):
    """ Define como representar uma coleção de vinhos """
    vinhos: List[VinhoViewSchema]

class VinhoDelSchema(BaseModel):
    """ Define como representar a remoção de um vinho """
    id: int


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
