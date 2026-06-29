import os
import subprocess
import sys

def install_dependencies():
    print("🤖 Verificando e instalando dependências do FinAI...")
    dependencies = ["streamlit", "pandas", "requests"]
    for package in dependencies:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
    print("✅ Todas as dependências estão prontas!")

def run_app():
    print("🚀 Iniciando a interface Streamlit...")
    # Executa o streamlit apontando para o arquivo dentro de src/
    subprocess.run(["streamlit", "run", "src/app.py"])

if __name__ == "__main__":
    install_dependencies()
    run_app()
