
function mostrarpsico() {
    var getSelectValue = document.getElementById("select").value;

    switch (getSelectValue) {
        case "0":

            document.getElementById("e_civil").style.display = "none";
            document.getElementById("e_civill").style.display = "none";
            document.getElementById("fechan").style.display = "none";
            document.getElementById("fechal").style.display = "none";
            document.getElementById("hoja").style.display = "none";
            document.getElementById("hojal").style.display = "none";
            document.getElementById("profesion").style.display = "none";
            document.getElementById("profesionl").style.display = "none";
            document.getElementById("telefono").style.display = "none";
            document.getElementById("telefonol").style.display = "none";
            break;
        case "1":
            document.getElementById("fechan").style.display = "inline-block";
            // document.getElementById("fechan").setAttribute("required", "required");
            document.getElementById("fechal").style.display = "inline-block";
            document.getElementById("hoja").style.display = "inline-block";
            // document.getElementById("hoja").setAttribute("required", "required");
            document.getElementById("hojal").style.display = "inline-block";
            document.getElementById("e_civil").style.display = "none";
            document.getElementById("e_civill").style.display = "none";
            document.getElementById("profesion").style.display = "none";
            document.getElementById("profesionl").style.display = "none";
            document.getElementById("telefono").style.display = "none";
            document.getElementById("telefonol").style.display = "none";
            break;

        case "2":
            document.getElementById("e_civil").style.display = "inline-block";
            // document.getElementById("e_civil").setAttribute("required", "required");
            document.getElementById("e_civill").style.display = "inline-block";
            document.getElementById("profesion").style.display = "inline-block";
            // document.getElementById("profesion").setAttribute("required", "required");
            document.getElementById("profesionl").style.display = "inline-block";
            document.getElementById("telefono").style.display = "inline-block";
            // document.getElementById("telefono").setAttribute("required", "required");
            document.getElementById("telefonol").style.display = "inline-block";
            document.getElementById("fechan").style.display = "none";
            document.getElementById("fechal").style.display = "none";
            document.getElementById("hoja").style.display = "none";
            document.getElementById("hojal").style.display = "none";
            // document.getElementById("frphone").style.display = "none";
            break;
    }
}

