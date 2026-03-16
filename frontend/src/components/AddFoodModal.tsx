import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { aiService, type AIAnalysisResponse } from '../services/ai';
import { foodLogService } from '../services/foodLogs';

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export default function AddFoodModal({ isOpen, onClose }: Props) {

    const [mode, setMode] = useState<'image' | 'text'>('image');
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [textQuery, setTextQuery] = useState('');
    const [analysis, setAnalysis] = useState<AIAnalysisResponse | null>(null);

    const queryClient = useQueryClient();

    const aiImageMutation = useMutation({
        mutationFn: (file: File) => aiService.analyzeImage(file),
        onSuccess: (data) => setAnalysis(data),
    });

    const aiTextMutation = useMutation({
        mutationFn: (query: string) => aiService.analyzeText(query),
        onSuccess: (data) => setAnalysis(data),
    });

    const saveMutation = useMutation({
        mutationFn: (formData: FormData) => foodLogService.uploadLog(formData),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['foodLogs'] });
            handleClose();
        },
    });

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {

            setFile(selectedFile);
            if (preview) URL.revokeObjectURL(preview);
            const objectUrl = URL.createObjectURL(selectedFile);
            setPreview(objectUrl);

            aiImageMutation.mutate(selectedFile);
        }
    };

    const handleTextAnalyze = () => {
        if (textQuery.trim()) {
            aiTextMutation.mutate(textQuery);
        }
    };

    const handleClose = () => {
        if (preview) URL.revokeObjectURL(preview);
        setFile(null);
        setPreview(null);
        setAnalysis(null);
        setTextQuery('');
        setMode('image');
        aiImageMutation.reset();
        aiTextMutation.reset();
        onClose();
    };

    const handleSave = () => {
        if (!analysis) return;

        const formData = new FormData();

        if (mode === 'image' && file) {
            formData.append('file', file);
        }

        formData.append('food_name', analysis.food_name);
        formData.append('calories', analysis.calories.toString());
        formData.append('proteins', analysis.proteins.toString());
        formData.append('carbs', analysis.carbs.toString());
        formData.append('fats', analysis.fats.toString());

        saveMutation.mutate(formData);
    };

    if (!isOpen) return null;

    const isAnalyzing = aiImageMutation.isPending || aiTextMutation.isPending;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4">
            <div className="w-full max-w-md rounded-3xl bg-white shadow-2xl overflow-hidden border border-gray-100">
                <div className="p-6 space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-black text-gray-800 tracking-tight">Nueva Comida</h2>
                        <button onClick={handleClose} className="text-gray-400 hover:text-gray-600 transition-colors">✕</button>
                    </div>

                    <div className="flex bg-gray-100 p-1 rounded-xl">
                        <button
                            onClick={() => { setMode('image'); setAnalysis(null); }}
                            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${mode === 'image' ? 'bg-white shadow-sm text-emerald-600' : 'text-gray-400'}`}
                        >
                            📸 Foto
                        </button>
                        <button
                            onClick={() => { setMode('text'); setAnalysis(null); }}
                            className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all ${mode === 'text' ? 'bg-white shadow-sm text-emerald-600' : 'text-gray-400'}`}
                        >
                            ✍️ Descripción
                        </button>
                    </div>

                    {mode === 'image' ? (
                        <div className="relative aspect-square w-full overflow-hidden rounded-2xl bg-gray-50 border-2 border-dashed border-gray-200 flex items-center justify-center group hover:border-emerald-300 transition-all">
                            {preview ? (
                                <img src={preview} className="h-full w-full object-cover block" alt="Preview" />
                            ) : (
                                <label className="cursor-pointer flex flex-col items-center justify-center w-full h-full p-6 text-center">
                                    <span className="text-5xl mb-3">📸</span>
                                    <p className="text-sm font-bold text-gray-400">Toca para subir una foto</p>
                                    <input type="file" className="hidden" onChange={handleFileChange} accept=".jpg,.jpeg,.png,.webp" />
                                </label>
                            )}
                            {aiImageMutation.isPending && (
                                <div className="absolute inset-0 bg-white/90 backdrop-blur-sm flex flex-col items-center justify-center">
                                    <div className="h-10 w-10 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
                                    <p className="text-emerald-700 font-black mt-4 text-xs">ANALIZANDO IMAGEN...</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="space-y-3">
                            <textarea
                                className="w-full p-4 rounded-2xl border-2 border-gray-100 focus:border-emerald-500 outline-none resize-none h-32 text-sm"
                                placeholder="Ej: Tres pupusas de revuelta con curtido y salsa..."
                                value={textQuery}
                                onChange={(e) => setTextQuery(e.target.value)}
                            />
                            <button
                                onClick={handleTextAnalyze}
                                disabled={isAnalyzing || !textQuery.trim()}
                                className="w-full py-2 bg-emerald-100 text-emerald-700 rounded-xl font-bold text-xs hover:bg-emerald-200 transition-colors"
                            >
                                {aiTextMutation.isPending ? 'Analizando...' : 'Analizar texto'}
                            </button>
                        </div>
                    )}

                    {analysis && (
                        <div className="animate-in slide-in-from-bottom-2 fade-in duration-500">
                            <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100">
                                <p className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Identificado como</p>
                                <h3 className="text-lg font-black text-gray-800 capitalize leading-tight">{analysis.food_name}</h3>

                                <div className="grid grid-cols-4 gap-2 mt-4">
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-gray-800">{analysis.calories}</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase">Kcal</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-emerald-600">{analysis.proteins}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase">Prot</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-blue-600">{analysis.carbs}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase">Carb</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-orange-600">{analysis.fats}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase">Fat</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex gap-3 pt-2">
                        <button onClick={handleClose} className="flex-1 py-3 font-bold text-gray-400 hover:bg-gray-50 rounded-2xl text-sm transition-all">
                            Cancelar
                        </button>
                        <button
                            disabled={!analysis || saveMutation.isPending}
                            onClick={handleSave}
                            className={`flex-[2] py-3 rounded-2xl font-black text-white shadow-lg transition-all text-sm uppercase ${!analysis ? 'bg-gray-100 text-gray-300 cursor-not-allowed shadow-none' : 'bg-emerald-600 hover:bg-emerald-700 active:scale-95'
                                }`}
                        >
                            {saveMutation.isPending ? 'Guardando...' : 'Confirmar y Guardar'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}