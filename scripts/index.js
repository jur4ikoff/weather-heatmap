async function resButtonEventClickedV1(map) {
    const bounds = map.getBounds();
    const left_down = bounds[0];
    const right_upper = bounds[1];

    const params = new URLSearchParams(
        {
            leftdown: `${left_down[0]}&${left_down[1]}`,
            rightupper: `${right_upper[0]}&${right_upper[1]}`,
            width: document.getElementById("map").offsetWidth,
            height: document.getElementById("map").offsetHeight
        }
    )

    const response = await fetch(`api/v1.0/heatmap?${params.toString()}`, {
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
