from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

app = Flask(__name__)

def comprobar_pitagoras(a, b, c):
    """
    Comprueba si los tres lados dados forman un triángulo rectángulo
    usando el teorema de Pitágoras.
    
    Args:
        a, b, c: Longitudes de los lados del triángulo
        
    Returns:
        Un mensaje indicando si cumple o no con el teorema de Pitágoras
    """
    if a > c and a > b:
        if a**2 == b**2 + c**2:
            return f"Estos lados forman un triángulo rectángulo según el teorema de Pitágoras."
        else:
            return f"No cumple: {a}^2 != {b}^2 + {c}^2"
    elif b > c and b > a:
        if b**2 == a**2 + c**2:
            return f"Estos lados forman un triángulo rectángulo según el teorema de Pitágoras."
        else:
            return f"No cumple: {b}^2 != {a}^2 + {c}^2"
    elif c > a and c > b:
        if c**2 == a**2 + b**2:
            return f"Estos lados forman un triángulo rectángulo según el teorema de Pitágoras."
        else:
            return f"No cumple: {c}^2 != {a}^2 + {b}^2"

def calcular_area(a, b, c):
    """
    Calcula el área de un triángulo utilizando la fórmula de Herón.
    
    Args:
        a, b, c: Longitudes de los lados del triángulo
        
    Returns:
        El área del triángulo
    """
    s = (a + b + c) / 2
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

def graficar_triangulo(a, b, c):
    """
    Grafica un triángulo en 3D con las longitudes de los lados dados y muestra el área.
    
    Args:
        a, b, c: Longitudes de los lados del triángulo
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Coordenadas de los vértices del triángulo
    vertices = [(0, 0, 0), (a, 0, 0), (0, b, 0)]
    
    # Agregar las líneas que representan los lados del triángulo
    lines = [(vertices[0], vertices[1]), (vertices[1], vertices[2]), (vertices[2], vertices[0])]
    
    # Dibujar las líneas
    for line in lines:
        ax.plot3D(*zip(*line), color='blue')
    
    # Triángulo en 3D
    tri = np.array([vertices[0], vertices[1], vertices[2]])
    ax.plot_trisurf(tri[:, 0], tri[:, 1], tri[:, 2], color='skyblue', alpha=0.5)
    
    # Etiquetas para los puntos
    ax.text(*vertices[0], "A (0, 0, 0)", color='red')
    ax.text(*vertices[1], f"B ({a}, 0, 0)", color='red')
    ax.text(*vertices[2], f"C (0, {b}, 0)", color='red')
    
    # Calcular el área
    area = calcular_area(a, b, c)
    
    # Mostrar el área en el gráfico
    mid_point = [(vertices[0][0] + vertices[1][0] + vertices[2][0]) / 3,
                 (vertices[0][1] + vertices[1][1] + vertices[2][1]) / 3,
                 (vertices[0][2] + vertices[1][2] + vertices[2][2]) / 3]
    
    ax.text(mid_point[0], mid_point[1], mid_point[2], f"Área = {area:.2f}", color='green')
    
    # Configuraciones adicionales
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Triángulo en 3D')
    
    # Guardar la figura como imagen
    plt.savefig('static/triangulo.png')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lado_a = float(request.form['lado_a'])
        lado_b = float(request.form['lado_b'])
        hipotenusa = float(request.form['hipotenusa'])

        mensaje = comprobar_pitagoras(lado_a, lado_b, hipotenusa)
        if "Estos lados forman un triángulo rectángulo según el teorema de Pitágoras." in mensaje:
            graficar_triangulo(lado_a, lado_b, hipotenusa)
        
        return render_template('index.html', mensaje=mensaje, mostrar=True)
    else:
        return render_template('index.html', mensaje="", mostrar=False)

if __name__ == '__main__':
    app.run(debug=True)
