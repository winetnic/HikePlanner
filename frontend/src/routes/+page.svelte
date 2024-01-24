<script>
    let count = 0;

    function increment() {
        count++;
    }

    let downhill = 0;
    let uphill = 0;
    let length = 0;

    let prediction = "n.a."

    async function predict() {
        let result = await fetch(
            "http://localhost:5000/api/predict?" +
                new URLSearchParams({
                    downhill: downhill,
                    uphill: uphill,
                    length: length,
                }),
            {
                method: "GET"
            },
        );
        let data = await result.json();
        console.log(data)
        prediction = data.time;
    }
</script>

<h1>Welcome to SvelteKit</h1>
<p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
</p>

<button on:click={increment}>
    Clicked {count}
    {count === 1 ? "time" : "times"}
</button>

<p>
    <strong>Abwärts [m]</strong>
    <label>
        <input type="number" bind:value={downhill} min="0" max="10000" />
        <input type="range" bind:value={downhill} min="0" max="10000" />
    </label>
</p>

<p>
    <strong>Aufwärts [m]</strong>
    <label>
        <input type="number" bind:value={uphill} min="0" max="10000" />
        <input type="range" bind:value={uphill} min="0" max="10000" />
    </label>
</p>

<p>
    <strong>Distanz [m]</strong>
    <label>
        <input type="number" bind:value={length} min="0" max="30000" />
        <input type="range" bind:value={length} min="0" max="30000" />
    </label>
</p>

<button on:click={predict}>Predict</button>

<p>Dauer: {prediction}</p>
