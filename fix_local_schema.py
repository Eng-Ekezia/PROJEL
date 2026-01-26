import os

local_schema_content = r'''
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LocalBase(BaseModel):
    nome: str = Field(..., min_length=2, description="Nome do cômodo (ex: Sala de Estar)")
    
    # Geometria Básica
    area_m2: float = Field(..., gt=0, description="Área em metros quadrados")
    perimetro_m: float = Field(..., gt=0, description="Perímetro em metros")
    pe_direito_m: float = Field(default=2.80, gt=1.5, description="Altura do teto em metros")
    
    # Vínculos
    zona_id: str = Field(..., description="ID da Zona de Influência vinculada")
    projeto_id: str = Field(..., description="ID do Projeto pai")  # <--- O CAMPO FALTANTE ERA ESTE

class LocalCreate(LocalBase):
    pass

class Local(LocalBase):
    id: str
    data_criacao: datetime

    class Config:
        from_attributes = True
'''

def main():
    base_dir = os.getcwd()
    target_path = os.path.join(base_dir, "domain_core/schemas/local.py")
    
    # Verifica se a pasta existe (segurança)
    if not os.path.exists(os.path.dirname(target_path)):
        print(f"ERRO: Pasta {os.path.dirname(target_path)} não encontrada.")
        return

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(local_schema_content.strip())
    
    print("✅ domain_core/schemas/local.py corrigido com sucesso!")
    print("👉 REINICIE O BACKEND AGORA: (Ctrl+C -> uvicorn main:app --reload)")

if __name__ == "__main__":
    main()