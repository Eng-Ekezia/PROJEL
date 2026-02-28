import { 
    Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogClose
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertCircle, CheckCircle2, Zap, LayoutList, Calculator, CheckSquare } from "lucide-react"

interface VerificacaoNormativa {
    criterio: string;
    status: 'atende' | 'atende_com_restricao' | 'nao_atende';
    valor_calculado: string | number;
    limite_normativo: string | number;
    mensagem: string;
    referencia_nbr: string;
}

interface ResultadoDimensionamento {
    circuito_id: string;
    status_global: 'atende' | 'atende_com_restricao' | 'nao_atende';
    corrente_projeto_ib: number;
    corrente_corrigida_iz: number;
    disjuntor_nominal_in: number;
    secao_condutor_mm2: number;
    queda_tensao_pct: number;
    verificacoes: VerificacaoNormativa[];
    memoria: { passos: string[] };
    erros_entrada: string[];
}

interface Props {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    resultado: ResultadoDimensionamento | null;
    circuitoNome: string;
}

export function ResultadoDimensionamentoDialog({ open, onOpenChange, resultado, circuitoNome }: Props) {
    if (!resultado) return null;

    const getStatusStyle = (status: string) => {
        if (status === 'atende') return "bg-green-100 text-green-800 border-green-200 dark:bg-green-900/40 dark:text-green-300";
        if (status === 'atende_com_restricao') return "bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900/40 dark:text-yellow-300";
        return "bg-red-100 text-red-800 border-red-200 dark:bg-red-900/40 dark:text-red-300";
    };

    const getStatusIcon = (status: string) => {
        if (status === 'atende') return <CheckCircle2 className="w-4 h-4" />;
        return <AlertCircle className="w-4 h-4" />;
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[850px] max-h-[90vh] flex flex-col p-0 overflow-hidden">
                <DialogHeader className="p-6 pb-2 border-b shrink-0">
                    <div className="flex items-start justify-between">
                        <div>
                            <DialogTitle className="text-xl flex items-center gap-2">
                                <Zap className="w-5 h-5 text-indigo-500" /> 
                                Análise Normativa: Circuito {circuitoNome}
                            </DialogTitle>
                            <DialogDescription className="mt-1 flex items-center gap-2">
                                Status Geral: 
                                <Badge variant="outline" className={`ml-1 gap-1 ${getStatusStyle(resultado.status_global)}`}>
                                    {getStatusIcon(resultado.status_global)}
                                    {resultado.status_global.replace(/_/g, " ").toUpperCase()}
                                </Badge>
                            </DialogDescription>
                        </div>
                    </div>
                </DialogHeader>

                {resultado.erros_entrada && resultado.erros_entrada.length > 0 && (
                    <div className="mx-6 mt-4 p-3 bg-red-50 text-red-800 border border-red-200 rounded-md text-sm">
                        <strong className="flex items-center gap-2 mb-1"><AlertCircle className="w-4 h-4"/> Erros Críticos que Inviabilizaram o Cálculo:</strong>
                        <ul className="list-disc pl-5">
                            {resultado.erros_entrada.map((e, idx) => <li key={idx}>{e}</li>)}
                        </ul>
                    </div>
                )}

                <Tabs defaultValue="resumo" className="flex-1 overflow-hidden flex flex-col p-6 pt-2">
                    <TabsList className="mb-4 shrink-0">
                        <TabsTrigger value="resumo" className="gap-2"><LayoutList className="w-4 h-4"/> Resultados Rápidos</TabsTrigger>
                        <TabsTrigger value="verificacoes" className="gap-2"><CheckSquare className="w-4 h-4"/> Check NBR 5410</TabsTrigger>
                        <TabsTrigger value="memoria" className="gap-2"><Calculator className="w-4 h-4"/> Memória de Cálculo</TabsTrigger>
                    </TabsList>

                    <TabsContent value="resumo" className="flex-1 overflow-auto m-0 space-y-4 pr-2">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="border rounded-md p-4 flex flex-col items-center justify-center bg-card shadow-sm">
                                <span className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Seção do Condutor</span>
                                <span className="text-2xl font-bold font-mono">{resultado.secao_condutor_mm2} mm²</span>
                            </div>
                            <div className="border rounded-md p-4 flex flex-col items-center justify-center bg-card shadow-sm">
                                <span className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Disjuntor (IN)</span>
                                <span className="text-2xl font-bold font-mono">{resultado.disjuntor_nominal_in} A</span>
                            </div>
                            <div className="border rounded-md p-4 flex flex-col items-center justify-center bg-card shadow-sm">
                                <span className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Corrente Corrigida</span>
                                <span className="text-2xl font-bold font-mono">{resultado.corrente_corrigida_iz.toFixed(2)} A</span>
                            </div>
                            <div className="border rounded-md p-4 flex flex-col items-center justify-center bg-card shadow-sm">
                                <span className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Queda de Tensão</span>
                                <span className="text-2xl font-bold font-mono">{resultado.queda_tensao_pct.toFixed(2)} %</span>
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent value="verificacoes" className="flex-1 overflow-hidden m-0">
                        <ScrollArea className="h-full pr-4">
                            <div className="space-y-3 pb-8">
                                {resultado.verificacoes.map((verificacao, idx) => (
                                    <div key={idx} className={`p-4 border rounded-lg bg-card/50 flex flex-col gap-2 ${verificacao.status === 'nao_atende' ? 'border-red-300' : ''}`}>
                                        <div className="flex justify-between items-start">
                                            <h4 className="font-semibold text-sm">{verificacao.criterio}</h4>
                                            <Badge variant="outline" className={`px-2 py-0 text-xs ${getStatusStyle(verificacao.status)}`}>
                                                {verificacao.status.replace(/_/g, ' ').toUpperCase()}
                                            </Badge>
                                        </div>
                                        <p className="text-sm text-foreground my-1">{verificacao.mensagem}</p>
                                        <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground mt-2 bg-muted/30 p-2 rounded">
                                            <span>Calc: {verificacao.valor_calculado}</span>
                                            <span>Lim: {verificacao.limite_normativo}</span>
                                            <span className="ml-auto text-indigo-500 font-sans font-medium">{verificacao.referencia_nbr}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </ScrollArea>
                    </TabsContent>

                    <TabsContent value="memoria" className="flex-1 overflow-hidden m-0">
                        <div className="h-full border rounded-lg bg-slate-950 p-4 font-mono text-sm text-green-400 overflow-auto">
                            <ScrollArea className="h-full pr-4">
                                {resultado.memoria.passos.map((passo, i) => (
                                    <div key={i} className="mb-2 opacity-90 hover:opacity-100 hover:bg-slate-900 px-2 py-1 rounded transition-colors break-words">
                                        <span className="text-slate-600 mr-3">{(i + 1).toString().padStart(2, '0')}:</span>
                                        {passo}
                                    </div>
                                ))}
                            </ScrollArea>
                        </div>
                    </TabsContent>
                </Tabs>

            </DialogContent>
        </Dialog>
    )
}
