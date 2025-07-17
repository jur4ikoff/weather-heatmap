// document.getElementById("resButton").addEventListener("click", async () => {

//     const latitude = document.getElementById("latitude").value;
//     const longitude = document.getElementById("longitude").value;

//     const params = new URLSearchParams(
//         {
//             latitude: latitude,
//             longitude: longitude
//         }
//     )
//     const response = await fetch(`api/heatmap?${params.toString()}`, {
//         method: "GET",
//         headers: { "Accept": "application/json" },
//     });
//     if (response.ok == true) {
//         const blob = await response.blob();
//         const imageUrl = URL.createObjectURL(blob);

//         document.getElementById("resImg").src = imageUrl;
//     }
//     else {
//         const error = await response.json();
//         console.log(error.message);
//     }


// })

import { YMap, YMapDefaultSchemeLayer } from './lib/ymaps.js'

const map = new YMap(
    document.getElementById('app'),
    {
        location: {
            center: [37.588144, 55.733842],
            zoom: 10
        }
    }
);

map.setLocation({
    center: [47.588144, 55.733842],
    zoom: 10
});


map.addChild(
    new YMapLayer({
      source: 'urlSource',
      type: 'tiles'
    })
  );
  
  map.addChild(
    new YMapLayer({
      source: 'tileGeneratorSource',
      type: 'tiles',
      zIndex: 2000,
      raster: {
        // Опция позволяет дожидаться загрузки всех видимых на экране тайлов до отображения.
        awaitAllTilesOnFirstDisplay: true,
        // Опция задаёт продолжительность анимации отображения загруженных тайлов
        tileRevealDuration: 0
      }
    })
  );
  
  map.addChild(
    new YMapLayer({
      source: 'markerSource',
      type: 'markers',
      zIndex: 2020
    })
  );
  
  map.addChild(
    new YMapLayer({
      source: 'featureSource',
      type: 'features',
      zIndex: 2010
    })
  );


// map.addChild(layer);
map.addChild(new YMapDefaultSchemeLayer());
initMap();