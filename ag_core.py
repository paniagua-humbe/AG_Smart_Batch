import numpy as np
import random

MIN_CALLES_V = 2
MIN_CALLES_H = 2

def generar_calles_no_adyacentes(n, min_calles):
    posibles = list(range(1, n-1))
    random.shuffle(posibles)
    calles = []
    while posibles and len(calles) < min_calles:
        c = posibles.pop()
        if all(abs(c - x) > 1 for x in calles):
            calles.append(c)
    calles.sort()
    return calles

def generar_individuo(n):
    calles_v = generar_calles_no_adyacentes(n, MIN_CALLES_V)
    calles_h = generar_calles_no_adyacentes(n, MIN_CALLES_H)
    individuo = {
        'calles_v': calles_v,
        'calles_h': calles_h
    }
    return individuo

def mutar(individuo, n):
    nuevo = {'calles_v': individuo['calles_v'][:], 'calles_h': individuo['calles_h'][:]}
    # Muta verticales
    if random.random() < 0.5 and len(nuevo['calles_v']) > MIN_CALLES_V:
        nuevo['calles_v'].remove(random.choice(nuevo['calles_v']))
    elif random.random() < 0.5 and len(nuevo['calles_v']) < n-2:
        posibles = set(range(1, n-1)) - set(nuevo['calles_v'])
        posibles = [c for c in posibles if all(abs(c - x) > 1 for x in nuevo['calles_v'])]
        if posibles:
            nuevo['calles_v'].append(random.choice(posibles))
    # Muta horizontales
    if random.random() < 0.5 and len(nuevo['calles_h']) > MIN_CALLES_H:
        nuevo['calles_h'].remove(random.choice(nuevo['calles_h']))
    elif random.random() < 0.5 and len(nuevo['calles_h']) < n-2:
        posibles = set(range(1, n-1)) - set(nuevo['calles_h'])
        posibles = [c for c in posibles if all(abs(c - x) > 1 for x in nuevo['calles_h'])]
        if posibles:
            nuevo['calles_h'].append(random.choice(posibles))
    nuevo['calles_v'] = sorted(nuevo['calles_v'])
    nuevo['calles_h'] = sorted(nuevo['calles_h'])
    return nuevo

