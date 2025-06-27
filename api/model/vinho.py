from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from typing import Union

from model import Base

class Vinho(Base):
    __tablename__ = 'vinho'
    
    id = Column(Integer, primary_key=True)
    fixed_acidity = Column(Float)
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    residual_sugar = Column(Float)
    chlorides = Column(Float)
    free_sulfur_dioxide = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    pH = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    quality = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self,
                 fixed_acidity: float,
                 volatile_acidity: float,
                 citric_acid: float,
                 residual_sugar: float,
                 chlorides: float,
                 free_sulfur_dioxide: float,
                 total_sulfur_dioxide: float,
                 density: float,
                 pH: float,
                 sulphates: float,
                 alcohol: float,
                 quality: int,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um registro de Vinho

        Args:
            fixed_acidity: acidez fixa
            volatile_acidity: acidez volátil
            citric_acid: ácido cítrico
            residual_sugar: açúcar residual
            chlorides: cloretos
            free_sulfur_dioxide: dióxido de enxofre livre
            total_sulfur_dioxide: dióxido de enxofre total
            density: densidade
            pH: pH
            sulphates: sulfatos
            alcohol: teor alcoólico
            quality: qualidade (nota)
            data_insercao: data de inserção no banco (opcional)
        """
        self.fixed_acidity = fixed_acidity
        self.volatile_acidity = volatile_acidity
        self.citric_acid = citric_acid
        self.residual_sugar = residual_sugar
        self.chlorides = chlorides
        self.free_sulfur_dioxide = free_sulfur_dioxide
        self.total_sulfur_dioxide = total_sulfur_dioxide
        self.density = density
        self.pH = pH
        self.sulphates = sulphates
        self.alcohol = alcohol
        self.quality = quality
        
        if data_insercao:
            self.data_insercao = data_insercao
