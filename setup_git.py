import os
import subprocess
import sys

# Nome do projeto definido no Roadmap
PROJECT_NAME = "webapp-dimensionamento-nbr5410"

# Conteúdo do .gitignore unificado (Python + Node + VSCode + OS)
GITIGNORE_CONTENT = """
# --- Python ---
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# --- Node.js (Frontend) ---
node_modules/
dist/
build/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# --- IDEs / Editores ---
.idea/
.vscode/
*.swp
*.swo

# --- OS ---
.DS_Store
Thumbs.db

# --- Logs e Dados Locais ---
*.log
*.sqlite
*.db
"""

def run_command(command, error_message):
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ {error_message}")
        # print(f"Detalhe: {e.stderr.decode().strip()}") # Descomente para debug
        return False

def create_gitignore():
    print("📝 Criando .gitignore otimizado para Monorepo...")
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT.strip())
    print("✅ .gitignore criado.")

def init_git():
    print("\n🔧 Inicializando repositório Git local...")
    
    # 1. Init
    if not run_command("git init", "Falha ao rodar git init"): return False
    
    # 2. Rename branch to main (padrão moderno)
    run_command("git branch -M main", "Aviso: Não foi possível renomear branch para main (pode já ser o padrão).")
    
    # 3. Add all
    print("📦 Adicionando arquivos...")
    if not run_command("git add .", "Falha ao adicionar arquivos"): return False
    
    # 4. Commit
    print("💾 Realizando commit inicial...")
    if not run_command('git commit -m "feat: initial structure (phase 02) - monorepo setup"', "Nada para commitar ou falha no commit"):
        print("   (Talvez o commit já tenha sido feito anteriormente?)")
    else:
        print("✅ Commit inicial realizado com sucesso.")
    
    return True

def setup_github():
    print("\n☁️  Configurando GitHub...")
    
    # Verifica se o GitHub CLI (gh) está instalado
    gh_installed = run_command("gh --version", "GitHub CLI (gh) não detectado.")
    
    if gh_installed:
        print("🚀 GitHub CLI detectado. Tentando criar repositório remoto...")
        print(f"   Nome do Repo: {PROJECT_NAME}")
        
        # Cria repo publico e já faz o push
        # --source=. usa a pasta atual
        # --public define visibilidade
        # --remote=origin define o remote
        # --push faz o push imediato
        cmd = f"gh repo create {PROJECT_NAME} --public --source=. --remote=origin --push"
        
        if run_command(cmd, "Falha ao criar repo via GitHub CLI."):
            print(f"\n✅ Repositório criado e código enviado: https://github.com/[SEU_USUARIO]/{PROJECT_NAME}")
            return
        else:
            print("⚠️  Não foi possível criar automaticamente (talvez você precise fazer login: 'gh auth login').")
    
    # Fallback Manual
    print("\n--- INSTRUÇÕES MANUAIS ---")
    print("Como a automação via CLI não foi possível, execute manualmente:")
    print(f"1. Crie um repositório vazio no GitHub chamado '{PROJECT_NAME}'")
    print("2. Rode os comandos abaixo no terminal:")
    print(f"   git remote add origin https://github.com/SEU_USUARIO/{PROJECT_NAME}.git")
    print("   git push -u origin main")

if __name__ == "__main__":
    create_gitignore()
    if init_git():
        setup_github()
    else:
        print("\n❌ Erro: Git não parece estar instalado ou configurado corretamente.")