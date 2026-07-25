// ==========================================
// MAIN APPLICATION LOGIC & VISUAL ANIMATIONS
// ==========================================

let currentLang = 'ar'; // Default language
let allQuestions = [];
let userFacts = {};
let currentQuestionId = 'reason';
let questionsAskedCount = 0;
let lastInferResult = null;

// UI Text Translations
const I18N = {
    ar: {
        brandTitle: "مكتشف المغامرات الذكي",
        langText: "English",
        homeLinkBtn: "الرئيسية",
        heroBadgeText: "🧠 نظام خبير استنتاجي مدعوم بقواعد المعرفة",
        heroTitle: "مكتشف المغامرات الذكي",
        heroSubtitle: "نظام خبير تفاعلي يقيم تفضيلاتك ومخاوفك وميزانيتك لااختيار الوجهة المثالية مع التقييم والتحذيرات وصور الوجهة.",
        feat1Text: "فلترة المخاوف والطيران",
        feat2Text: "تطابق الميزانية والأجواء",
        feat3Text: "معرض صور تفاعلي",
        startBtnText: "🚀 ابدأ المغامرة الآن",
        stepCounter: (step, total) => `الخطوة ${step} من ${total}`,
        whyBtnText: "لماذا هذا السؤال؟",
        resultBannerTitle: "✨ وجهتك المثالية الموصى بها",
        warnTitleText: "⚠ تحذير مهم للرحلة",
        galleryTitle: "📸 معرض صور الوجهة",
        traceBtnText: "⚙ تتبع المنطق والاستدلال",
        restartBtnText: "🔄 تجربة استكشاف جديدة",
        whyModalTitle: "المنطق وراء السؤال",
        traceModalTitle: "تتبع قواعد الاستدلال (Rule Inference Trace)"
    },
    en: {
        brandTitle: "Adventure Matcher",
        langText: "عربي",
        homeLinkBtn: "Home",
        heroBadgeText: "🧠 Rule-Based Forward Chaining Expert System",
        heroTitle: "Adventure Matcher",
        heroSubtitle: "An interactive travel expert system that evaluates your phobias, budget, and desired atmosphere to recommend the perfect destination.",
        feat1Text: "Phobia & Flight Filtering",
        feat2Text: "Budget & Vibe Alignment",
        feat3Text: "Interactive Image Gallery",
        startBtnText: "🚀 Start Adventure Now",
        stepCounter: (step, total) => `Step ${step} of ${total}`,
        whyBtnText: "Why ask?",
        resultBannerTitle: "✨ Your Recommended Destination",
        warnTitleText: "⚠ Important Travel Warning",
        galleryTitle: "📸 Destination Gallery",
        traceBtnText: "⚙ Trace Logic",
        restartBtnText: "🔄 Start Over",
        whyModalTitle: "Behind the Logic",
        traceModalTitle: "Inference Rule Trace"
    }
};

// ==========================================
// INITIALIZATION & EVENT LISTENERS
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initCanvasAnimation();
    fetchQuestions();
});

