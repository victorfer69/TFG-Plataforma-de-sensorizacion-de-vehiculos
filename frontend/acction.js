// Elementos utilizados
const container = document.querySelector(".sensor-container");
let sistemaEnCaptura = false;
const startButton = document.querySelector(".start-button");

// Cargar los identificadores de los sensores
async function loadSensors() {

    try {

        // Obtener la lista de identificadors de los sensores
        const response = await fetch("http://127.0.0.1:8000/sensors");
        const sensors = await response.json();

        console.log("Sensores:", sensors);

        //Para cada sensor se obtiene su manifiesto
        for (const sensorId of sensors) {
            await loadManifest(sensorId);
        }

    } catch(error) {

        console.error("Error cargando sensores:", error);

    }

}

//Obtener el manifiesto del sensor segun el identificador
async function loadManifest(sensorId) {

    try {

        // Realizamos llamada al endpoint
        const response = await fetch(`http://127.0.0.1:8000/sensors/${sensorId}/manifest`);
        const manifest = await response.json();
        console.log("Manifest:", manifest);

        //Mostrar el sensor en el HTML
        renderSensor(manifest);

    } catch(error) {

        console.error(`Error obteniendo manifest de ${sensorId}:`, error);

    }

}

// Mostramos el sensor
function renderSensor(manifest) {

    // Creamos la estructura html
    const card = document.createElement("div");
    card.classList.add("sensor-card");
    card.innerHTML = `

        <div class="sensor-header">

            <h2>${manifest.metadata.title}</h2>

            <div class="sensor-controls">

                <label class="switch">
                    <input type="checkbox" id="switch-${manifest.sensorId}">
                    <span class="slider"></span>
                </label>

                <button class="expand-button">
                    ▼
                </button>

            </div>

        </div>

        <div class="sensor-config hidden" id="config-${manifest.sensorId}">
        
        <div class="sensor-body" id="body-${manifest.sensorId}">

            <div class="config-group">
                
                <div class="input-row-tres-columnas">

                    <div class="field">
                        <label>Valor mínimo:</label>
                        <input type="number" 
                            id="min-${manifest.sensorId}" 
                            min="${manifest.inputs.min_range.minimum}" 
                            max="${manifest.inputs.min_range.maximum}" 
                            value="${manifest.inputs.min_range.currentValue}">
                        <p>${manifest.inputs.min_range.unit}</p>
                    </div>

                    <div class="field">
                        <label>Valor máximo:</label>
                        <input type="number" 
                            id="max-${manifest.sensorId}" 
                            min="${manifest.inputs.max_range.minimum}" 
                            max="${manifest.inputs.max_range.maximum}" 
                            value="${manifest.inputs.max_range.currentValue}">
                        <p>${manifest.inputs.min_range.unit}</p>
                    </div>

                    <div class="field full-width">
                        <label>Alerta umbral:</label>
                        <input type="number" 
                            id="alert-${manifest.sensorId}" 
                            min="${manifest.inputs.alert.minimum}" 
                            max="${manifest.inputs.alert.maximum}" 
                            value="${manifest.inputs.alert.currentValue}">
                        <p>${manifest.inputs.min_range.unit}</p>
                    </div>
                </div>

            </div>

            <hr>

            <div class="config-group selectors-row-dos-columnas">

                <div class="field">
                    <label>Modo captura:</label>
                    <select id="mode-${manifest.sensorId}">
                        <option value="" selected>--Selecciona--</option>
                        <option value="capture_single">capture_single</option>
                        <option value="capture_doble">capture_doble</option>
                        <option value="capture_triple">capture_triple</option>
                    </select>
                </div>

                <div class="field">
                    <label>Frecuencia captura:</label>
                    <select id="freq-${manifest.sensorId}">
                        <option value="" selected>--Selecciona--</option>
                        <option value="100">100 Hz</option>
                        <option value="400">400 Hz</option>
                        <option value="800">800 Hz</option>
                        <option value="1600">1600 Hz</option>
                    </select>
                </div>

            </div>

            <div class="actions">
                <button class="details-button">Ver más detalles</button>
            </div>

        </div>


        <div class="sensor-body-details hidden" id="body-${manifest.sensorId}">

            <p class="sensor-description">
                ${manifest.metadata.description}
            </p>

            <hr>

            <div class="config-group">
                <p class="group-instruction">
                    Los valores de medida deben estar entre ${manifest.inputs.min_range.minimum} y ${manifest.inputs.max_range.maximum} ${manifest.inputs.min_range.unit}.
                </p>
                <div class="input-row">
                    <div class="field">
                        <label>Valor mínimo (por defecto ${manifest.inputs.min_range.default} ${manifest.inputs.min_range.unit}):</label>
                        <input type="number"
                            id="min-${manifest.sensorId}"
                            min="${manifest.inputs.min_range.minimum}"
                            max="${manifest.inputs.min_range.maximum}"
                            value="${manifest.inputs.min_range.currentValue}">
                        <p>${manifest.inputs.min_range.unit}</p>
                    </div>
                    <div class="field">
                        <label>Valor máximo (por defecto ${manifest.inputs.max_range.default} ${manifest.inputs.max_range.unit}):</label>
                        <input type="number"
                            id="max-${manifest.sensorId}"
                            min="${manifest.inputs.max_range.minimum}"
                            max="${manifest.inputs.max_range.maximum}"
                            value="${manifest.inputs.max_range.currentValue}">
                        <p>${manifest.inputs.min_range.unit}</p>
                    </div>
                </div>
                <div class="field full-width">
                    <label>Recibir alerta cada vez que se supere el valor:</label>
                    <input type="number"
                        id="alert-${manifest.sensorId}"
                        min="${manifest.inputs.alert.minimum}"
                        max="${manifest.inputs.alert.maximum}"
                        value="${manifest.inputs.alert.currentValue}">
                    <p>${manifest.inputs.min_range.unit}</p>
                </div>
            </div>

            <hr>

            <div class="config-group selectors-row">
                <div class="field">
                    <label>Modo captura:</label>
                    <select id="mode-${manifest.sensorId}">
                        <option value="" selected>--Selecciona--</option>
                        <option value="capture_single">capture_single</option>
                        <option value="capture_doble">capture_doble</option>
                        <option value="capture_triple">capture_triple</option>
                    </select>
                </div>

                <div class="field">
                    <label>Frecuencia captura:</label>
                    <select id="freq-${manifest.sensorId}">
                        <option value="" selected>--Selecciona--</option>
                        <option value="100">100 Hz</option>
                        <option value="400">400 Hz</option>
                        <option value="800">800 Hz</option>
                        <option value="1600">1600 Hz</option>
                    </select>
                </div>
            </div>

            <hr>

            <div class="config-group outputs-info">
                <h4>Información sobre los canales de salida:</h4>
                <ul>
                    <li><strong>time_vector:</strong> ${manifest.outputs.time_vector.description} (${manifest.outputs.time_vector.unit})</li>
                    <li><strong>output_01:</strong> ${manifest.outputs.output_01.description} (Resolución: ${manifest.outputs.output_01.resolution})</li>
                    <li><strong>output_02:</strong> ${manifest.outputs.output_02.description} (Resolución: ${manifest.outputs.output_02.resolution})</li>
                    <li><strong>output_03:</strong> ${manifest.outputs.output_03.description} (Resolución: ${manifest.outputs.output_03.resolution})</li>
                </ul>
            </div>

            <div class="actions">
                <button class="less-details-button">Ver menos detalles</button>
            </div>


        </div> 


    `;

    // Añadimos el HTML de la página
    container.appendChild(card);

    // Obtenemos el boton de expandir y la zona de configuración
    const expandButton = card.querySelector(".expand-button");
    const config = card.querySelector(".sensor-config");

    // Asignamos el evento de click
    expandButton.addEventListener("click", () => {
        config.classList.toggle("hidden");

        if (config.classList.contains("hidden")) {
            expandButton.textContent = "▼";
        } else {
            expandButton.textContent = "▲";
        }
    });


    // Obtenemos el boton de detalles de las posibles vistas
    const detailsButton = card.querySelector(".details-button");
    const lessDetailsButton = card.querySelector(".less-details-button");
    const sensorBody = card.querySelector(".sensor-body");
    const sensorDetails = card.querySelector(".sensor-body-details")

    // Asignamos el evento de click mostrar detalles
    detailsButton.addEventListener("click", () => {
        sensorBody.classList.add("hidden");
        sensorDetails.classList.remove("hidden");
    });

    // Asignamos el evento de click mostrar menos detalles
    lessDetailsButton.addEventListener("click", () => {
        sensorDetails.classList.add("hidden");
        sensorBody.classList.remove("hidden");
    });

}

