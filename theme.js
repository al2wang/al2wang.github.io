// Apply a saved preference before the first paint. Without one, CSS follows
// the system theme, including when JavaScript or browser storage is disabled.
(function () {
  try {
    const theme = localStorage.getItem('color-theme');
    if (theme === 'light' || theme === 'dark') {
      document.documentElement.dataset.theme = theme;
    }
  } catch (error) {
    // Storage may be unavailable in private browsing or when opening a file.
  }
}());
