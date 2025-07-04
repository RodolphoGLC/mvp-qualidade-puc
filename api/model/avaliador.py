from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class Avaliador:
    def __init__(self):
        pass

    def avaliar(self, model, X_test, y_test):
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        return {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "y_pred": y_pred
        }
                
