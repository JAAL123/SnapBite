import api from './api';

export interface FoodLog {
    id: string;
    food_name: string;
    calories: number;
    proteins: number;
    carbs: number;
    fats: number;
    image_url: string;
    created_at: string;
}

export const foodLogService = {
    async getMyLogs(): Promise<FoodLog[]> {
        const response = await api.get('/food-logs/');
        return response.data;
    },

    async uploadLog(formData: FormData): Promise<FoodLog> {
        const response = await api.post('/food-logs/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

};