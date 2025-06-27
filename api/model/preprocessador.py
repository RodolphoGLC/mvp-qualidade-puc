from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class PreProcessadorVinho:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers (se necessário)

        # feature selection (se necessário)

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                  percentual_teste,
                                                                  seed)
        # normalização/padronização
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando holdout.
        Assume que a variável target está na última coluna.
        """
        dados = dataset.values
        X = dados[:, 0:-1]  # todas as colunas menos a última
        Y = dados[:, -1]    # última coluna = quality
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo.
            Espera um objeto form com os atributos do vinho, sem quality (target).
        """
        X_input = np.array([
            form.fixed_acidity,
            form.volatile_acidity,
            form.citric_acid,
            form.residual_sugar,
            form.chlorides,
            form.free_sulfur_dioxide,
            form.total_sulfur_dioxide,
            form.density,
            form.pH,
            form.sulphates,
            form.alcohol
        ])
        # Reshape para o modelo entender (1 amostra, N features)
        X_input = X_input.reshape(1, -1)
        return X_input
    
    def scaler(self, X_train):
        """ Normaliza os dados usando scaler previamente salvo. """
        scaler = pickle.load(open('./MachineLearning/scalers/scaler_wine.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train
