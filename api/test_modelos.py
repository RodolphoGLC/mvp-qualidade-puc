from model import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
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
array = dataset.values
X = array[:, :-1]
y = array[:, -1]

# Separação dos dados para validação justa
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def test_modelo_bag():
    # Caminho do modelo
    model_path = './MachineLearning/models/bag_wine_model.pkl'
    
    # Carrega o modelo treinado
    modelo_bag = modelo.carrega_modelo(model_path)

    # Predição nos dados de teste
    y_pred = modelo_bag.predict(X_test)

    # Cálculo das métricas
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # Impressão das métricas em caso de falha
    if acc < 0.4 or prec < 0.3 or rec < 0.4:
        print("\n---- Avaliação do modelo Bagging ----")
        print(f"Acurácia: {acc:.3f}")
        print(f"Precisão: {prec:.3f}")
        print(f"Recall: {rec:.3f}")
        print("--------------------------------------")

    # Asserts com limiares ajustáveis
    assert acc >= 0.4
    assert prec >= 0.3
    assert rec >= 0.4