async function resButtonEventClickedV1(map) {
    // const latitude = document.getElementById("latitude").value;
    // const longitude = document.getElementById("longitude").value;
    // const latitude = document.getElementById("map").;
    console.log("Test");
    const latitude = 45.53434354;
    const longitude = 45.53434354;
    const scale = 10;

    const params = new URLSearchParams(
        {
            center: `${latitude}&${longitude}`,
            scale: scale
        }
    )

    // const bounds = map.getBounds();
    // const topleft = bounds[0] // Шировта, долгота
    // console.log(topleft);

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



async function initMap() {

    await ymaps3.ready;

    const { YMap, YMapDefaultSchemeLayer, YMapFeature } = ymaps3;

    const map = new YMap(
        document.getElementById('map'),
        {
            location: {
                center: [37.588144, 55.733842],
                zoom: 10
            }
        }
    );

    console.log(map.location);
    map.addChild(new YMapDefaultSchemeLayer());

    const lineStringFeature = new YMapFeature({
        id: 'line',
        source: 'featureSource',
        geometry: {
            type: 'LineString',
            coordinates: [
                [37.588144, 55.733842],
                [25.329762, 55.389311]
            ]
        },
        style: {
            stroke: [{ width: 12, color: 'rgb(14, 194, 219)' }]
        }
    });

    map.addChild(lineStringFeature);
    //const test = map.state;
    //const coords = test.center;

    document.getElementById("resButton").addEventListener("click", async () => resButtonEventClickedV1((map)));
    // Подписываемся на изменения центр

}

initMap();