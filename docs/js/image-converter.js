/*
 * Gestion de la conversion d'images
 */

class ImageConverter {
    constructor() {
        this.currentFile = null;
        this.setupEventListeners();
        this.loadOptions();
    }

    setupEventListeners() {
        // Drop zone
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');

        if (dropZone) {
            dropZone.addEventListener('click', () => fileInput.click());
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });
            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('dragover');
            });
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFile(files[0]);
                }
            });
        }

        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFile(e.target.files[0]);
                }
            });
        }

        // Bouton de conversion
        const convertBtn = document.getElementById('convertBtn');
        if (convertBtn) {
            convertBtn.addEventListener('click', () => this.convert());
        }

        // Bouton de téléchargement
        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.download());
        }

        // Sliders avec affichage de valeur
        this.setupSliders();
    }

    setupSliders() {
        const sliders = document.querySelectorAll('input[type="range"]');
        sliders.forEach(slider => {
            const valueDisplay = document.getElementById(`${slider.id}Value`);
            if (valueDisplay) {
                slider.addEventListener('input', () => {
                    valueDisplay.textContent = slider.value;
                });
            }
        });
    }

    handleFile(file) {
        // Vérifier le type de fichier
        if (!file.type.startsWith('image/')) {
            this.showError('Veuillez sélectionner une image valide');
            return;
        }

        // Vérifier la taille (max 10 MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('Image trop grande (max 10 MB)');
            return;
        }

        this.currentFile = file;

        // Afficher preview de l'image
        const preview = document.getElementById('imagePreview');
        if (preview) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = `<img src="${e.target.result}" style="max-width: 100%; border-radius: 8px;">`;
            };
            reader.readAsDataURL(file);
        }

        // Activer le bouton de conversion
        const convertBtn = document.getElementById('convertBtn');
        if (convertBtn) {
            convertBtn.disabled = false;
        }

        this.hideError();
    }

    async loadOptions() {
        try {
            // Charger les palettes
            const palettes = await window.asciiAPI.getPalettes();
            const paletteSelect = document.getElementById('palette');
            if (paletteSelect && palettes.length > 0) {
                paletteSelect.innerHTML = palettes.map(p =>
                    `<option value="${p.name}">${p.name} (${p.length} chars)</option>`
                ).join('');
            }

            // Charger les algorithmes
            const algorithms = await window.asciiAPI.getAlgorithms();
            const algorithmSelect = document.getElementById('algorithm');
            if (algorithmSelect && algorithms.length > 0) {
                algorithmSelect.innerHTML = algorithms.map(a =>
                    `<option value="${a.name}">${a.name} - ${a.description}</option>`
                ).join('');
            }

            // Charger les modes de couleur
            const colorModes = await window.asciiAPI.getColorModes();
            const colorModeSelect = document.getElementById('colorMode');
            if (colorModeSelect && colorModes.length > 0) {
                colorModeSelect.innerHTML = colorModes.map(c =>
                    `<option value="${c.name}">${c.name} - ${c.description}</option>`
                ).join('');
            }
        } catch (error) {
            console.error('Error loading options:', error);
        }
    }

    async convert() {
        if (!this.currentFile) {
            this.showError('Veuillez sélectionner une image');
            return;
        }

        // Récupérer les options
        const options = {
            width: parseInt(document.getElementById('width').value),
            palette: document.getElementById('palette').value,
            colorMode: document.getElementById('colorMode').value,
            algorithm: document.getElementById('algorithm').value,
            contrast: parseFloat(document.getElementById('contrast').value),
            brightness: parseInt(document.getElementById('brightness').value),
            invert: document.getElementById('invert').checked,
            edgeDetect: document.getElementById('edgeDetect').checked,
            dithering: document.getElementById('dithering').value || null
        };

        // Afficher le loader
        this.showLoader();
        this.hideError();

        try {
            const result = await window.asciiAPI.convertImage(this.currentFile, options);

            if (result.success) {
                // Afficher le résultat
                const output = document.getElementById('asciiOutput');
                if (output) {
                    output.textContent = result.ascii_art;
                }

                // Afficher les métadonnées
                const metadata = document.getElementById('metadata');
                if (metadata && result.metadata) {
                    metadata.innerHTML = `
                        <p><strong>Dimensions:</strong> ${result.metadata.width}x${result.metadata.height}</p>
                        <p><strong>Image originale:</strong> ${result.metadata.original_size[0]}x${result.metadata.original_size[1]}px</p>
                        <p><strong>Palette:</strong> ${result.metadata.palette}</p>
                        <p><strong>Mode:</strong> ${result.metadata.color_mode}</p>
                    `;
                }

                // Activer le bouton de téléchargement
                const downloadBtn = document.getElementById('downloadBtn');
                if (downloadBtn) {
                    downloadBtn.disabled = false;
                }

                this.showSuccess('Image convertie avec succès !');
            }
        } catch (error) {
            this.showError(error.message || 'Erreur lors de la conversion');
        } finally {
            this.hideLoader();
        }
    }

    download() {
        const output = document.getElementById('asciiOutput');
        if (!output || !output.textContent) {
            return;
        }

        const blob = new Blob([output.textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ascii-art.txt';
        a.click();
        URL.revokeObjectURL(url);
    }

    showLoader() {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('active');
        }
    }

    hideLoader() {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.remove('active');
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
        }
    }

    hideError() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.classList.remove('show');
        }
    }

    showSuccess(message) {
        const successDiv = document.getElementById('successMessage');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.classList.add('show');
            setTimeout(() => {
                successDiv.classList.remove('show');
            }, 3000);
        }
    }
}

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.imageConverter = new ImageConverter();
});
