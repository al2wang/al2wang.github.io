(function () {
  'use strict';

  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');

  function isDark() {
    return root.dataset.theme ? root.dataset.theme === 'dark' : systemTheme.matches;
  }

  function updateThemeButton() {
    const label = isDark() ? 'Switch to light theme' : 'Switch to dark theme';
    themeButton.setAttribute('aria-label', label);
    themeButton.setAttribute('title', label);
    themeButton.setAttribute('aria-pressed', String(isDark()));
  }

  if (themeButton) {
    themeButton.hidden = false;
    updateThemeButton();
    themeButton.addEventListener('click', function () {
      const theme = isDark() ? 'light' : 'dark';
      root.dataset.theme = theme;
      try {
        localStorage.setItem('color-theme', theme);
      } catch (error) {
        // The theme still changes when browser storage is unavailable.
      }
      updateThemeButton();
    });
    systemTheme.addEventListener('change', updateThemeButton);
  }

  const year = document.getElementById('copyright-year');
  if (year) year.textContent = String(new Date().getFullYear());
}());
