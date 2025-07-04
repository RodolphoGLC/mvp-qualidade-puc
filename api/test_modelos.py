from model import *
from sklearn.metrics import classification_report

# Instanciação das Classes
carregador = Carregador()
preprocessador = PreProcessadorVinho()
modelo = Model()
avaliador = Avaliador()
pipeline = Pipeline()

# Parâmetros    
url_dados = "./MachineLearning/data/test_database_wine.csv"
colunas = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
           'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide',
           'density', 'pH', 'sulphates', 'alcohol', 'quality']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Separação dos dados
X_train, X_test, y_train, y_test = preprocessador.separa_teste_treino(dataset, 0.20)

# Normalização com scaler treinado
X_test_scaled = preprocessador.scaler(X_test)

def test_modelo_bag():
    # Caminho do modelo treinado
    model_path = './MachineLearning/models/bag_wine_model.pkl'
    
    # Carrega o modelo
    modelo_bag = modelo.carrega_modelo(model_path)

    # Avalia o modelo com métricas completas
    resultados = avaliador.avaliar(modelo_bag, X_test_scaled, y_test)

    if resultados['accuracy'] > 0.7:
        print("\n---- Avaliação do modelo Bagging ----")
        print(f"Acurácia:  {resultados['accuracy']:.3f}")
        print(f"Precisão:  {resultados['precision']:.3f}")
        print(f"Recall:    {resultados['recall']:.3f}")
        print(f"F1-score:  {resultados['f1']:.3f}")
        print("--------------------------------------")

        # print(classification_report(y_test, resultados['y_pred']))

    # Asserts opcionais
    assert resultados["accuracy"] >= 0.7
    assert resultados["precision"] >= 0.3
    assert resultados["recall"] >= 0.3
    assert resultados["f1"] >= 0.3