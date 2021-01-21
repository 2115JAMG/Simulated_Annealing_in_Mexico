import matplotlib.pyplot as plt
import geopandas
#import os
#import imageio

#flag = 0

def plotTSP(paths, points, flag):
    
    """
    The graph of the Mexican Republic is generated with the points of the capitals
    followed by the path generated by S.A. or B.F.
    path: List of lists with the different orders in which the nodes are visited
    points: coordinates for the different nodes
    num_iters: number of paths that are in the path list

    """
    x = []; y = [] 
    for i in paths[0]:
        x.append(points[i][2])
        y.append(points[i][1])

  
    fig,ax = plt.subplots(1,1,figsize=(10,8))
    mex = geopandas.read_file("mexican-states.shp")
    mex.plot(ax = ax)
    mex_tr = mex["geometry"]

    # Map
    mex_tr.plot(ax=ax,
                color="#ffffff",
                edgecolor="#bcbcbc",
                zorder=1)
    # Coords
    ax.scatter(x,
               y,
               color="#ff944d")
    # Draw the primary arrow
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = 0.3,            
              color ='b')
    
    """
    # for a Gif remove comment quotes
    if flag >=1:
        i= -1
        # create file name and append it to a list
        filename = f'{i}.png'
        filenames.append(filename)
    
        # save frame
        plt.savefig(filename)
    """
    
    # Generate the following arrows on the path of S.A.
    for i in range(0,len(x)-1):
        """
        if flag >=1:
            #Graficando el mapa
            mex_tr.plot(ax=ax,
                        color="#ffffff",
                        edgecolor="#bcbcbc",
                        zorder=1)
            #Mostrando la posición de las coordenadas
            ax.scatter(x,
                       y,
                       color="#ff944d")
            plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = 0.2,
                      color = 'g')
            # create file name and append it to a list
            filename = f'{i}.png'
            filenames.append(filename)
    
            # save frame
            plt.savefig(filename)
            """   
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = 0.3,
                      color = 'g')
        
    """
    i=-2
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename)
    """
    plt.show()
    """
    if flag >=1:
        plt.close()
    # build gif
        with imageio.get_writer('mygif.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
        
        # Remove files
        for filename in set(filenames):
            os.remove(filename)
    """
 