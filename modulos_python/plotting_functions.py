from scipy.stats import gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpltcols
import matplotlib.patches as mpatches



def density_estimation(x, y, sort_points = True):
    '''Calcula la densidad de la distribución de los puntos en un espacio bidimensional x y
    utilizando la distribución gausiana, y devuelve los puntos x, y ordenados por su frecuencia,
    y un valor z con las frecucias asociadas a cada punto según su posición.'''
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)
    if sort_points:
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    return x, y, z

def plot_anotation_labels(list_of_all_index, list_of_ref_names, x, y, 
    marker='o', s = 90, c = "", 
    linewidths = 2.5, edgecolors = "black",
    xytext_delta = [0.2, 0.2],
    fontsize = 18):
    '''Recives a pandas dataframe index Series and a list of reference structures names'''
    ref_index = [list_of_all_index.get_loc(name) for name in  list_of_ref_names]
    x_ref_points = x[ref_index]
    y_ref_points = y[ref_index]
    plt.scatter(x = x_ref_points, y = y_ref_points, marker = marker, s = s, c = c, 
            linewidths = linewidths, edgecolors = edgecolors)
    for i, label in enumerate(list_of_ref_names):
        plt.annotate(label, xy = (x_ref_points[i], y_ref_points[i]), fontsize = fontsize, weight = 'bold',
                    arrowprops=dict(facecolor='black', shrink=0.1), 
                    xytext=(x_ref_points[i] - xytext_delta[0], y_ref_points[i]- xytext_delta[1]),
                    horizontalalignment='left', verticalalignment='bottom',)


def plot_mds_or_pca(mds, labels = None,
    colors_list = ['#E93523', '#23E9BC', '#23B537', '#036193', '#FEA50A', 'gray'],
    #dic_of_ref_labels = None,
    #traj_labels = None,
    alpha=0.6, fig_size = 7, refs_fontsize = 15,
    general_font_size = 16,
    point_size = 60,
    title = "Classic MDS",
    xlabel = "Primer componente",
    ylabel = "Segundo componente",
    legend = False,
    equal_axis = True,
    xy_lims = None):
    
    '''Genera una gráfica de dispersión en dos dimensiones dado un objeto de cDM.'''
    # Properties of the scatter plot
    colors = colors_list
    plt.rcParams.update({'font.size': general_font_size})
    plt.axhline(0, color='grey',  linestyle='--')
    plt.axvline(0, color='grey',  linestyle='--')
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize = 14)
    plt.ylabel(ylabel, fontsize = 14)


    if labels is not None:
        # Color by label
        name_labels =  list(np.unique( labels ))
        if len(colors_list) < len(name_labels):
                print(F'El número de colores en la lista ({len(colors_list)}) es menor al número único de etiquetas ({len(name_labels)}).')
                return None
        color_numeric_labels = range(len(name_labels))
        code_labels = dict(zip(name_labels, colors_list[:len(name_labels)]))
        color_labels = [ code_labels[i] for i in labels]
        
        for label in code_labels:
            if label != 'None':
                indices = np.where(label == labels)
                plt.scatter( mds[0][indices], mds[1][indices], marker='o', c = code_labels[label],  alpha=alpha, s= point_size)
        
        # plt.scatter( mds[0], mds[1], marker='o', c = color_labels,  alpha=alpha, s=60)
        
        if legend:
            patchList = []
            for key in code_labels:
                data_key = mpatches.Patch(color = code_labels[key], label=key)
                patchList.append(data_key)
            plt.legend(handles=patchList)
        
    else:
        plt.scatter( mds[0], mds[1], marker='o', c = colors_list[0], alpha=alpha, s=point_size)
    '''
    if dic_of_ref_labels is not None  and  traj_labels is not None:
        # Creates the refs label and its color
        name_ref_label, color_ref_label = zip(*[(i, dic_of_ref_labels[i])  if i in dic_of_ref_labels.keys() else ("None", "None") for i in traj_labels])
        # plots the labels of the given references indixes 
        for label, x, y in zip( name_ref_label, mds[0], mds[1]):
            if label != 'None':
                plt.scatter(x, y, marker='o', s=point_size, c = "None", linewidths = 1.5, edgecolors = "black")
                plt.annotate(label.split("_")[0], xy = (x, y), fontsize = refs_fontsize, weight = 'bold')
                '''
    if xy_lims is not None and len(xy_lims) == 4:
        plt.xlim(xy_lims[0], xy_lims[1])
        plt.ylim(xy_lims[2], xy_lims[3])
    if equal_axis:
        plt.axis('equal')
    plt.grid(linestyle='--')