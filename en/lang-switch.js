/* ============================================================
   語言切換Feature - Share JS
   用於所有語言版本的站點
   ============================================================ */

// 語言Configuration
const LANG_CONFIG = {
    en: { name: 'Traditional Chinese', flag: '🇹🇼', path: '/en/' },
    cn: { name: 'Simplified Chinese', flag: '🇨🇳', path: '/cn/' },
    en: { name: 'English', flag: '🇬🇧', path: '/en/' },
    ko: { name: '한국어', flag: '🇰🇷', path: '/ko/' },
    ja: { name: '日本語', flag: '🇯🇵', path: '/ja/' }
};

const LANG_ORDER = ['en', 'cn', 'en', 'ko', 'ja'];
const COOKIE_NAME = 'oscar_lang';
const CURRENT_LANG_KEY = 'oscar_current_lang';

// 取得當前語言（從 URL 路徑判斷）
function getCurrentLang() {
    const path = window.location.pathname;
    for (const lang of LANG_ORDER) {
        if (path.includes('/' + lang + '/')) return lang;
    }
    return 'en'; // 默認繁中
}

// 取得語言的基础路徑
function getLangBasePath(lang) {
    return LANG_CONFIG[lang].path;
}

// 取得當前页面的相對路徑（不含語言前綴）
function getCurrentPagePath() {
    const path = window.location.pathname;
    for (const lang of LANG_ORDER) {
        const prefix = '/' + lang + '/';
        if (path.includes(prefix)) {
            return path.substring(path.indexOf(prefix) + prefix.length);
        }
    }
    // 如果是根目錄
    return 'index.html';
}

// 切換語言
function switchLanguage(targetLang) {
    if (targetLang === getCurrentLang()) return;

    // 儲存到 Cookie（1年）
    document.cookie = COOKIE_NAME + '=' + targetLang + '; max-age=31536000; path=/';

    // 儲存到 localStorage
    localStorage.setItem(CURRENT_LANG_KEY, targetLang);

    // 儲存當前页面的表單数據（记憶Feature）
    saveFormData();

    // 儲存到 Firebase(if logged in)
    const local = localStorage.getItem('currentUser');
    if (local) {
        try {
            const user = JSON.parse(local);
            if (window.db && user.uid) {
                window.db.ref('users/' + user.uid + '/language').set(targetLang).catch(() => {});
            }
        } catch (e) {}
    }

    // 跳轉到目標語言的相同页面
    const pagePath = getCurrentPagePath();
    const targetBase = getLangBasePath(targetLang);
    window.location.href = targetBase + pagePath;
}

// 儲存表單数據
function saveFormData() {
    const formData = {};
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach((input, index) => {
        if (input.type === 'password' || input.type === 'checkbox') return;
        const key = 'field_' + index;
        formData[key] = input.value;
        input.setAttribute('data-field-key', key);
    });
    localStorage.setItem('oscar_form_data', JSON.stringify(formData));
}

// 恢復表單数據
function restoreFormData() {
    try {
        const saved = JSON.parse(localStorage.getItem('oscar_form_data') || '{}');
        Object.keys(saved).forEach(key => {
            const el = document.querySelector('[data-field-key="' + key + '"]');
            if (el) el.value = saved[key];
        });
    } catch (e) {}
}

// 建立語言下拉菜單 HTML
function createLangDropdownHTML(currentLang) {
    let html = '<select id="langSwitcher" class="lang-switcher" onchange="switchLanguage(this.value)">';
    for (const lang of LANG_ORDER) {
        const cfg = LANG_CONFIG[lang];
        const selected = lang === currentLang ? ' selected' : '';
        html += '<option value="' + lang + '"' + selected + '>' + cfg.flag + ' ' + cfg.name + '</option>';
    }
    html += '</select>';
    return html;
}

// Initialize語言下拉菜單
function initLangSwitcher() {
    const currentLang = getCurrentLang();

    // 儲存當前語言
    localStorage.setItem(CURRENT_LANG_KEY, currentLang);

    // 恢復表單数據
    restoreFormData();

    // 在导航栏中插入下拉菜單
    const navRight = document.querySelector('.nav-right');
    if (navRight && !document.getElementById('langSwitcher')) {
        const dropdownContainer = document.createElement('li');
        dropdownContainer.style.display = 'flex';
        dropdownContainer.style.alignItems = 'center';
        dropdownContainer.innerHTML = createLangDropdownHTML(currentLang);
        navRight.insertBefore(dropdownContainer, navRight.firstChild);
    }
}

// 页面加載完成後Initialize
document.addEventListener('DOMContentLoaded', function() {
    initLangSwitcher();
});

// 也支援直接調用（用於動態加載）
if (typeof window !== 'undefined') {
    window.switchLanguage = switchLanguage;
    window.getCurrentLang = getCurrentLang;
    window.LANG_CONFIG = LANG_CONFIG;
}