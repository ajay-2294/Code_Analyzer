import os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to analyze code quality using pylint
def analyze_code_quality():
    files = ['module1.py', 'module2.py', 'utils.py']
    results = {}
    for file in files:
        result = subprocess.run(['pylint', os.path.join(app.config['UPLOAD_FOLDER'], file)], capture_output=True, text=True)

        results[file] = result.stdout
    with open('static/code_quality.log', 'w') as log_file:
        for file, report in results.items():
            log_file.write(f"\nFile: {file}\n{report}\n")
    return results

# Function to analyze module dependencies
def analyze_dependencies():
    dependencies = {
        'app.py': ['module1.py', 'module2.py'],
        'module1.py': ['utils.py'],
        'module2.py': ['utils.py'],
        'utils.py': []
    }
    G = nx.DiGraph(dependencies)
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.savefig('static/dependency_graph.png')
    return 'static/dependency_graph.png'

@app.route('/', methods=['GET', 'POST'])
def index():
    print("✅ Rendering index.html")  # <-- Debugging line
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('index'))

    code_quality = analyze_code_quality()
    dependency_graph = analyze_dependencies()
    
    return render_template('index.html', code_quality=code_quality, dependency_graph=dependency_graph)

if __name__ == '__main__':
    app.run(debug=True)