// Canvas Floating Geometric Shapes — Alive Background
function initCanvasAnimation() {
    const canvas = document.getElementById('bgCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    // Shape types: 0=circle, 1=square, 2=ring, 3=triangle, 4=cross, 5=diamond, 6=hexagon
    const shapeTypes = 7;
    const shapes = [];
    const numShapes = 55;

    const fillColors = [
        'rgba(14, 165, 233, 0.18)',    // Sky blue
        'rgba(139, 92, 246, 0.16)',    // Violet
        'rgba(249, 115, 22, 0.14)',    // Orange
        'rgba(16, 185, 129, 0.16)',    // Emerald
        'rgba(236, 72, 153, 0.14)',    // Rose
        'rgba(245, 158, 11, 0.14)',    // Amber
    ];
    const strokeColors = [
        'rgba(14, 165, 233, 0.35)',
        'rgba(139, 92, 246, 0.30)',
        'rgba(249, 115, 22, 0.28)',
        'rgba(16, 185, 129, 0.30)',
        'rgba(236, 72, 153, 0.28)',
        'rgba(245, 158, 11, 0.28)',
    ];

    for (let i = 0; i < numShapes; i++) {
        const sizeRand = Math.random();
        let size;
        if (sizeRand < 0.3) size = Math.random() * 18 + 8;        // tiny 8-26
        else if (sizeRand < 0.65) size = Math.random() * 30 + 26;  // medium 26-56
        else if (sizeRand < 0.88) size = Math.random() * 40 + 56;  // large 56-96
        else size = Math.random() * 50 + 96;                        // huge 96-146

        const colIdx = Math.floor(Math.random() * fillColors.length);
        shapes.push({
            type: Math.floor(Math.random() * shapeTypes),
            x: Math.random() * width,
            y: Math.random() * height,
            size: size,
            dx: (Math.random() - 0.5) * (0.15 + Math.random() * 0.5),
            dy: (Math.random() - 0.5) * (0.15 + Math.random() * 0.5),
            rotation: Math.random() * Math.PI * 2,
            rotSpeed: (Math.random() - 0.5) * 0.012,
            fillColor: fillColors[colIdx],
            strokeColor: strokeColors[colIdx],
            isOutline: Math.random() > 0.55,
            pulseOffset: Math.random() * Math.PI * 2,
        });
    }

    function drawHexagon(ctx, size) {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 6;
            const px = Math.cos(angle) * size;
            const py = Math.sin(angle) * size;
            if (i === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.closePath();
    }

    function drawTriangle(ctx, size) {
        ctx.beginPath();
        ctx.moveTo(0, -size);
        ctx.lineTo(-size * 0.866, size * 0.5);
        ctx.lineTo(size * 0.866, size * 0.5);
        ctx.closePath();
    }

    function drawCross(ctx, size) {
        const t = size * 0.28;
        ctx.beginPath();
        ctx.moveTo(-t, -size);
        ctx.lineTo(t, -size);
        ctx.lineTo(t, -t);
        ctx.lineTo(size, -t);
        ctx.lineTo(size, t);
        ctx.lineTo(t, t);
        ctx.lineTo(t, size);
        ctx.lineTo(-t, size);
        ctx.lineTo(-t, t);
        ctx.lineTo(-size, t);
        ctx.lineTo(-size, -t);
        ctx.lineTo(-t, -t);
        ctx.closePath();
    }

    function drawDiamond(ctx, size) {
        ctx.beginPath();
        ctx.moveTo(0, -size);
        ctx.lineTo(size * 0.6, 0);
        ctx.lineTo(0, size);
        ctx.lineTo(-size * 0.6, 0);
        ctx.closePath();
    }

    let time = 0;

    function render() {
        ctx.clearRect(0, 0, width, height);
        time += 0.008;

        // Draw faint connecting lines between nearby shapes
        ctx.lineWidth = 0.8;
        for (let i = 0; i < shapes.length; i++) {
            for (let j = i + 1; j < shapes.length; j++) {
                const dx = shapes[i].x - shapes[j].x;
                const dy = shapes[i].y - shapes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 180) {
                    const alpha = (1 - dist / 180) * 0.08;
                    ctx.strokeStyle = `rgba(14, 165, 233, ${alpha})`;
                    ctx.beginPath();
                    ctx.moveTo(shapes[i].x, shapes[i].y);
                    ctx.lineTo(shapes[j].x, shapes[j].y);
                    ctx.stroke();
                }
            }
        }

        shapes.forEach((s) => {
            s.x += s.dx;
            s.y += s.dy;
            s.rotation += s.rotSpeed;

            if (s.x < -s.size) s.x = width + s.size;
            if (s.x > width + s.size) s.x = -s.size;
            if (s.y < -s.size) s.y = height + s.size;
            if (s.y > height + s.size) s.y = -s.size;

            // Subtle pulse breathing
            const pulse = 1 + Math.sin(time * 2 + s.pulseOffset) * 0.06;
            const drawSize = (s.size / 2) * pulse;

            ctx.save();
            ctx.translate(s.x, s.y);
            ctx.rotate(s.rotation);

            switch (s.type) {
                case 0: // Circle
                    ctx.beginPath();
                    ctx.arc(0, 0, drawSize, 0, Math.PI * 2);
                    break;
                case 1: // Rounded Square
                    ctx.beginPath();
                    ctx.roundRect(-drawSize, -drawSize, drawSize * 2, drawSize * 2, drawSize * 0.25);
                    break;
                case 2: // Ring (always outline)
                    ctx.beginPath();
                    ctx.arc(0, 0, drawSize, 0, Math.PI * 2);
                    ctx.lineWidth = Math.max(2, drawSize * 0.08);
                    ctx.strokeStyle = s.strokeColor;
                    ctx.stroke();
                    ctx.restore();
                    return;
                case 3: // Triangle
                    drawTriangle(ctx, drawSize);
                    break;
                case 4: // Cross
                    drawCross(ctx, drawSize);
                    break;
                case 5: // Diamond
                    drawDiamond(ctx, drawSize);
                    break;
                case 6: // Hexagon
                    drawHexagon(ctx, drawSize);
                    break;
            }

            if (s.isOutline) {
                ctx.lineWidth = Math.max(1.5, drawSize * 0.06);
                ctx.strokeStyle = s.strokeColor;
                ctx.stroke();
            } else {
                ctx.fillStyle = s.fillColor;
                ctx.fill();
            }

            ctx.restore();
        });

        requestAnimationFrame(render);
    }

    render();
}

// Language Switcher
function toggleLanguage() {
    currentLang = currentLang === 'ar' ? 'en' : 'ar';
    document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = currentLang;

    updateLanguageUI();

    if (document.getElementById('questionScreen').classList.contains('active')) {
        renderCurrentQuestion();
    } else if (document.getElementById('resultScreen').classList.contains('active') && lastInferResult) {
        renderResults(lastInferResult);
    }
}

function updateLanguageUI() {
    const t = I18N[currentLang];
    for (const key in t) {
        const el = document.getElementById(key);
        if (el && typeof t[key] === 'string') {
            el.innerText = t[key];
        }
    }
}

// Fetch Questions metadata
async function fetchQuestions() {
    try {
        const res = await fetch('/api/questions');
        const data = await res.json();
        allQuestions = data.questions || [];
    } catch (err) {
        console.error('Failed to load questions:', err);
    }
}

// Start Quiz Flow
function startQuiz() {
    userFacts = {};
    questionsAskedCount = 0;
    currentQuestionId = 'reason';
    switchScreen('questionScreen');
    evaluateInference();
}

function resetQuiz() {
    switchScreen('welcomeScreen');
}

function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach((s) => s.classList.remove('active'));
    const target = document.getElementById(screenId);
    if (target) {
        target.classList.add('active');
    }
}

