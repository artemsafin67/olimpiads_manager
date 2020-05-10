// That function changes avatar label then registering or editing profile

document.getElementById("avatar_photo").addEventListener("change", function () {
    if (this.files[0]) {
        var fr = new FileReader();

        fr.addEventListener("load", function () {
            document.getElementById("avatar_label").style.backgroundImage = "url(" + fr.result + ")";
        }, false);

    fr.readAsDataURL(this.files[0]);
    }
});