def cruzar(ind1, ind2, n):
    hijo = {
        'calles_v': sorted(list(set(ind1['calles_v'][:len(ind1['calles_v'])//2] + ind2['calles_v'][len(ind2['calles_v'])//2:]))),
        'calles_h': sorted(list(set(ind1['calles_h'][:len(ind1['calles_h'])//2] + ind2['calles_h'][len(ind2['calles_h'])//2:])))
    }
    # Garantizar mínimo y no adyacentes
    while len(hijo['calles_v']) < MIN_CALLES_V:
        posibles = set(range(1, n-1)) - set(hijo['calles_v'])
        posibles = [c for c in posibles if all(abs(c - x) > 1 for x in hijo['calles_v'])]
        if posibles:
            hijo['calles_v'].append(random.choice(posibles))
    while len(hijo['calles_h']) < MIN_CALLES_H:
        posibles = set(range(1, n-1)) - set(hijo['calles_h'])
        posibles = [c for c in posibles if all(abs(c - x) > 1 for x in hijo['calles_h'])]
        if posibles:
            hijo['calles_h'].append(random.choice(posibles))
    hijo['calles_v'] = sorted(hijo['calles_v'])
    hijo['calles_h'] = sorted(hijo['calles_h'])
    return hijo

def colocar_fijos(matriz, posiciones, valor):
    for (i, j) in posiciones:
        matriz[i][j] = valor
    return matriz

def tiene_acceso_a_calle(matriz, i, j):
    """Verifica si un lote tiene acceso a una calle (está adyacente a una calle)"""
    n = len(matriz)
    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n and matriz[ni][nj] == 4:  # 4 = calle
            return True
    return False

def colocar_areas_verdes_manhattan(matriz, num_areas_verdes):
    n = len(matriz)
    verdes_colocados = 0
    # Espaciado para lograr distancias de 1-5 celdas
    step = max(3, int((n * n / (num_areas_verdes * 4)) ** 0.5))  
    
    # Primera pasada: colocar áreas verdes con espaciado
    for i in range(0, n-1, step):
        for j in range(0, n-1, step):
            if verdes_colocados >= num_areas_verdes:
                break
            puede_colocar = True
            for di in range(2):
                for dj in range(2):
                    if i+di >= n or j+dj >= n or matriz[i+di][j+dj] != 1:
                        puede_colocar = False
            if puede_colocar:
                for di in range(2):
                    for dj in range(2):
                        matriz[i+di][j+dj] = 3  # 3 representa área verde
                verdes_colocados += 1
    
    # Segunda pasada: añadir más áreas verdes si es necesario
    while verdes_colocados < num_areas_verdes:
        # Buscar un lugar adecuado para una nueva área verde
        mejores_posiciones = []
        for i in range(n-1):
            for j in range(n-1):
                puede_colocar = True
                for di in range(2):
                    for dj in range(2):
                        if i+di >= n or j+dj >= n or matriz[i+di][j+dj] != 1:
                            puede_colocar = False
                if puede_colocar:
                    mejores_posiciones.append((i, j))
        
        if not mejores_posiciones:
            break  # No hay más lugares disponibles
            
        # Elegir una posición aleatoria entre las mejores
        i, j = random.choice(mejores_posiciones)
        for di in range(2):
            for dj in range(2):
                matriz[i+di][j+dj] = 3
        verdes_colocados += 1
    
    return matriz

def construir_matriz(individuo, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion=None):
    matriz = np.ones((n, n), dtype=int)  # 1 = lote habitacional
    
    # Colocar calles
    for fila in individuo['calles_h']:
        matriz[fila, :] = 4  # 4 = calle
    for col in individuo['calles_v']:
        matriz[:, col] = 4
    
    # Asegurar que todos los lotes tengan acceso a calles
    for i in range(n):
        for j in range(n):
            if matriz[i][j] == 1 and not tiene_acceso_a_calle(matriz, i, j):
                # Buscar la calle más cercana y crear un camino hacia ella
                min_dist = float('inf')
                mejor_dir = None
                
                for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    dist = 1
                    ni, nj = i + di, j + dj
                    while 0 <= ni < n and 0 <= nj < n:
                        if matriz[ni][nj] == 4:  # Encontramos una calle
                            if dist < min_dist:
                                min_dist = dist
                                mejor_dir = (di, dj)
                            break
                        dist += 1
                        ni += di
                        nj += dj
                
                if mejor_dir:
                    di, dj = mejor_dir
                    ni, nj = i, j
                    for _ in range(min_dist):
                        ni += di
                        nj += dj
                        if matriz[ni][nj] != 4:  # No sobreescribir calles existentes
                            matriz[ni][nj] = 4
    
    # Colocar áreas verdes
    matriz = colocar_areas_verdes_manhattan(matriz, num_verdes)
    
    # Colocar tanques de agua
    if elevacion is not None:
        # Encontrar posiciones de calles
        calles = np.argwhere(matriz == 4)
        
        # Ordenar posiciones de tanques
        posiciones_ordenadas = []
        for i in range(n):
            for j in range(n):
                if matriz[i][j] == 1:  # Solo considerar lotes habitacionales
                    posiciones_ordenadas.append((i, j, elevacion[i][j]))
        
        # Ordenar por elevacion
        posiciones_ordenadas.sort(key=lambda x: x[2], reverse=True)
        
        # Tomar las posiciones más altas para los tanques
        posiciones_tanques = [(i, j) for i, j, _ in posiciones_ordenadas[:min(len(posiciones_ordenadas), len(posiciones_tanques))]]
    
    matriz = colocar_fijos(matriz, posiciones_tanques, 2)  # 2 = tanque de agua
    
    # Colocar drenajes en calles y en zonas bajas
    posiciones_drenajes_en_calles = []
    calles = np.argwhere(matriz == 4)
    
    if len(calles) > 0 and len(posiciones_drenajes) > 0:
        if elevacion is not None:
            # Ordenar posiciones de calles por elevación
            calles_con_elevacion = [(i, j, elevacion[i][j]) for i, j in calles]
            calles_con_elevacion.sort(key=lambda x: x[2])  # Ordenar por elevación ascendente
            
            # Tomar las posiciones más bajas para los drenajes
            posiciones_drenajes_en_calles = [(i, j) for i, j, _ in calles_con_elevacion[:min(len(calles_con_elevacion), len(posiciones_drenajes))]]
        else:
            # Si no hay elevación, seleccionar posiciones aleatorias
            indices = np.random.choice(len(calles), min(len(posiciones_drenajes), len(calles)), replace=False)
            posiciones_drenajes_en_calles = [tuple(calles[i]) for i in indices]
    
    matriz = colocar_fijos(matriz, posiciones_drenajes_en_calles, 5)  # 5 = drenaje
    
    return matriz

def distancia_promedio_a_verde(matriz):
    n = matriz.shape[0]
    lotes = np.argwhere(matriz == 1)
    verdes = np.argwhere(matriz == 3)
    if len(verdes) == 0 or len(lotes) == 0:
        return 0
    distancias = []
    for (i, j) in lotes:
        min_dist = min([abs(i - vi) + abs(j - vj) for (vi, vj) in verdes])
        distancias.append(min_dist)
    return np.mean(distancias)

def calcular_fitness(individuo, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion=None):
    matriz = construir_matriz(individuo, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion)
    lotes = np.sum(matriz == 1)
    calles = np.sum(matriz == 4)
    verdes = np.sum(matriz == 3)
    drenajes = np.sum(matriz == 5)
    tanques = np.sum(matriz == 2)
    
    # Calcular distancia promedio a áreas
    distancia_verde = distancia_promedio_a_verde(matriz)
    
    if 1 <= distancia_verde <= 5:
        bonus_distancia = 10 * (1 - abs(distancia_verde - 3) / 3)  
    else:
        bonus_distancia = 0
    
    # Contar lotes con acceso a calles
    lotes_con_acceso = 0
    for i in range(n):
        for j in range(n):
            if matriz[i][j] == 1 and tiene_acceso_a_calle(matriz, i, j):
                lotes_con_acceso += 1
    
    bonus_elevacion = 0
    if elevacion is not None:
        # Bonus por drenajes en zonas bajas
        posiciones_drenajes = np.argwhere(matriz == 5)
        if len(posiciones_drenajes) > 0:
            elevacion_drenajes = np.mean([elevacion[i][j] for i, j in posiciones_drenajes])
            elevacion_promedio = np.mean(elevacion)
            if elevacion_drenajes < elevacion_promedio:
                # Bonus si los drenajes están por debajo del promedio
                bonus_elevacion += 5 * (1 - elevacion_drenajes / elevacion_promedio)
        
        # Bonus por tanques en zonas altas
        posiciones_tanques = np.argwhere(matriz == 2)
        if len(posiciones_tanques) > 0:
            elevacion_tanques = np.mean([elevacion[i][j] for i, j in posiciones_tanques])
            if elevacion_tanques > elevacion_promedio:
                # Bonus si los tanques
                bonus_elevacion += 5 * (elevacion_tanques / elevacion_promedio - 1)
    
    # Calcular fitness final
    fitness = lotes + verdes + bonus_distancia + lotes_con_acceso + bonus_elevacion
    
    return fitness

def ejecutar_algoritmo_genetico(n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion=None, generaciones=200, poblacion_size=20):
    poblacion = [generar_individuo(n) for _ in range(poblacion_size)]
    for _ in range(generaciones):
        fitness = [calcular_fitness(ind, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion) for ind in poblacion]
        padres_idx = np.argsort(fitness)[-2:]
        padre1, padre2 = poblacion[padres_idx[0]], poblacion[padres_idx[1]]
        nueva_poblacion = [padre1, padre2]
        while len(nueva_poblacion) < poblacion_size:
            hijo = cruzar(padre1, padre2, n)
            hijo = mutar(hijo, n)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    fitness = [calcular_fitness(ind, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion) for ind in poblacion]
    mejor_idx = np.argmax(fitness)
    mejor_ind = poblacion[mejor_idx]
    mejor_matriz = construir_matriz(mejor_ind, n, num_verdes, posiciones_drenajes, posiciones_tanques, elevacion)
    return mejor_matriz
