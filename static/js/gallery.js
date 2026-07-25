// ==========================================
// IMAGE GALLERY & LIGHTBOX MODULE
// ==========================================

let currentGalleryImages = [];
let currentImageIndex = 0;

function renderGallery(imagePaths, destinationName) {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return;

    grid.innerHTML = '';
    currentGalleryImages = imagePaths || [];
    currentImageIndex = 0;

    if (!imagePaths || imagePaths.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 20px;">
            📷 No extra gallery photos available for this destination.
        </div>`;
        return;
    }

    imagePaths.forEach((path, idx) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.onclick = () => openLightbox(idx, destinationName);

        const imgUrl = `/images/${path}`;
        item.innerHTML = `
            <img src="${imgUrl}" alt="${destinationName} - Photo ${idx + 1}" loading="lazy">
            <div class="gallery-overlay">
                <span>🔍 View Full</span>
            </div>
        `;
        grid.appendChild(item);
    });
}

function openLightbox(index, destinationName) {
    if (!currentGalleryImages || currentGalleryImages.length === 0) return;
    currentImageIndex = index;

    const modal = document.getElementById('lightboxModal');
    const img = document.getElementById('lightboxImg');
    const caption = document.getElementById('lightboxCaption');

    if (modal && img) {
        const path = currentGalleryImages[currentImageIndex];
        img.src = `/images/${path}`;
        if (caption) {
            caption.innerText = `${destinationName || 'Destination'} — Photo ${currentImageIndex + 1} of ${currentGalleryImages.length}`;
        }
        modal.classList.add('active');
    }
}

function closeLightbox(event) {
    if (event.target.id === 'lightboxModal') {
        closeLightboxDirect();
    }
}

function closeLightboxDirect() {
    const modal = document.getElementById('lightboxModal');
    if (modal) modal.classList.remove('active');
}

function navigateLightbox(direction) {
    if (!currentGalleryImages || currentGalleryImages.length === 0) return;
    currentImageIndex = (currentImageIndex + direction + currentGalleryImages.length) % currentGalleryImages.length;
    
    const img = document.getElementById('lightboxImg');
    const caption = document.getElementById('lightboxCaption');
    if (img) {
        const path = currentGalleryImages[currentImageIndex];
        img.src = `/images/${path}`;
        if (caption) {
            caption.innerText = `Photo ${currentImageIndex + 1} of ${currentGalleryImages.length}`;
        }
    }
}

// Global Keyboard Listener for Lightbox
document.addEventListener('keydown', (e) => {
    const modal = document.getElementById('lightboxModal');
    if (modal && modal.classList.contains('active')) {
        if (e.key === 'Escape') closeLightboxDirect();
        if (e.key === 'ArrowRight') navigateLightbox(1);
        if (e.key === 'ArrowLeft') navigateLightbox(-1);
    }
});