// Evaluate facts via Flask Backend
async function evaluateInference() {
    try {
        const res = await fetch('/api/infer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ facts: userFacts })
        });
        const result = await res.json();
        lastInferResult = result;

        if (result.completed) {
            switchScreen('resultScreen');
            renderResults(result);
        } else {
            currentQuestionId = result.next_question_id;
            renderCurrentQuestion();
        }
    } catch (err) {
        console.error('Inference error:', err);
    }
}

// Render Active Question with Staggered Entrance Animations
function renderCurrentQuestion() {
    const qData = allQuestions.find((q) => q.id === currentQuestionId);
    if (!qData) return;

    const totalEstimate = estimateTotalQuestions();
    const progressPercent = Math.min(100, Math.round(((questionsAskedCount + 1) / totalEstimate) * 100));

    const progressBar = document.getElementById('progressBar');
    if (progressBar) progressBar.style.width = `${progressPercent}%`;

    const stepText = document.getElementById('stepCounterText');
    if (stepText) stepText.innerText = I18N[currentLang].stepCounter(questionsAskedCount + 1, totalEstimate);

    const qTitle = document.getElementById('questionText');
    if (qTitle) qTitle.innerText = qData[`text_${currentLang}`];

    const optsContainer = document.getElementById('optionsContainer');
    if (optsContainer) {
        optsContainer.innerHTML = '';
        qData.options.forEach(([displayObj, val], idx) => {
            const btn = document.createElement('div');
            btn.className = 'option-card';
            btn.style.animationDelay = `${idx * 0.08}s`;
            btn.innerText = displayObj[currentLang];
            btn.onclick = () => selectOption(qData.id, val);
            optsContainer.appendChild(btn);
        });
    }
}

