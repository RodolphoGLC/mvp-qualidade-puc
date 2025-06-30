from model import PreProcessadorVinho
from model.vinho import Vinho
from schemas import apresenta_vinhos, apresenta_vinhos

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *

from flask_cors import CORS

# Instanciando o objeto OpenAPI
info = Info(title="Minha API de Vinhos", version="1.0.0")
app = OpenAPI(__name__, info=info, static_folder='../front',
              static_url_path='/front')
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
vinho_tag = Tag(
    name="Vinho", description="Adição, visualização, remoção e predição de vinhos")


# Rota home - redireciona para o frontend
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect('/front/index.html')


# Rota para documentação OpenAPI
@app.get('/docs', tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


# Rota de listagem de vinhos
@app.get('/vinhos', tags=[vinho_tag],
         responses={"200": VinhoViewSchema, "404": ErrorSchema})
def get_vinhos():
    """Lista todos os vinhos cadastrados na base"""
    logger.debug("Coletando dados sobre todos os vinhos")
    session = Session()
    vinhos = session.query(Vinho).all()

    if not vinhos:
        return {"vinhos": []}, 200
    else:
        logger.debug(f"%d vinhos encontrados" % len(vinhos))
        print(vinhos)
        return apresenta_vinhos(vinhos), 200


# Rota para adicionar vinho
@app.post('/vinho', tags=[vinho_tag],
          responses={"200": VinhoViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_vinho(form: VinhoSchema):
    """Adiciona um novo vinho à base de dados"""

    preprocessador = PreProcessadorVinho()
    pipeline = Pipeline()

    # Preparando os dados para o modelo
    X_input = preprocessador.preparar_form(form)

    # Carregando modelo
    model_path = './MachineLearning/pipelines/pipeline_wine_svm.pkl'
    modelo = pipeline.carrega_pipeline(model_path)

    # Realizando predição de quality
    quality = int(modelo.predict(X_input)[0])

    vinho = Vinho(
        fixed_acidity=form.fixed_acidity,
        volatile_acidity=form.volatile_acidity,
        citric_acid=form.citric_acid,
        residual_sugar=form.residual_sugar,
        chlorides=form.chlorides,
        free_sulfur_dioxide=form.free_sulfur_dioxide,
        total_sulfur_dioxide=form.total_sulfur_dioxide,
        density=form.density,
        pH=form.pH,
        sulphates=form.sulphates,
        alcohol=form.alcohol,
        quality=quality
    )

    logger.error("Vinho", vinho)

    logger.debug(f"Adicionando vinho com qualidade prevista: {quality}")

    try:
        session = Session()

        session.add(vinho)
        session.commit()

        logger.debug(f"Adicionado vinho com id: {vinho.id}")
        return apresenta_vinho(vinho), 200

    except Exception as e:
        error_msg = "Não foi possível salvar novo vinho :/"
        logger.warning(f"Erro ao adicionar vinho, {error_msg} Erro: {str(e)}")
        return {"message": error_msg}, 400


# Busca vinho por id (ou por outro critério que preferir)
@app.get('/vinho', tags=[vinho_tag],
         responses={"200": VinhoViewSchema, "404": ErrorSchema})
def get_vinho(query: VinhoBuscaSchema):
    """Busca um vinho cadastrado na base a partir do id"""

    vinho_id = query.id
    logger.debug(f"Buscando vinho #{vinho_id}")
    session = Session()
    vinho = session.query(Vinho).filter(Vinho.id == vinho_id).first()

    if not vinho:
        error_msg = f"Vinho #{vinho_id} não encontrado na base :/"
        logger.warning(error_msg)
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Vinho encontrado: id {vinho.id}")
        return apresenta_vinho(vinho), 200


# Remover vinho por id
@app.delete('/vinho', tags=[vinho_tag],
            responses={"200": VinhoViewSchema, "404": ErrorSchema})
def delete_vinho(query: VinhoBuscaSchema):
    """Remove um vinho cadastrado na base a partir do id"""

    vinho_id = query.id
    logger.debug(f"Deletando vinho #{vinho_id}")

    session = Session()
    vinho = session.query(Vinho).filter(Vinho.id == vinho_id).first()

    if not vinho:
        error_msg = "Vinho não encontrado na base :/"
        logger.warning(error_msg)
        return {"message": error_msg}, 404
    else:
        session.delete(vinho)
        session.commit()
        logger.debug(f"Deletado vinho #{vinho_id}")
        return {"message": f"Vinho #{vinho_id} removido com sucesso!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
