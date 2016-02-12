var arch_divs;

function arch_init () {
    var names = ['x86', 'x86_64'];
    arch_divs = {};

    for (var i = 0; i < names.length; i++) {
        var name = names[i];
        arch_divs[name] = document.getElementById(name);
    }

    var radios = document.getElementsByName('arch');

    for (var i = 0; i < radios.length; i++) {
        var radio = radios[i];
        if (radio.checked)
            arch_sel(radio.value);

        radio.addEventListener('change', arch_onchange);
    }
}

function arch_sel (value) {
    for (var name in arch_divs) {
        var dsp = name == value ? 'block' : 'none';
        arch_divs[name].style.display = dsp;
    }
}

function arch_onchange () {
    arch_sel(this.value)
}

// Listen for the DOMContentLoaded event on the document, and
// when it triggers, perform our initialization 
// and add listeners to specific elements of interest.
document.addEventListener('DOMContentLoaded', function () {
    arch_init();
});
