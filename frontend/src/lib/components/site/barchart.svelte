<script>
	import { scaleLinear } from 'd3-scale';

	export let data = [];
	export let xKey = '';
	export let yKey = '';
	export let xLabel = '';
	export let yLabel = '';

	const padding = { top: 20, right: 15, bottom: 40, left: 40 };
	let width = 500;
	let height = 200;

	function formatMobile(tick) {
		return "'" + tick.toString().slice(-2);
	}

	$: xTicks = data.map((d) => d[xKey]);
	$: yTicks = Array.from({ length: 5 }, (_, i) => i * (Math.max(...data.map((d) => d[yKey])) / 4));

	$: xScale = scaleLinear()
		.domain([0, xTicks.length])
		.range([padding.left, width - padding.right]);

	$: yScale = scaleLinear()
		.domain([0, Math.max(...data.map((d) => d[yKey]))])
		.range([height - padding.bottom, padding.top]);

	$: innerWidth = width - (padding.left + padding.right);
	$: barWidth = innerWidth / xTicks.length;
</script>

<h2>{yLabel} by {xLabel}</h2>

<div class="chart" bind:clientWidth={width} bind:clientHeight={height}>
	<svg>
		<!-- y axis -->
		<g class="axis y-axis">
			{#each yTicks as tick}
				<g class="tick tick-{tick}" transform="translate(0, {yScale(tick)})">
					<line x2="100%" />
					<text y="-4">{tick.toFixed(2)}</text>
				</g>
			{/each}
		</g>

		<!-- x axis -->
		<g class="axis x-axis">
			{#each data as point, i}
				<g class="tick" transform="translate({xScale(i)},{height})">
					<text x={barWidth / 2} y="-4"
						>{width > 380 ? point[xKey] : formatMobile(point[xKey])}</text
					>
				</g>
			{/each}
		</g>

		<g class="bars">
			{#each data as point, i}
				<rect
					x={xScale(i) + 2}
					y={yScale(point[yKey])}
					width={barWidth - 4}
					height={yScale(0) - yScale(point[yKey])}
				/>
			{/each}
		</g>
	</svg>
</div>

<style>
	h2 {
		text-align: center;
		color: #004080; /* Capgemini blue */
	}

	.chart {
		width: 100%;
		max-width: 500px;
		margin: 0 auto;
	}

	svg {
		position: relative;
		width: 100%;
		height: 200px;
	}

	.tick {
		font-family: 'Roboto', sans-serif;
		font-size: 0.725em;
		font-weight: 400;
	}

	.tick line {
		stroke: #ccc;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #004080; /* Capgemini blue */
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}

	.x-axis .tick text {
		text-anchor: middle;
	}

	.bars rect {
		fill: #0070c0; /* Capgemini secondary color */
		stroke: none;
		opacity: 0.85;
	}

	.axis.y-axis .tick:nth-child(odd) line {
		stroke-dasharray: 4;
	}
</style>