// Función que sirve para capturar la información de los sensores e iniciar la captura de datos
async function iniciarCaptura(){

    // Recopilamos la lista de sensores activos
    const response =  await fetch("http://127.0.0.1:8000/sensors");
    const listaSensores =  await response.json();
    const sensoresParaCapturar = [];

    // Encontramos los sensores seleccionados
    for(const sensorId of listaSensores){
        const checkboxEstado = document.getElementById(`switch-${sensorId}`);

        // Sensor activado
        if(checkboxEstado && checkboxEstado.checked){
            const response = await fetch(`http://127.0.0.1:8000/sensors/${sensorId}/manifest`);
            const manifest = await response.json();
            const minVal = parseFloat(document.getElementById(`min-${sensorId}`).value);
            const maxVal = parseFloat(document.getElementById(`max-${sensorId}`).value);
            const alertVal = parseFloat(document.getElementById(`alert-${sensorId}`).value);
            const selectMode = document.getElementById(`mode-${sensorId}`).value;
            const selectFreq = parseInt(document.getElementById(`freq-${sensorId}`).value);

            // Validar datos
            if(!selectMode || !selectFreq){
                alert(`Error en [${sensorId}]: Deber seleccionar un modo y una frecuencia de captura.`);
                return;
            }

            if(isNaN(minVal) || isNaN(maxVal) || isNaN(alertVal)){
                alert(`Error en [${sensorId}]: Los valores del rango y alerta deben de ser números válidos.`);
                return;
            }

            if(minVal >= maxVal){
                alert(`Error en [${sensorId}]: El valor mínimo debe de ser menor que el valor máximo.`);
                return;
            }

            // Guardamos la informacion del sensor en la lista de sensores activos
            sensoresParaCapturar.push({
                sensorId: sensorId,
                minimo: minVal,
                maximo: maxVal,
                alerta: alertVal,
                modo: selectMode,
                frecuencia: selectFreq,
                tipo: manifest.inputs.min_range.type,
                unidad: manifest.inputs.min_range.unit 
            });

            console.log(`El sensor ${sensorId} está activo.`);

        // Sensor apagado
        }else{
            console.log(`El sensor ${sensorId} está apagado.`);
        }
    }

    
    // Si no hay sensores activos
    if(sensoresParaCapturar.length == 0){
        alert("No se puede iniciar la captura de datos: Debes activar el interruptor de al menos un sensor");
        return;
    }

    // Si el sistema esta encendido -> apagarlo
    if(sistemaEnCaptura){

        try{
            // Llamamos al endpoint de detener captura
            console.log("Enviando orden de detención");
            const response = await fetch("http://127.0.0.1:8000/sensors/stop-capture", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(sensoresParaCapturar)
            });

            if(response.ok){
                alert("Captura de datos detenida");
                sistemaEnCaptura = false;
                startButton.textContent = "Iniciar Captura";
                startButton.classList.remove("button-active");
            }else{
                alert("El servidor no ha parado el sensor.")
            }

        }catch (error){
            // Ocurre algún error
            console.error("Error: ", error);
            alert("El servicio de detencion ha fallado.");
        }

    // Si el sistema esta apagado -> encenderlo
    }else{

        try {
            
            // Llamada al endpoint que inicie captura
            const response = await fetch("http://127.0.0.1:8000/sensors/start-capture", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(sensoresParaCapturar)
            });

            const result = await response.json();

            if (response.ok) {
                alert("¡Captura del sistema iniciada correctamente!");
                sistemaEnCaptura = true;
                startButton.textContent = "Detener Captura";
                startButton.classList.add("button-active");
            } else {
                alert(`El servidor rechazó la orden: ${result.detail || "Error interno"}`);
            }

        } catch (error) {
            // Ocurre algún error
            console.error("Error: ", error);
            alert("El servicio de captura de datos ha fallado.")
        }

    }

}

// Iniciar carga
loadSensors();