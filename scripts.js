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

  const navigation = document.querySelector('.navigation');
  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.getElementById('navigation-links');

  if (navigation && menuButton && menu) {
    navigation.dataset.enhanced = '';
    menuButton.hidden = false;

    function closeMenu() {
      menu.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    }

    menuButton.addEventListener('click', function () {
      const open = menu.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
    });

    menu.addEventListener('click', function (event) {
      const link = event.target.closest('a');
      if (!link) return;
      closeMenu();
      if (link.hash) {
        const target = document.getElementById(link.hash.slice(1));
        if (target) {
          target.setAttribute('tabindex', '-1');
          target.focus({ preventScroll: true });
        }
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.classList.contains('is-open')) {
        closeMenu();
        menuButton.focus();
      }
    });

    const links = Array.from(menu.querySelectorAll('a[href^="#"]'));
    const sections = links.map(function (link) {
      return document.getElementById(link.hash.slice(1));
    }).filter(Boolean);
    let scrollPending = false;

    function updateNavigation() {
      let current = sections[0];
      sections.forEach(function (section) {
        if (section.getBoundingClientRect().top <= 140) current = section;
      });
      links.forEach(function (link) {
        if (current && link.hash === '#' + current.id) {
          link.setAttribute('aria-current', 'location');
        } else {
          link.removeAttribute('aria-current');
        }
      });
      scrollPending = false;
    }

    window.addEventListener('scroll', function () {
      if (!scrollPending) {
        scrollPending = true;
        requestAnimationFrame(updateNavigation);
      }
    }, { passive: true });
    window.addEventListener('hashchange', updateNavigation);
    updateNavigation();
  }

  const year = document.getElementById('copyright-year');
  if (year) year.textContent = String(new Date().getFullYear());
}());
