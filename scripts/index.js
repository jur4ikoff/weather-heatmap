document.getElementById("resButton").addEventListener("click", async () => {

    const latitude = document.getElementById("latitude").value;
    const longitude = document.getElementById("longitude").value;

    const params = new URLSearchParams(
        {
            latitude: latitude,
            longitude: longitude
        }
    )
    const response = await fetch(`api/heatmap?${params.toString()}`, {
        method: "GET",
        headers: { "Accept": "application/json" },
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


})

async function initMap() {
    await ymaps3.ready;

    const { YMap, YMapDefaultSchemeLayer } = ymaps3;

    const map = new YMap(
        document.getElementById('app'),
        {
            location: {
                center: [37.588144, 55.733842],
                zoom: 10
            }
        }
    );

    map.addChild(new YMapDefaultSchemeLayer());
}

initMap();