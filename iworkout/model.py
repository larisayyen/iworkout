
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

class Trainer():

    def __init__(self,X,y):
        self.X = X
        self.y = y

    def split(self):

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=2)

        return X_train, X_test, y_train, y_test

    def run(self):

        model = make_pipeline(StandardScaler(),RandomForestClassifier())

        return model

    def evaluate(self,X_test,y_test,model):

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test,y_pred)

        return accuracy

    def save_model(self,model):

        with open("pipeline3.pkl", "wb") as file:
            pickle.dump(model, file)

if __name__ == "__main__":
    df = pd.read_csv('fitness_poses_csvs_out_basic(5).csv')

    X = df.drop('class', axis=1) # features
    y = df['class'] # target value

    trainer = Trainer(X,y)

    X_train,X_test,y_train,y_test = trainer.split()
    print(X_test.shape)

    print('Fitting')
    model = trainer.run()
    model.fit(X_train,y_train)

    print('Cross Validation')
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy').mean()
    print(score)

    print('Evaluating')
    acc = trainer.evaluate(X_test,y_test,model)
    print(acc)

    print('Saving')
    trainer.save_model(model)
