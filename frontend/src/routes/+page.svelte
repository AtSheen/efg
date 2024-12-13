<script lang="ts">
	import MlForm from '$lib/components/site/mlForm.svelte';
	import StaticTables from '$lib/components/site/staticTables.svelte';
</script>

<div class="grid w-full grid-cols-2 gap-10 h-full">
	<div class="w-full">
		<MlForm />
	</div>
	<div class="w-full overflow-scroll">
		<StaticTables />
	</div>
</div>
