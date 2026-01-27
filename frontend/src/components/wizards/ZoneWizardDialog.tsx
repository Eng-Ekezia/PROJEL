import React, { useState } from 'react';
import { 
    Dialog, DialogTitle, DialogContent, DialogActions, 
    Button, Stepper, Step, StepLabel, Typography, 
    Box, Radio, RadioGroup, FormControlLabel, FormControl, 
    FormLabel, Paper, Grid, Divider
} from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

import { ZONE_WIZARD_DATA } from '../../data/nbr5410_wizard';
import type { WizardQuestion } from '../../data/nbr5410_wizard';
import type { Zona } from '../../types/project';

interface ZoneWizardDialogProps {
    open: boolean;
    onClose: () => void;
    onSave: (zonaData: Partial<Zona>) => void;
}

const STEPS = ['Ambiente Físico', 'Uso e Pessoas', 'Estrutura e Materiais', 'Revisão'];

export const ZoneWizardDialog: React.FC<ZoneWizardDialogProps> = ({ open, onClose, onSave }) => {
    const [activeStep, setActiveStep] = useState(0);
    const [answers, setAnswers] = useState<Partial<Zona>>({
        nome: '',
        // Defaults seguros
        temp_ambiente: 'AA4',
        presenca_agua: 'AD1',
        presenca_solidos: 'AE1',
        competencia_pessoas: 'BA1',
        materiais_construcao: 'CA2',
        estrutura_edificacao: 'CB1'
    });

    // Filtra perguntas da etapa atual
    const getQuestionsForStep = (stepIndex: number): WizardQuestion[] => {
        switch(stepIndex) {
            case 0: return ZONE_WIZARD_DATA.filter(q => q.category === 'ambiente');
            case 1: return ZONE_WIZARD_DATA.filter(q => q.category === 'pessoas');
            case 2: return ZONE_WIZARD_DATA.filter(q => q.category === 'estrutura');
            default: return [];
        }
    };

    const handleChange = (fieldId: string, value: string) => {
        setAnswers(prev => ({ ...prev, [fieldId]: value }));
    };

    const handleNext = () => {
        if (activeStep === STEPS.length - 1) {
            onSave(answers);
            handleClose();
        } else {
            setActiveStep(prev => prev + 1);
        }
    };

    const handleBack = () => setActiveStep(prev => prev - 1);
    
    const handleClose = () => {
        setActiveStep(0);
        setAnswers({ nome: '' }); // Reset parcial
        onClose();
    };

    return (
        <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
            <DialogTitle sx={{ bgcolor: 'primary.main', color: 'white' }}>
                Assistente de Criação de Zona
            </DialogTitle>
            
            <DialogContent sx={{ mt: 2 }}>
                <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
                    {STEPS.map((label) => <Step key={label}><StepLabel>{label}</StepLabel></Step>)}
                </Stepper>

                <Box sx={{ minHeight: '300px' }}>
                    {activeStep < 3 ? (
                        // --- ETAPAS DE PERGUNTAS ---
                        <Box>
                             {/* Nome da Zona (Aparece apenas no passo 0) */}
                            {activeStep === 0 && (
                                <Box mb={4}>
                                    <Typography variant="h6" gutterBottom>1. Identificação</Typography>
                                    <Typography variant="body2" color="text.secondary" paragraph>
                                        Dê um nome descritivo para este grupo de ambientes (ex: "Área de Serviço", "Quartos", "Área Externa").
                                    </Typography>
                                    <input 
                                        type="text" 
                                        placeholder="Nome da Zona (ex: Área Molhada)" 
                                        style={{ width: '100%', padding: '10px', fontSize: '16px', borderRadius: '4px', border: '1px solid #ccc' }}
                                        value={answers.nome || ''}
                                        onChange={(e) => handleChange('nome', e.target.value)}
                                        autoFocus
                                    />
                                </Box>
                            )}

                            {getQuestionsForStep(activeStep).map((q) => (
                                <Box key={q.id} sx={{ mb: 4, p: 2, bgcolor: '#f9f9f9', borderRadius: 2 }}>
                                    <FormLabel component="legend" sx={{ color: 'text.primary', fontWeight: 'bold', mb: 1 }}>
                                        {q.question}
                                    </FormLabel>
                                    <Typography variant="caption" color="text.secondary" display="block" mb={2}>
                                        {q.helperText}
                                    </Typography>
                                    
                                    <RadioGroup
                                        value={answers[q.id as keyof Zona] || ''}
                                        onChange={(e) => handleChange(q.id, e.target.value)}
                                    >
                                        <Grid container spacing={2}>
                                            {q.options.map((opt) => (
                                                <Grid item xs={12} sm={6} key={opt.code}>
                                                    <Paper variant="outlined" 
                                                        sx={{ 
                                                            p: 1, 
                                                            borderColor: answers[q.id as keyof Zona] === opt.code ? 'primary.main' : 'divider',
                                                            bgcolor: answers[q.id as keyof Zona] === opt.code ? 'action.selected' : 'background.paper',
                                                            cursor: 'pointer'
                                                        }}
                                                        onClick={() => handleChange(q.id, opt.code)}
                                                    >
                                                        <FormControlLabel 
                                                            value={opt.code} 
                                                            control={<Radio size="small" />} 
                                                            label={
                                                                <Box>
                                                                    <Typography variant="subtitle2" fontWeight="bold">{opt.label}</Typography>
                                                                    <Typography variant="caption" color="text.secondary">{opt.description}</Typography>
                                                                </Box>
                                                            } 
                                                            sx={{ margin: 0, width: '100%', alignItems: 'flex-start' }}
                                                        />
                                                    </Paper>
                                                </Grid>
                                            ))}
                                        </Grid>
                                    </RadioGroup>
                                </Box>
                            ))}
                        </Box>
                    ) : (
                        // --- ETAPA DE REVISÃO (RESUMO TÉCNICO) ---
                        <Box textAlign="center" py={2}>
                            <CheckCircleIcon color="success" sx={{ fontSize: 60, mb: 2 }} />
                            <Typography variant="h5" gutterBottom>Zona Definida!</Typography>
                            <Typography color="text.secondary" paragraph>
                                O sistema traduziu suas respostas para os seguintes parâmetros normativos:
                            </Typography>
                            
                            <Paper variant="outlined" sx={{ maxWidth: 600, mx: 'auto', textAlign: 'left' }}>
                                <Box p={2} display="flex" justifyContent="space-between" bgcolor="#f5f5f5">
                                    <Typography fontWeight="bold">Nome da Zona:</Typography>
                                    <Typography>{answers.nome}</Typography>
                                </Box>
                                <Divider />
                                <Grid container p={2} spacing={2}>
                                    {ZONE_WIZARD_DATA.map(q => {
                                        const selected = q.options.find(o => o.code === answers[q.id as keyof Zona]);
                                        return (
                                            <Grid item xs={6} key={q.id}>
                                                <Typography variant="caption" color="text.secondary">{q.category.toUpperCase()}</Typography>
                                                <Typography variant="subtitle2">{selected?.label}</Typography>
                                                <Typography variant="caption" sx={{ bgcolor: '#eee', px: 0.5, borderRadius: 0.5 }}>
                                                    Código: {selected?.code}
                                                </Typography>
                                            </Grid>
                                        );
                                    })}
                                </Grid>
                            </Paper>
                        </Box>
                    )}
                </Box>
            </DialogContent>
            
            <DialogActions sx={{ p: 3 }}>
                {activeStep > 0 && (
                    <Button onClick={handleBack} startIcon={<NavigateBeforeIcon />}>
                        Voltar
                    </Button>
                )}
                <Box sx={{ flexGrow: 1 }} />
                <Button 
                    variant="contained" 
                    onClick={handleNext}
                    endIcon={activeStep === STEPS.length - 1 ? <CheckCircleIcon /> : <NavigateNextIcon />}
                    disabled={activeStep === 0 && !answers.nome}
                >
                    {activeStep === STEPS.length - 1 ? 'Confirmar e Criar' : 'Próximo'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};