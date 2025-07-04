from sklearn.metrics import accuracy_score

class Avaliador:
    
    def __init__(self):
        """Inicializa o avaliador"""
        pass

    def avaliar(self, model, X_test, Y_test):
        """ Faz uma predição e avalia o modelo.
        """
        predicoes = model.predict(X_test)
        
        return accuracy_score(Y_test, predicoes)
                