function selectOption(factKey, factValue) {
    userFacts[factKey] = factValue;
    questionsAskedCount++;
    evaluateInference();
}

function estimateTotalQuestions() {
    if (userFacts.reason === 'medical' || userFacts.reason === 'charity') return 3;
    if (userFacts.reason === 'burnout' && userFacts.duration === 'weekend') return 2;
    if (userFacts.phobia === 'flying') return userFacts.duration === 'weekend' ? 3 : 4;
    return 5;
}

// Render Results Page
function renderResults(res) {
    const recs = res.recommendations || [];
    const destTitle = document.getElementById('destTitle');
    const destNameStr = recs.length > 0 ? recs[0][currentLang] : (currentLang === 'ar' ? 'رحلة مفاجئة' : 'Surprise Journey');

    if (destTitle) destTitle.innerText = destNameStr;

    // Rating
    const ratingStr = res.rating || '4.5/5';
    const ratingScore = document.getElementById('ratingScore');
    if (ratingScore) ratingScore.innerText = ratingStr;

    const starIcons = document.getElementById('starIcons');
    if (starIcons) {
        const scoreNum = parseFloat(ratingStr.split('/')[0]) || 4.5;
        const fullStars = Math.floor(scoreNum);
        starIcons.innerText = '★'.repeat(fullStars) + (scoreNum % 1 >= 0.4 ? '½' : '') + '☆'.repeat(5 - Math.ceil(scoreNum));
    }

    // Warning
    const warningText = document.getElementById('warningText');
    if (warningText) {
        warningText.innerText = res.warning || (currentLang === 'ar' ? 'لا توجد تحذيرات حرجة.' : 'No critical warnings.');
    }

    // Gallery
    renderGallery(res.gallery_images, destNameStr);
}

// Modals Handler
function openWhyModal() {
    const qData = allQuestions.find((q) => q.id === currentQuestionId);
    if (!qData) return;

    const modal = document.getElementById('whyModal');
    const content = document.getElementById('whyModalContent');

    if (modal && content) {
        content.innerText = qData[`why_${currentLang}`];
        modal.classList.add('active');
    }
}

function closeWhyModal() {
    const modal = document.getElementById('whyModal');
    if (modal) modal.classList.remove('active');
}

function openTraceModal() {
    if (!lastInferResult) return;
    const modal = document.getElementById('traceModal');
    const body = document.getElementById('traceModalBody');

    if (modal && body) {
        body.innerHTML = '';
        const rules = lastInferResult.rules_fired || [];

        if (rules.length === 0) {
            body.innerHTML = '<p style="color:var(--text-muted);">No rules triggered.</p>';
        } else {
            rules.forEach((r) => {
                const card = document.createElement('div');
                card.className = 'trace-card';
                card.innerHTML = `
                    <div class="trace-id">📌 Rule: ${r.id}</div>
                    <div class="trace-if"><strong>IF:</strong> ${JSON.stringify(r.conditions)}</div>
                    <div class="trace-then"><strong>THEN:</strong> ${JSON.stringify(r.conclusions)}</div>
                    <div class="trace-why"><strong>WHY:</strong> ${r.explanation_en}</div>
                `;
                body.appendChild(card);
            });
        }
        modal.classList.add('active');
    }
}

function closeTraceModal() {
    const modal = document.getElementById('traceModal');
    if (modal) modal.classList.remove('active');
}
