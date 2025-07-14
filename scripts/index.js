document.getElementById("resButton").addEventListener("click", async () => {

    const latitude = document.getElementById("latitude").value;
    const longitude = document.getElementById("longitude").longitude;

    const response = await fetch("api/heatmap", {
        method: "GET",
        headers: { "Accept": "application/json" }
    });
    if (response.ok == true)
    {
        console.log("true");
    }
    else
    {
        const error = await response.json();
        console.log(error.message);
    }


})