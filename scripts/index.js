async function resButtonEventClickedV1(map) {
    const center = map.getCenter()
    const latitude = center[0];
    const longitude = center[1];
    const scale = map.getZoom();

    const params = new URLSearchParams(
        {
            center: `${latitude}&${longitude}`,
            scale: scale,
            width: 1080,
            height: 600
        }
    )

    const response = await fetch(`api/v1/heatmap?${params.toString()}`, {
        method: "GET",
        headers: { "Accept": "maplication/json" },
    });
    if (response.ok == true) {
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);

        document.getElementById("resImg").src = imageUrl;
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }

}




// Функция ymaps.ready() будет вызвана, когда
// загрузятся все компоненты API, а также когда будет готово DOM-дерево.
ymaps.ready(init);
function init() {
    // Создание карты.
    var map = new ymaps.Map("map", {
        // Координаты центра карты.
        // Порядок по умолчанию: «широта, долгота».
        // Чтобы не определять координаты центра карты вручную,
        // воспользуйтесь инструментом Определение координат.
        center: [55.76, 37.64],
        // Уровень масштабирования. Допустимые значения:
        // от 0 (весь мир) до 19.
        zoom: 10
    });

    document.getElementById("resButton").addEventListener("click", async () => resButtonEventClickedV1((map)));
}
