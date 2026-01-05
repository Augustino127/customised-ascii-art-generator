/*
 * Configuration de l'API
 */

// URL de l'API - METTEZ VOTRE URL RENDER ICI !
const API_URL = 'https://VOTRE-URL-RENDER.onrender.com';  // ← Changez ici !

// Export pour utilisation dans d'autres fichiers
window.API_CONFIG = {
    BASE_URL: API_URL,
    ENDPOINTS: {
        HEALTH: `${API_URL}/api/health`,
        CONVERT_IMAGE: `${API_URL}/api/convert/image`,
        CONVERT_TEXT: `${API_URL}/api/convert/text`,
        PALETTES: `${API_URL}/api/palettes`,
        FONTS: `${API_URL}/api/fonts`,
        ALGORITHMS: `${API_URL}/api/algorithms`,
        COLOR_MODES: `${API_URL}/api/color-modes`,
        EFFECTS: `${API_URL}/api/effects`
    }
};
