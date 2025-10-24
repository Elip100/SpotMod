fetch("SpotMod-dat/data.json")
  .then((response) => response.json())
  .then((data) => {
    data.mods.forEach((mod) => {
      if (mod.enabled) {
        switch (mod.type) {
          case ".css":
            fetch(`SpotMod-dat/mods/${mod.id}`)
              .then((response) => response.text())
              .then((css) => {
                const styleElement = document.createElement("style");
                styleElement.type = "text/css";
                const importantCss = css.replace(
                  /([^{};]+):\s*([^{};]+)/g,
                  "$1: $2 !important",
                );
                styleElement.innerHTML = importantCss;
                document.head.appendChild(styleElement);
              })
              .catch((error) =>
                toast(`Error loading CSS mod: ${mod.id}`, true),
              );
            break;
          default:
            const script = document.createElement("script");
            script.src = `SpotMod-dat/mods/${mod.id}`;
            script.onerror = function () {
              toast(`Error running mod: ${mod.id}`, true);
            };
            document.body.appendChild(script);
        }
      }
    });
    toast("SpotMod loaded!");
  })
  .catch((error) => toast(`Error loading mod list: ${error}`, true));

function toast(text, error = false) {
  Toastify({
    text: text,
    duration: 3000,
    close: true,
    gravity: "bottom",
    position: "right",
    stopOnFocus: true,
    style: {
      background: error ? "red" : "green",
      fontFamily: "sans-serif",
    },
  }).showToast();
}
