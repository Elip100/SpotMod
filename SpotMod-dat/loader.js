fetch('SpotMod-dat/data.json')
    .then(response => response.json())
    .then(data => {
        data.mods.forEach(mod => {
            if (mod.enabled) {
                const script = document.createElement('script');
                script.src = `SpotMod-dat/mods/${mod.id}`;
                script.onerror = function() {
                    toast(`Error loading mod: ${mod.id}`, true);
                };
                document.body.appendChild(script);
            }
        });
        toast("SpotMod loaded!")
    })
    .catch(error => toast(`Error loading mod list: ${error}`, true))

function toast(text, error = false){
    Toastify({
        text: text,
        duration: 3000,
        close: true,
        gravity: "bottom",
        position: "right",
        stopOnFocus: true,
        style: {
            background: error ? "red" : "green",
            fontFamily: "sans-serif"
        }
    }).showToast();
}