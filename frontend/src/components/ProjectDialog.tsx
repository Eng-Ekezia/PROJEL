import React, { useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Grid // CORREÇÃO: Usar Grid v1 ou v2 do MUI 5
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { 
  EsquemaAterramento, 
  SistemaFases, 
  TensaoSistema, 
  TipoInstalacao 
} from '../types/enums';
// CORREÇÃO: Importação explicita de tipo
import type { Projeto } from '../types/project';

// --- SCHEMA DE VALIDAÇÃO (ZOD) ---
const tiposInstalacao = Object.values(TipoInstalacao) as [string, ...string[]];
const tensoesSistema = Object.values(TensaoSistema) as [string, ...string[]];
const sistemasFases = Object.values(SistemaFases) as [string, ...string[]];
const esquemasAterramento = Object.values(EsquemaAterramento) as [string, ...string[]];

// CORREÇÃO: Sintaxe correta para mensagens de erro no Zod v3
const projectSchema = z.object({
  nome: z.string().min(3, "O nome deve ter pelo menos 3 caracteres"),
  tipo_instalacao: z.enum(tiposInstalacao, { errorMap: () => ({ message: "Selecione o tipo" }) }),
  tensao_sistema: z.enum(tensoesSistema, { errorMap: () => ({ message: "Selecione a tensão" }) }),
  sistema: z.enum(sistemasFases, { errorMap: () => ({ message: "Selecione o sistema" }) }),
  esquema_aterramento: z.enum(esquemasAterramento, { errorMap: () => ({ message: "Selecione o aterramento" }) }),
  descricao_aterramento: z.string().optional(),
});

type ProjectFormData = z.infer<typeof projectSchema>;

interface ProjectDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: ProjectFormData) => void;
  initialData?: Projeto;
}

export const ProjectDialog: React.FC<ProjectDialogProps> = ({ 
  open, onClose, onSave, initialData 
}) => {
  const { control, handleSubmit, reset, formState: { errors } } = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      nome: '',
      tipo_instalacao: TipoInstalacao.RESIDENCIAL,
      tensao_sistema: TensaoSistema.V_127_220,
      sistema: SistemaFases.MONOFASICO,
      esquema_aterramento: EsquemaAterramento.TN_S,
      descricao_aterramento: ''
    }
  });

  useEffect(() => {
    if (open) {
      reset(initialData ? {
        nome: initialData.nome,
        tipo_instalacao: initialData.tipo_instalacao,
        tensao_sistema: initialData.tensao_sistema,
        sistema: initialData.sistema,
        esquema_aterramento: initialData.esquema_aterramento,
        descricao_aterramento: initialData.descricao_aterramento || ''
      } : {
        nome: '',
        tipo_instalacao: TipoInstalacao.RESIDENCIAL,
        tensao_sistema: TensaoSistema.V_127_220,
        sistema: SistemaFases.MONOFASICO,
        esquema_aterramento: EsquemaAterramento.TN_S,
        descricao_aterramento: ''
      });
    }
  }, [open, initialData, reset]);

  const onSubmit = (data: ProjectFormData) => {
    onSave(data);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {initialData ? 'Editar Configurações do Projeto' : 'Novo Projeto Elétrico'}
      </DialogTitle>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent dividers>
          <Grid container spacing={2}>
            {/* Nome do Projeto */}
            <Grid item xs={12}>
              <Controller
                name="nome"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Nome do Projeto"
                    fullWidth
                    error={!!errors.nome}
                    helperText={errors.nome?.message}
                    autoFocus
                  />
                )}
              />
            </Grid>

            {/* Tipo de Instalação */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="tipo_instalacao"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Tipo de Instalação"
                    fullWidth
                    error={!!errors.tipo_instalacao}
                    helperText={errors.tipo_instalacao?.message}
                  >
                    {Object.values(TipoInstalacao).map((option) => (
                      <MenuItem key={option} value={option}>{option}</MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>

            {/* Outros campos seguem o padrão... (Grid item em vez de Grid size no MUI 5) */}
             <Grid item xs={12} sm={6}>
               {/* ... Repetir correção Grid item vs Grid size para os demais campos ... */}
               {/* Exemplo para Sistema: */}
               <Controller
                name="sistema"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Sistema"
                    fullWidth
                    error={!!errors.sistema}
                    helperText={errors.sistema?.message}
                  >
                    {Object.values(SistemaFases).map((option) => (
                      <MenuItem key={option} value={option}>{option.toUpperCase()}</MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
             <Grid item xs={12} sm={6}>
               <Controller
                name="tensao_sistema"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Tensão Nominal"
                    fullWidth
                    error={!!errors.tensao_sistema}
                    helperText={errors.tensao_sistema?.message}
                  >
                    {Object.values(TensaoSistema).map((option) => (
                      <MenuItem key={option} value={option}>{option}</MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
             <Grid item xs={12} sm={6}>
               <Controller
                name="esquema_aterramento"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Esquema de Aterramento (NBR 5410)"
                    fullWidth
                    error={!!errors.esquema_aterramento}
                    helperText={errors.esquema_aterramento?.message}
                  >
                    {Object.values(EsquemaAterramento).map((option) => (
                      <MenuItem key={option} value={option}>{option}</MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
             <Grid item xs={12}>
              <Controller
                name="descricao_aterramento"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Detalhes do Eletrodo de Aterramento (Opcional)"
                    fullWidth
                    multiline
                    rows={2}
                    placeholder="Ex: Malha de aterramento com 3 hastes alinhadas..."
                  />
                )}
              />
            </Grid>

          </Grid>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={onClose} color="inherit">Cancelar</Button>
          <Button type="submit" variant="contained" color="primary">
            Salvar Projeto
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};