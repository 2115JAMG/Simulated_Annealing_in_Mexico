import geopandas
import matplotlib.pyplot as plt
import pandas as pd
from anneal import SimAnneal
import sys

mex = geopandas.read_file("mexican-states.shp")

print('\n=====================================\n')
print('\nGenerating maps')
print('\n=====================================\n')

"""
parameter setting for the graph
"""
fig,ax = plt.subplots(1,1,figsize=(10,8))
mex.plot(ax = ax)

# Centroid
x0 = -102.57634952
y0 = 23.9353719


mex_tr = mex["geometry"]

# Capitals in sort by alphabetic order of states
Republica =            [['Aguascalientes',21.880833, -102.296111,'Aguascalientes'], 
                       ['Mexicali',32.663333,-115.467778, 'Baja California Norte'], 
                       ['La Paz ',24.142222,-110.310833, 'Baja California Sur'], 
                       ['San Francisco de Campeche',19.848611,-90.525278, 'Campeche'], 
                       ['Tuxtla Gutiérrez',16.753056, -93.115556,'Chiapas'], 
                       ['Chihuahua',28.635278,-106.088889,'Chihuahua'],
                       ['Saltillo',25.433333,-101, 'Coahuila de Zaragoza'], 
                       ['Colima',19.243611,-103.730833,'Colima'], 
                       ['Victoria de Durango',24.022778,-104.654444,'Durango'], 
                       ['Guanajuato',21.017778,-101.256667,'Guanajuato'], 
                       ['Chilpancingo de los Bravo',17.551389,-99.500833,'Guerrero'], 
                       ['Pachuca de Soto',20.1225, -98.736111,'Hidalgo'], 
                       ['Guadalajara',20.676667,-103.3475,'Jalisco'], 
                       ['Toluca de Lerdo',19.292222,-99.653889,'México'], 
                       ['Morelia',19.768333,-101.189444,'Michoacán de Ocampo'], 
                       ['Cuernavaca',18.918611,-99.234167,'Morelos'], 
                       ['Tepic',21.5,-104.9,'Nayarit'], 
                       ['Monterrey',25.671389,-100.308611,'Nuevo León'], 
                       ['Oaxaca de Juárez',17.083333, -96.75,'Oaxaca'], 
                       ['Puebla de Zaragoza',19.051389,-98.217778,'Puebla'], 
                       ['Santiago de Querétaro',20.588056,-100.388056,'Querétaro'], 
                       ['Chetumal',18.503611,-88.305278,'Quintana Roo'], 
                       ['San Luis Potosí',22.149722,-100.975,'San Luis Potosí'], 
                       ['Culiacán Rosales',24.8,-107.383333,'Sinaloa'], 
                       ['Hermosillo',29.095556,-110.950833,'Sonora'], 
                       ['Villahermosa',17.986944,-92.919444,'Tabasco'], 
                       ['Ciudad Victoria',23.736111,-99.146111,'Tamaulipas'], 
                       ['Tlaxcala de Xicohténcatl',19.31695,-98.238231,'Tlaxcala'], 
                       ['Xalapa-Enríquez',19.54,-96.9275, 'Veracruz de Ignacio de la Llave'], 
                       ['Mérida',20.97, -89.62,'Yucatán'], 
                       ['Zacatecas',22.771667,-102.575278,'Zacatecas'], 
                       ['Ciudad de Mexico',19.419444,-99.145556,'D.F.']]

Republica = pd.DataFrame(Republica,
                       columns=['Nombre','Lat','Long','Estados'])



fig,ax = plt.subplots(1,1,figsize=(10,8))

#Plot map
mex_tr.plot(ax=ax,
            color="#ffffff",
            edgecolor="#bcbcbc",
            zorder=1)

#Coord position
ax.scatter(x=Republica['Long'],
           y=Republica['Lat'],
           color="#ff944d")
plt.show()

# Sort the capital by order
coords = []
cont = 0
for g in range(len(Republica)):
    cont = cont + 1  
    nuevo = Republica['Lat'][g],Republica['Long'][g]
    num = cont,nuevo[0],nuevo[1]
    coords.append(num)


# Start the algorithm
if __name__ == "__main__":
    sa = SimAnneal(coords)
    sa.anneal()
    sa.visualize_routes()
    sa.plot_learning()
    print('\n=====================================\n')
    print('\nWhat is the value of N for show the N-capitals?')
    n = input()
    sa.list_of_capitals(n, Republica)
    if int(n) >= 33:
        print('\nMéxico only have 32 capitals')
        sys.exit()
    if int(n)<=10:
        if int(n)>=2:
            sa.brute_force(n, Republica)
            sa.visualize_routes2()
        else:
             print('\nI need almost 2 capital for the comparative with Brute force')
    else:
        print('\nBy brute force greater than 10 the computation can be very slow...')