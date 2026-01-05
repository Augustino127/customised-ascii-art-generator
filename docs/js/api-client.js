/*
 * Client API pour communiquer avec le backend
 */

class ASCIIArtAPI {
    constructor(baseURL) {
        this.baseURL = baseURL || window.API_CONFIG.BASE_URL;
    }

    /**
     * Convertit une image en ASCII art
     */
    async convertImage(imageFile, options = {}) {
        try {
            // Convertir l'image en base64
            const base64 = await this.fileToBase64(imageFile);

            const response = await fetch(`${this.baseURL}/api/convert/image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: base64,
                    width: options.width || 100,
                    palette: options.palette || 'STANDARD',
                    color_mode: options.colorMode || 'monochrome',
                    algorithm: options.algorithm || 'luminosity',
                    contrast: options.contrast || 1.0,
                    brightness: options.brightness || 0,
                    invert: options.invert || false,
                    edge_detect: options.edgeDetect || false,
                    dithering: options.dithering || null
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Erreur lors de la conversion');
            }

            return await response.json();
        } catch (error) {
            console.error('Error converting image:', error);
            throw error;
        }
    }

    /**
     * Convertit du texte en ASCII art
     */
    async convertText(text, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}/api/convert/text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    font: options.font || 'standard',
                    width: options.width || null,
                    color: options.color || null,
                    banner: options.banner || false,
                    gradient: options.gradient || false,
                    gradient_colors: options.gradientColors || {
                        start: [0, 255, 255],
                        end: [255, 0, 255]
                    },
                    shadow: options.shadow || false,
                    shadow_offset: options.shadowOffset || [2, 1]
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Erreur lors de la conversion');
            }

            return await response.json();
        } catch (error) {
            console.error('Error converting text:', error);
            throw error;
        }
    }

    /**
     * Récupère la liste des palettes
     */
    async getPalettes() {
        try {
            const response = await fetch(`${this.baseURL}/api/palettes`);
            const data = await response.json();
            return data.palettes || [];
        } catch (error) {
            console.error('Error fetching palettes:', error);
            return [];
        }
    }

    /**
     * Récupère la liste des polices
     */
    async getFonts() {
        try {
            const response = await fetch(`${this.baseURL}/api/fonts`);
            const data = await response.json();
            return data.fonts || [];
        } catch (error) {
            console.error('Error fetching fonts:', error);
            return [];
        }
    }

    /**
     * Récupère la liste des algorithmes
     */
    async getAlgorithms() {
        try {
            const response = await fetch(`${this.baseURL}/api/algorithms`);
            const data = await response.json();
            return data.algorithms || [];
        } catch (error) {
            console.error('Error fetching algorithms:', error);
            return [];
        }
    }

    /**
     * Récupère la liste des modes de couleur
     */
    async getColorModes() {
        try {
            const response = await fetch(`${this.baseURL}/api/color-modes`);
            const data = await response.json();
            return data.color_modes || [];
        } catch (error) {
            console.error('Error fetching color modes:', error);
            return [];
        }
    }

    /**
     * Vérifie la santé de l'API
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`);
            const data = await response.json();
            return data.status === 'healthy';
        } catch (error) {
            console.error('API health check failed:', error);
            return false;
        }
    }

    /**
     * Convertit un fichier en base64
     */
    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // Extraire uniquement les données base64 (sans le préfixe data:image/...)
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }
}

// Instance globale
window.asciiAPI = new ASCIIArtAPI();
