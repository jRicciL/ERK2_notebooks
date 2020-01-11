import numpy as np 
import pandas as pd  
import matplotlib.pyplot as plt

class Pareto:
    def __init__(self, df_scores, methods, minimize = True):
        self.methods = methods
        self.df_scores = df_scores
        self.counter = 0
        self.minimize = minimize
        self.fronts_dic = {}

    def pareto_front(self, scores):
        ''' Función para determinar si una observación pertenece 
        al frente no dominado dado un arreglo de n_observaciones, 
        y m_scores de las funciones objetivo.
        '''
        # Se crea un arreglo inicial de tamaño igual al número de observaciones
        # Todos los elementos se inicializan como parte del frente no dominado ( = 1)
        pareto_front = np.ones(scores.shape[0], dtype = bool)
        # Se itera sobre cada observación
        # Comprueba si el punto i domina a los demás elementos
        n_points = scores.shape[0]
        for i in range(n_points):
            for j in range(n_points):
                # j domina a i si y sólo si es mejor o igual a i en todos los scores
                # (dimensiones), y si es mejor en al menos uno de los scores
                if all(scores[j] >= scores[i]) and any(scores[j] > scores[i]):
                    # Si j domina a i, i no está en el frente no dominado
                    pareto_front[i] = 0
                    break
        return pareto_front
    
    def get_front(self, df_scores):
        scores_sub_mtx = df_scores[self.methods].to_numpy()
        if self.minimize:
            scores_sub_mtx = scores_sub_mtx*-1
        pareto_points = self.pareto_front(scores_sub_mtx) # Se calculan lso scores
        df_pareto = df_scores[pareto_points]
        return(df_pareto)
    
    def get_pareto_front(self):
        df_pareto = self.get_front(self.df_scores)
        return(df_pareto)
    
    def get_all_fronts(self, df_scores = None, just_actives = True, retorno = True):
        if df_scores is None:
            df_scores = self.df_scores
        df_pf = self.get_front(df_scores)
        efficient_confs = df_pf.index.to_numpy()
        if len(efficient_confs) > 0:
            is_active = df_pf['Activity']
            self.counter = self.counter + 1
            self.fronts_dic[F'{self.counter}'] = efficient_confs
            if np.any(is_active) or not just_actives:
                df_scores = df_scores.drop(efficient_confs)
                self.get_all_fronts(df_scores, just_actives = just_actives)
        return(self.fronts_dic)
    
    def get_num_of_actives_per_front(self):
        print(F'Número total de frentes: {len(self.fronts_dic)}')
        print("___________________________________")
        for frente, puntos in self.fronts_dic.items():
            puntos_df = self.df_scores.loc[puntos][['Activity']]
            n_elementos = ( puntos_df.count())[0]
            n_activos = puntos_df.sum()[0]
            print(F'Frente {frente}: {n_activos}/{n_elementos} activos.')
            print(puntos_df.T)
            print("___________________________________")


    def plot_pareto_front(self, n_frentes = None, just_actives = True):
        if not self.fronts_dic:
            self.get_all_fronts(retorno = False, just_actives = just_actives)
        _n_frentes = len(self.fronts_dic.keys())
        if n_frentes is None or (n_frentes > _n_frentes):
            n_frentes = _n_frentes
        plt.figure(figsize=(7, 7))
        for frente in range(1, n_frentes + 1):
            index = self.fronts_dic[str(frente)]
            df = self.df_scores.loc[index]
            sns.lineplot(df[self.methods[0]], df[self.methods[1]], drawstyle='steps-post')
        pareto_points = self.pareto_front(self.df_scores[self.methods].to_numpy())
        sns.scatterplot(self.df_scores[self.methods[0]], self.df_scores[self.methods[1]], 
                        hue = self.df_scores['Activity'], s=70, palette = ["#50DAB4", "#FA5F50"],
                       zorder=100)
        plt.show()